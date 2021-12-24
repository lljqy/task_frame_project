# coding: utf-8
from sqlalchemy import Column, Date, Float, Integer, String, text

from utils.db_utils import BaseModel


class Temperature(BaseModel):
    app_name = "test_app"
    __tablename__ = 'temperature'
    __table_args__ = {'comment': '温度表'}

    id = Column(Integer, primary_key=True)
    barcode = Column(String(32), index=True, server_default=text("''"), comment='条码')
    country = Column(String(16), server_default=text("''"), comment='国家')
    country_en = Column(String(32), server_default=text("''"), comment='国家英文名称')
    content = Column(String(2048), server_default=text("''"), comment='描述内容')
    data_date = Column(Date, server_default=text("'1970-01-01'"), comment='数据日期')
    temp_max = Column(Float, server_default=text("'0'"), comment='最高温度')
    temp_min = Column(Float, server_default=text("'0'"), comment='最低温度')
    temp_avg = Column(Float, server_default=text("'0'"), comment='平均温度')
