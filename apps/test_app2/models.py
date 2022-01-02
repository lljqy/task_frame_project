import sqlalchemy
from utils.db_utils import BaseModel


class TOfflineTask(BaseModel):
    """
    CREATE TABLE t_offline_tasks(
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        user_name VARCHAR(16) DEFAULT '' COMMENT '用户名',
        task_name VARCHAR(16) DEFAULT '' COMMENT '任务名',
        ip VARCHAR(16) DEFAULT '' COMMENT '数据库服务器ip',
        port int(8) DEFAULT 3306 COMMENT '数据库端口',
        sql_statement TEXT COMMENT '当前需要执行的sql语句',
        params TEXT COMMENT 'sql语句中的格式化参数',
        process VARCHAR(8) DEFAULT '未完成' COMMENT '当前文件下载状态',
        file_path VARCHAR(256) DEFAULT '' COMMENT '文件存储路径',
        last_updated_time DATETIME DEFAULT NOW() COMMENT '最后更新时间',
        add_time DATETIME DEFAULT NOW() COMMENT '数据入库时间'
    ) ENGINE = INNODB CHARSET utf8;
    """
    __tablename__ = 't_offline_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_name = sqlalchemy.Column(sqlalchemy.String(16), server_default=sqlalchemy.text("''"), comment='用户名')
    task_name = sqlalchemy.Column(sqlalchemy.String(16), server_default=sqlalchemy.text("''"), comment='任务名')
    ip = sqlalchemy.Column(sqlalchemy.String(16), server_default=sqlalchemy.text("''"), comment='数据库服务器ip')
    port = sqlalchemy.Column(sqlalchemy.Integer, server_default=sqlalchemy.text("'3306'"), comment='数据库端口')
    sql_statement = sqlalchemy.Column(sqlalchemy.Text, comment='当前需要执行的sql语句')
    params = sqlalchemy.Column(sqlalchemy.Text, comment='sql语句中的格式化参数')
    process = sqlalchemy.Column(sqlalchemy.String(8), server_default=sqlalchemy.text("'未完成'"), comment='当前文件下载状态')
    file_path = sqlalchemy.Column(sqlalchemy.String(256), server_default=sqlalchemy.text("''"), comment='文件存储路径')
    last_updated_time = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.text("CURRENT_TIMESTAMP"),
                                          comment='最后更新时间')
    add_time = sqlalchemy.Column(sqlalchemy.DateTime, server_default=sqlalchemy.text("CURRENT_TIMESTAMP"),
                                 comment='数据入库时间')
