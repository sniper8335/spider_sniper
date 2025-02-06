import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sniper.config.settings import BASE_DIR

database = {
    'sqlite': 'data.db'
}

class BaseConfig:
    """
    数据库配置：
        创建数据库所必须的配置信息，创建后自动生成系统文件表，记录爬虫创建时间，最后使用时间。
    """
    def __init__(self, DATABASE:dict=None):
        """
        :param DATABASE: 数据库配置信息
        :return: None
        DATABASE为必要参数，字典格式，需要传入数据库类型，以及数据库配置信息，如：
            DATABASE = {
                'sqlite': 'data.db'
            }
        系统目前仅支持sqlite和MySQL数据库，后续会支持SQL_Server、Postgre等数据库
        """
        if DATABASE is None:
            raise '请设置数据库配置！'
        elif DATABASE.get('sqlite'):
            db_name = DATABASE.get('sqlite')
            self.path = BASE_DIR.parent
            dir__ = os.path.join(self.path, db_name)
            self.base_engin = create_engine(f'sqlite:///{dir__}', echo=False, pool_size=1000, pool_recycle=60)
            self.Base = declarative_base()
            self.session = sessionmaker(self.base_engin)
            self.system_session = self.session()
        elif DATABASE.get('mysql'):
            user = DATABASE.get('mysql').get('user')
            password = DATABASE.get('mysql').get('password')
            host = DATABASE.get('mysql').get('host')
            port = DATABASE.get('mysql').get('port')
            database_name = DATABASE.get('mysql').get('db')
            charset = DATABASE.get('mysql').get('charset')
            self.base_engin = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}?charset={charset}',
                                            echo=False, pool_size=1000, pool_recycle=60)
            self.Base = declarative_base()
            self.session = sessionmaker(self.base_engin)
            self.system_session = self.session()


base = BaseConfig(DATABASE=database)


class System(base.Base):
    """
    : param base: 数据库配置
    : return: None
    系统表：
        记录爬虫创建时间，最后使用时间。
    该表为自动创建的表，无需手动创建，无需手动添加数据，系统会自动创建，无需手动操作。
    """
    __tablename__ = 'system'
    id = Column(Integer, autoincrement=True, primary_key=True)
    project_name = Column(String(128))
    create_time = Column(DateTime)
    update_time = Column(DateTime)



