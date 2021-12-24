from settings import *

DEBUG = True

DATABASES = {
    "test_app": "mysql+pymysql://root:123456@localhost:3306/scheduler",
    "test_manticore": "mysql+pymysql://root:123456@localhost:9306/ ",
}

job_stores = {
    'default': SQLAlchemyJobStore(url=DATABASES['test_app'])
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
