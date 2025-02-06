from datetime import datetime
from pathlib import Path
from collections import deque

import pandas
from concurrent.futures import ProcessPoolExecutor, as_completed

from sniper.database.ORM import ORM
from sniper.scheduler.loader import Loader
from sniper.utils import timer



class SpiderActuator:
    """
    爬虫执行器，多进程执行爬虫任务
    """

    def __init__(self,
                 spider_list: list[object] = None,
                 max_number: int = 32):
        """
        接受并发执行数量max_number和爬虫列表spider_list
        :param spider_list: list[object]
        :param max_number: int=32
        """
        self.spider_list = spider_list
        self.start(max_num=max_number)

    @timer
    def start(self, max_num: int = 32) -> None:
        """
        :param max_num: int=32
        多进程爬虫执行器
        设置最大并发数量，启动爬虫
        """
        with ProcessPoolExecutor(max_workers=max_num) as executor:
            as_completed([executor.submit(self.spider_run, spider=spider) for spider in self.spider_list])

    def spider_run(self, spider: object = None) -> None:
        spider.save()

class Run:
    """
    执行多爬虫运行系统
    """
    def __init__(self,
                 spiders: list[object],
                 max_num: int = 32) -> None:
        print('project start now', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'spider number: ', len(spiders))
        self.spiders = spiders
        self.start_project(max_num=max_num)

    def export_spiders(self) -> list[object]:
        """
        导出爬虫对象的列表
        :return:
        """
        spider_list = []
        for spider in self.spiders:
            res, spider_ = Loader(spider).export_spider()
            spider_list.append(spider_)
        return spider_list

    @timer
    def start_project(self, max_num: int = 32,) -> None:
        """
        设置最大并行数量
        :param max_num: int
        :return: object
        """
        spider_list = self.export_spiders()
        SpiderActuator(spider_list, max_number=max_num)


    @staticmethod
    @timer
    def to_sql(spider: object = None,
               model:object=None,
               cache_path=None,
               BASE:object=None) -> None:
        """
        :param spider: object 爬虫对象
        :param model: object 数据库模型对象
        :param cache_path: str 缓存路径
        :param BASE: object 数据库模型对象
        :return: None
        将缓存数据保存到数据库
        """
        orm = ORM(model=model, BASE=BASE)
        info = []
        for data_path in Path.iterdir(Path(cache_path) / spider.spider_name):
            data_dict = pandas.read_feather(data_path).to_dict(orient='records')
            if data_dict:
                info += data_dict
        orm.create_all(model=model, info=info)

    @staticmethod
    @timer
    def to_csv(spider: object = None,
               cache_path=None,
               csv_path = None) -> None:
        """
        将缓存数据保存到csv文件
        """
        info = []
        csv_file_name = Path(csv_path) / f'{spider.spider_name}.csv'
        for data_path in Path.iterdir(Path(cache_path) / spider.spider_name):
            data_dict = pandas.read_feather(data_path).to_dict(orient='records')
            if data_dict:
                info += data_dict
        pandas.DataFrame(info).to_csv(path_or_buf=csv_file_name, encoding='utf-8', index=False)

class SpiderList:
    """
    爬虫列表，用于管理爬虫对象，包括：
    1. 爬虫对象的创建
    2. 爬虫对象的运行
    3. 爬虫对象的停止
    """
    def __init__(self,
                 spider: object = None,
                 query_set: list[dict] = None):
        """
        :param spider: object
        :param query_set: list[dict]
        控制创建爬虫对象的最大数量
        """
        self.query_set = query_set
        self.spider = spider

    def spider_create(self, spider=None, **kwargs):
        """
        创建爬虫对象
        :param spider: object
        :param kwargs: dict
        """
        spider = spider(**kwargs)
        return spider

    def spider_to_list(self, max_number: int = 32):
        """
        多进程创建爬虫对象
        :param max_number: int=32
        :return: list[object]
        多进程创建爬虫对象
        """
        with ProcessPoolExecutor(max_workers=max_number) as executor:
            result = as_completed([executor.submit(self.spider_create, spider=self.spider, **kw) for kw in self.query_set])
            return [future.result() for future in result]

class TaskList:
    """
    任务列表，用于管理爬虫任务，包括：
    1. 任务列表的创建
    2. 任务列表的运行
    3. 任务列表的停止
    """

    def  __init__(self,
                 max_length: int = 100,
                 spider: object = None,
                 query_set: list[dict] = None,
                 max_number: int = 32):
        """
        :param max_length: int=100
        :param spider: object
        :param query_set: list[dict]
        :param max_number: int=32
        控制爬虫任务列表的最大长度， 当任务列表长度超过最大长度时，会自动删除最旧的任务，
        任务列表长度小于最大长度时，会自动添加新的任务， 控制进程的最大数量
        """
        self.max_length = max_length
        self.query_set = query_set
        self.spider = spider
        self.stop_flag = False
        self.max_number = max_number

    def get_fixed_length_list(self,
                              input_list: list[dict])\
                              -> list[dict[str, object]]:
        """
        :param input_list: list[dict]
        :return: list[dict[str, object]]
        保证任务列表的长度为max_length，
        当任务列表长度超过max_length时，
        会自动删除最旧的任务
        """
        q = deque(maxlen=self.max_length)
        for item in input_list:
            q.append(item)
            if self.stop_flag:
                break
        return list(q)

    def put_task(self,
                 model: object = None,
                 cache_path=None,
                 BASE=None,
                 max_number: int = 32,
                 csv_path=None) -> None:
        """
        将任务列表添加到任务列表中，当任务列表长度超过max_length时，会自动删除最旧的任务
        保存当前任务到csv文件和数据库
        :param model: object
        :param cache_path: str
        :param BASE: object
        :param max_number: int=32
        :param csv_path: str
        :return: None
        """
        total_segments = int(len(self.query_set) / self.max_length) + (
            1 if len(self.query_set) % self.max_length else 0)
        for i in range(total_segments):
            if i == total_segments - 1:
                self.stop_flag = True
            item = self.query_set[i * self.max_length:(i + 1) * self.max_length]
            spider_list = SpiderList(spider=self.spider, query_set=item).spider_to_list(max_number=self.max_number)
            Run(spiders=spider_list, max_num=max_number)
            if model and cache_path and BASE:
                Run.to_sql(spider=self.spider, model=model, cache_path=cache_path, BASE=BASE)
            elif csv_path and cache_path:
                Run.to_csv(spider=self.spider, cache_path=cache_path, csv_path=csv_path)

    def task_run(self,
                 model: object = None,
                 cache_path=None,
                 csv_path=None,
                 BASE=None,
                 max_number: int = 32) -> None:
        """
        不适用队列，直接运行任务列表
        保存当前任务到csv文件和数据库
        :param model: object
        :param cache_path: str
        :param csv_path: str
        :param BASE: object
        :param max_number: int=32
        """
        spider_list = SpiderList(spider=self.spider, query_set=self.query_set).spider_to_list(max_number=self.max_number)
        Run(spiders=spider_list, max_num=max_number)
        if model and cache_path and BASE:
            Run.to_sql(spider=self.spider, model=model, cache_path=cache_path, BASE=BASE)
        elif csv_path and cache_path:
            Run.to_csv(spider=self.spider, cache_path=cache_path, csv_path=csv_path)

