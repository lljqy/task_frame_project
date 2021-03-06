from settings import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "mysql+pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "scheduler",
    },
    "test_app": {
        "ENGINE": "mysql+pymysql",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "scheduler",
    },
}

job_stores = {
    'default': SQLAlchemyJobStore(url=convert_db_conf_to_url(DATABASES['test_app'])),
    'memory': MemoryJobStore(),
}

scheduler = BlockingScheduler(
    jobstores=job_stores,
    executors=executors,
    jobdefaults=job_defaults,
    replace_existing=True
)

background_scheduler = BackgroundScheduler(
    jobstores=job_stores,
    executors=executors,
    jobdefaults=job_defaults,
    replace_existing=True
)
asyncio_scheduler = AsyncIOScheduler(
    jobstores=job_stores,
    executors=executors,
    jobdefaults=job_defaults,
    replace_existing=True
)

# 设置任务监听
scheduler.add_listener(job_exception_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
background_scheduler.add_listener(job_exception_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
asyncio_scheduler.add_listener(job_exception_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
