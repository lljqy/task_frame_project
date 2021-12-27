from libs import settings


@settings.scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task():
    print("test_app1:运行了任务1")


@settings.background_scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task1():
    print("test_app1:运行了任务2")


@settings.background_scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task2():
    print("test_app1:运行了任务3")
