from datetime import datetime
from typing import Iterator
from sniper.database.save_to_loca import SaveData
from sniper.database.ORM import ORM
from sniper.utils import timer


class Response:
    """
    返回数据基类，通过继承类。重写回调函数实现数据解析
    """

    def parse(self, callback=None, max_req=32) -> Iterator:
        """
        解析response响应对象，返回list，
        :param max_req: int
        :example [{]{str:str},{str:str}]
        :param callback: response
        :return: iterator
        """

        for response in self.response(max_req=max_req):
            for data in callback(response):
                yield data

    @timer
    def to_csv(self,
               path: str = None,
               info: list[dict] = None,
               project_name=None,
               model=None,
               BASE=None) -> None:
        """
        保存到csv文件
        :param project_name: str
        :param model: object
        :param path: str
        :param info: list
        :param BASE: 用户配置文件中的BASE
        :return: None
        """
        orm = ORM(model=model, BASE=BASE)
        save = SaveData(path=path)
        save.df_to_csv(info=info)
        orm.update_or_create(project_name=project_name, update_time=datetime.now())

    @timer
    def to_sql_create(self,
                      info: list[dict] = None,
                      model=None,
                      project_name=None,
                      BASE=None) -> None:
        """
        保存到sql数据库，新增
        :param project_name: str
        :param info: list exampl: [{str:str},{str:str}]
        :param model: 模型类
        :param BASE: 用户配置文件中的BASE
        :return: None
        """
        orm = ORM(model=model, BASE=BASE)
        orm.create_all(model=model, info=info)
        orm.update_or_create(project_name=project_name, update_time=datetime.now())

    @timer
    def resp_pars(self,
                  response=None,
                  max_req=32,
                  project_name=None) -> list[dict]:
        """
        返回列表形式：[{str, str},{str, str}]
        :param project_name: str
        :param max_req: int
        :param response: response
        :return: list
        """
        data_list = []
        for data in self.parse(callback=self.html_pars, max_req=max_req):
            data_list.append(data)
        return data_list

    @timer
    def to_pdf(self,
               path: str = None,
               info: list[dict] = None,
               project_name=None,
               model=None,
               BASE=None):
        """
        保存到pdf文件
        :param path: str
        :param info: list
        :param project_name: str
        :param model: object
        :param BASE: 用户配置文件中的BASE
        :return: None
        """
        orm = ORM(model=model, BASE=BASE)
        save = SaveData(path=path)
        orm.update_or_create(project_name=project_name, update_time=datetime.now())
        for data in info:
            save.to_media(info=data)


    def cache_data(self, path: str = None,
                   info: list[dict] = None,
                   project_name=None) -> None:
        """
        缓存数据到文件
        :param path: str
        :param info: list
        :param project_name: str
        :return: None
        """
        save = SaveData(path=path)
        save.cache(info=info, spider_name=project_name)


    def html_pars(self) -> list[dict]:
        """
        网页解析函数，重写此函数，实现网页解析功能
        返回列表形式：[{str, str},{str, str}]
        :return: list
        """
        pass

    def save(self) -> None:
        """
        系统提供保存方法
        :return: None
        """
        pass
