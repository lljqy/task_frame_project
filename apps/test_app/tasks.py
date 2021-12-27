import string
from random import choices, randint

import pandas as pd

from apps.test_app import models
from utils import constants
from libs import settings

scheduler = settings.scheduler

date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range('2019-01-01', '2021-12-31')]


def get_barcode(k=20):
    possible_str = string.digits + string.ascii_uppercase
    return ''.join(choices(possible_str, k=k))


def get_country():
    en = choices(list(constants.COUNTRY.keys()), k=1)[0]
    return en, constants.COUNTRY.get(en)


def get_data_date():
    return choices(date_range, k=1)


def get_temp():
    return randint(0, 31), randint(31, 66), randint(66, 101)


@settings.background_scheduler.scheduled_job("interval", seconds=50, misfire_grace_time=600,id="test_app__generate_data")
def generate_data():
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始生成数据")
    model = models.Temperature
    session = model.session()
    objs = []
    for _ in range(int(10e2)):
        barcode = get_barcode()
        country_en, country = get_country()
        data_date = get_data_date()
        content = "巴拉巴拉不知道是啥，就这样吧"
        temp_min, temp_avg, temp_max = get_temp()
        obj = model(
            barcode=barcode,
            country_en=country_en,
            country=country,
            data_date=data_date,
            content=content,
            temp_min=temp_min,
            temp_avg=temp_avg,
            temp_max=temp_max,
        )
        objs.append(obj)
    session.add_all(objs)
    session.commit()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 成功生成数据")


@settings.scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task():
    print("运行了任务1")


@settings.background_scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task1():
    print("运行了任务2")


@settings.background_scheduler.scheduled_job('interval', seconds=60, misfire_grace_time=600)
def test_task2():
    print("运行了任务3")
