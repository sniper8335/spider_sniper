from sqlalchemy import delete, inspect
from .model import System, base
from pandas import DataFrame


class ORM:
    """
    ORM操作类
    1. create: 创建数据
    2. update_or_create: 更新或创建数据
    3. query_all: 查询所有数据
    4. create_all: 创建或更新数据
    5. get_query_set: 获取查询集
    """
    def __init__(self, model=None, BASE=None):
        """
        初始化ORM操作类
        :param model: 模型类
        :param BASE: 数据库连接对象
        :return: None
        需传入模型类和数据库连接对象，默认为model.py中的model和base.py中的base
        """
        if BASE:
            self.session = BASE.system_session
            self.model = model
        else:
            self.session = base.system_session
            self.model = model

    def create(self, info: list = None):
        """
        创建数据
        :param info: 数据
        :return: None
        传入数据， 数据格式为list，格式为[{},{}]
        此处插入数据没有去重逻辑，逐条插入，保存异常则抛出异常， 回滚
        """
        try:
            query = delete(self.model)
            self.session.execute(query)
            self.session.commit()
        except Exception as e:
            print(f"删除操作出错：{e}")
            self.session.rollback()
        self.session.execute(
            self.model.__table__.insert(),
            info
        )
        self.session.commit()
        self.session.close()

    def update_or_create(self, **kwargs):
        """
        更新或创建数据
        :param kwargs: 数据
        :return: None
        该函数操作数据表system， 该表记录项目创建时间和最后运行时间
        """
        query = self.session.query(System).filter_by(project_name=kwargs.get('project_name'))
        if query.first():
            data = {}
            for k, v in kwargs.items():
                data[k] = v
            query.update(data)
            base.system_session.commit()
        else:
            base.system_session.add(System(**kwargs))
            base.system_session.commit()

    def query_all(self, model: object = None):
        """
        查询所有数据
        :param model: 模型类
        :return: list
        传入模型类，返回该模型类所有数据对象，高层代码需解析该对象获得数据
        """
        query = self.session.query(model).all()
        return query

    def create_all(self,model:object = None, info: list = None):
        """
        创建或更新数据
        :param model: 模型类
        :param info: 数据
        :return: None
        传入模型类和数据，数据格式为list，格式为[{},{}]
        数据保存自动去重，为提高性能，此处采用pandas进行去重操作
        """
        inspector = inspect(model)
        columns = inspector.columns
        if columns:
            column_list = [column for column in columns]
            query_set = self.query_all(model=model)
            if query_set:
                old_info = []
                for query in query_set:
                    data = {}
                    for column in column_list:
                        if column.name != 'id':
                            data[column.name] = query.__dict__[column.name]
                    old_info.append(data)
                new_info = DataFrame(old_info + info).drop_duplicates().to_dict(orient='records')
                self.create(info=new_info)
            else:
                self.create(info=info)

    def get_query_set(self, model: object = None):
        """
        获取查询集
        :param model: 模型类
        :return: list[dict]
        传入模型类，返回查询集数据，类似Django的QuerySet
        """
        inspector = inspect(model)
        columns = inspector.columns
        column_list = [column for column in columns]
        querys = self.session.query(model).all()
        if querys:
            data = []
            for query in querys:
                data.append({column.name: query.__dict__[column.name] for column in column_list})
            return data
        else:
            return []



