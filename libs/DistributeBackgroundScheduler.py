"""
author: llj 2021-12-26
功能：分布式的调度器，只能在单机上进行分布式调度（利用了文件锁）
"""
import os
import six
import fcntl
from datetime import datetime, timedelta

from apscheduler.util import timedelta_seconds, TIMEOUT_MAX
from apscheduler.executors.base import MaxInstancesReachedError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import JobSubmissionEvent, EVENT_JOB_SUBMITTED, EVENT_JOB_MAX_INSTANCES

#: constant indicating a scheduler's stopped state
STATE_STOPPED = 0
#: constant indicating a scheduler's running state (started and processing jobs)
STATE_RUNNING = 1
#: constant indicating a scheduler's paused state (started but not processing jobs)
STATE_PAUSED = 2


class DistributedBackgroundScheduler(BackgroundScheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _process_jobs(self):
        """
        Iterates through jobs in every jobstore, starts jobs that are due and figures out how long
        to wait for the next round.

        If the ``get_due_jobs()`` call raises an exception, a new wakeup is scheduled in at least
        ``jobstore_retry_interval`` seconds.
        """
        if self.state == STATE_PAUSED:
            self._logger.debug('pid: %s Scheduler is paused -- not processing jobs' % os.getpid())
            return None
        f = None
        try:
            f = open("scheduler.lock", "wb")
            # 这里必须使用 lockf, 因为 gunicorn 的 worker 进程都是 master 进程 fork 出来的
            # flock 会使子进程拥有父进程的锁
            # fcntl.flock(flock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._logger.info("pid: %s get Scheduler file lock success" % os.getpid())
        except BaseException as exc:
            self._logger.warning("pid: %s get Scheduler file lock error: %s" % (os.getpid(), str(exc)))
            try:
                if f:
                    f.close()
            except BaseException:
                pass
            return None
        else:
            self._logger.debug('pid: %s Looking for jobs to run' % os.getpid())
            now = datetime.now(self.timezone)
            next_wakeup_time = None
            events = []

            with self._jobstores_lock:
                for jobstore_alias, jobstore in six.iteritems(self._jobstores):
                    try:
                        due_jobs = jobstore.get_due_jobs(now)
                    except Exception as e:
                        # Schedule a wakeup at least in jobstore_retry_interval seconds
                        self._logger.warning('pid: %s Error getting due jobs from job store %r: %s',
                                             os.getpid(), jobstore_alias, e)
                        retry_wakeup_time = now + timedelta(seconds=self.jobstore_retry_interval)
                        if not next_wakeup_time or next_wakeup_time > retry_wakeup_time:
                            next_wakeup_time = retry_wakeup_time

                        continue

                    for job in due_jobs:
                        # Look up the job's executor
                        try:
                            executor = self._lookup_executor(job.executor)
                        except BaseException:
                            self._logger.error(
                                'pid: %s Executor lookup ("%s") failed for job "%s" -- removing it from the '
                                'job store', os.getpid(), job.executor, job)
                            self.remove_job(job.id, jobstore_alias)
                            continue

                        run_times = job._get_run_times(now)
                        run_times = run_times[-1:] if run_times and job.coalesce else run_times
                        if run_times:
                            try:
                                executor.submit_job(job, run_times)
                            except MaxInstancesReachedError:
                                self._logger.warning(
                                    'pid: %s Execution of job "%s" skipped: maximum number of running '
                                    'instances reached (%d)', os.getpid(), job, job.max_instances)
                                event = JobSubmissionEvent(EVENT_JOB_MAX_INSTANCES, job.id,
                                                           jobstore_alias, run_times)
                                events.append(event)
                            except BaseException:
                                # 分配任务错误后马上释放文件锁，让其他 worker 抢占
                                try:
                                    fcntl.flock(f, fcntl.LOCK_UN)
                                    f.close()
                                    self._logger.info("pid: %s unlocked Scheduler file success" % os.getpid())
                                except:
                                    pass
                                self._logger.exception('pid: %s Error submitting job "%s" to executor "%s"',
                                                       os.getpid(), job, job.executor)
                                break
                            else:
                                event = JobSubmissionEvent(EVENT_JOB_SUBMITTED, job.id, jobstore_alias,
                                                           run_times)
                                events.append(event)

                            # Update the job if it has a next execution time.
                            # Otherwise remove it from the job store.
                            job_next_run = job.trigger.get_next_fire_time(run_times[-1], now)
                            if job_next_run:
                                job._modify(next_run_time=job_next_run)
                                jobstore.update_job(job)
                            else:
                                self.remove_job(job.id, jobstore_alias)

                    # Set a new next wakeup time if there isn't one yet or
                    # the jobstore has an even earlier one
                    jobstore_next_run_time = jobstore.get_next_run_time()
                    if jobstore_next_run_time and (next_wakeup_time is None or
                                                   jobstore_next_run_time < next_wakeup_time):
                        next_wakeup_time = jobstore_next_run_time.astimezone(self.timezone)

            # Dispatch collected events
            for event in events:
                self._dispatch_event(event)

            # Determine the delay until this method should be called again
            if next_wakeup_time is None:
                wait_seconds = None
                self._logger.debug('pid: %s No jobs; waiting until a job is added', os.getpid())
            else:
                wait_seconds = min(max(timedelta_seconds(next_wakeup_time - now), 0), TIMEOUT_MAX)
                self._logger.debug('pid: %s Next wakeup is due at %s (in %f seconds)', os.getpid(), next_wakeup_time,
                                   wait_seconds)
            try:
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()
                self._logger.info("pid: %s unlocked Scheduler file success" % os.getpid())
            except:
                pass

        return wait_seconds
