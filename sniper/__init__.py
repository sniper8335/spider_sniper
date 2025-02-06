from sniper.response.parse import Response
from sniper.spider.request import Spider
from sniper.utils import timer, get_params, read_cache, Path
from sniper.database.model import base
from sniper.create_project import Create
from sniper.scheduler import TaskList, Run, SpiderList
from sniper.download import Down
from sniper.database.ORM import ORM


class Crawl(Spider, Response):
    """
    配置爬虫类，继承此类，实现爬取逻辑
    """

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)
        file_path = Path(self.CACHE_PATH) / self.spider_name
        if not file_path.exists():
            file_path.mkdir()
        csv_path = Path(self.ROOT_PATH) / self.spider_name / 'csv'
        if not csv_path.exists():
            csv_path.mkdir()
        self.csv_path = str(Path(csv_path / self.name))
        self.file_name = str(Path(file_path / self.name))


    def save(self):
        """
        保存数据到缓存文件
        """
        data = self.resp_pars(project_name=self.spider_name)
        if data:
            self.cache_data(path=self.file_name,
                            info=data,
                            project_name=self.spider_name)

    def save_to_sql(self, model:object=None, BASE:object=None):
        """
        保存数据到数据库
        :param model: 数据库模型
        :param BASE: 数据库配置
        :return:None
        """
        cache_list = read_cache(file_name=self.file_name, spider_name=self.spider_name)
        if cache_list:
            self.to_sql_create(info=cache_list, model=model, project_name=self.spider_name, BASE=BASE)
        else:
            data = self.resp_pars(project_name=self.spider_name)
            if data:
                self.to_sql_create(info=data, model=model, project_name=self.spider_name, BASE=BASE)

    def save_to_csv(self, model:object=None):
        """
        保存数据到csv文件
        :param model: 数据库模型
        :return: None
        """
        cache_list = read_cache(file_name=self.file_name, spider_name=self.spider_name)
        if cache_list:
            self.to_csv(path=self.csv_path, info=cache_list, project_name=self.spider_name, model=model)
        else:
            data = self.resp_pars(project_name=self.spider_name)
            if data:
                self.to_csv(path=self.csv_path, info=data, project_name=self.spider_name, model=model)