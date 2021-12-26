import os
import logging

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED

PATH = os.path.dirname(os.path.dirname(__file__))

logger = logging.getLogger('apscheduler_task')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join(PATH, 'logs', 'apscheduler_task.log'),
    filemode='a'
)


def job_exception_listener(event):
    if event.exception:
        # todo：异常处理, 告警等
        logger.error('The job crashed :(')
    else:
        logger.info('The job worked :)')


executors = {
    'default': ThreadPoolExecutor(20),
    'process_pool': ProcessPoolExecutor(5),
}

job_defaults = {
    'coalesce': False,
    'max_instance': 2
}

INSTALL_APPS = (
    'apps.test_app',
    'apps.test_app1',
)
