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


def generate_data():
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始生成数据")
    model = models.Temperature
    session = model.session()
    objs = []
    for _ in range(int(10e4)):
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

@settings.background_scheduler.scheduled_job('interval', seconds=5)
def migrate_data_from_mysql_to_manticore():
    model = models.Temperature
    OFFSET = 5000
    pk = 0
    columns = ['id', 'barcode', 'country', 'country_en', 'content', 'data_date', 'temp_max', 'temp_min', 'temp_avg']
    while True:
        rows = model.objects().filter(model.id > pk).order_by(model.id).limit(OFFSET).all()
        if not rows:
            break
        res = []
        for row in rows:
            res.append(row.to_tuple())
        import pymysql
        conn = pymysql.connect(
            user='root',  # The first four arguments is based on DB-API 2.0 recommendation.
            password=" ",
            host='127.0.0.1',
            database=' ',
            port=9306,
            charset="utf8",
        )
        with conn.cursor() as cur:
            cur.executemany(
                f"INSERT INTO temperature({','.join(columns)}) VALUES({','.join(['%s'] * len(columns))})",
                res
            )
        conn.commit()
        conn.close()
        pk = rows[-1][0]
        print(f"id小于{pk}的同步完成")


scheduler.add_job(generate_data, "interval", seconds=50, id="test_app__generate_data")
from datetime import datetime

# scheduler.add_job(migrate_data_from_mysql_to_manticore, "date", run_date=datetime(year=2021, month=12, day=24, hour=0, minute=10))
