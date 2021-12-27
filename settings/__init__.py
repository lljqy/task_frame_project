import os
import logging
from urllib.parse import quote_plus

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
    filemode='a',
    encoding='utf-8',
)


def job_exception_listener(event):
    scheduled_run_time = event.scheduled_run_time.strftime("%Y-%m-%d %H:%M:%S")
    if event.exception:
        # todo：异常处理, 告警等
        logger.error(f'调度任务({event.job_id})在{scheduled_run_time}时刻失败 :(, 原因是：{event.exception}')
    else:
        logger.info(f'调度任务({event.job_id})在{scheduled_run_time}时刻成功运行 :)')


def convert_db_conf_to_url(db_conf):
    """
    将django类似的配置文件转化为sqlalchemy链接数据库的url
    :param db_conf:
    :return:
    """
    return f"{db_conf['ENGINE']}://{db_conf['USER']}:{quote_plus(db_conf['PASSWORD'])}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['NAME']}"


executors = {
    'default': ThreadPoolExecutor(30),
    'processpool': ProcessPoolExecutor(5),
}

job_defaults = {
    'coalesce': True,
    'max_instance': 2,
}

INSTALL_APPS = (
    'apps.test_app',
    'apps.test_app1',
)
