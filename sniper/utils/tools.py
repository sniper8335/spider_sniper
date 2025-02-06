import time

from sniper.config.settings import PARAMS_

from datetime import datetime
from pathlib import Path
import pandas


# 运行时间函数
def timer(functions):
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            func = functions(*args, **kwargs)
            name = kwargs.get('project_name')
            if name:
                print(f"{name} {functions.__name__} run at ：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}======================>", f" took {round(time.time() - start, 2)} seconds")
            else:
                print(f"{functions.__name__} run at ：======================>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f" took {round(time.time() - start, 2)} seconds")
            return func
        except Exception as e:
            print(e)
        print("runtime：======================>", f" took {round(time.time() - start, 2)} seconds")
    return wrapper


# URL提取params参数
def get_params(url_str: str = None) -> dict:
    """
    URL分解params参数，返回字典
    :param url_str: 含有params的URL链接
    :return: dict
    """
    params = PARAMS_(url_str=url_str)
    return params.params()

@timer
def read_cache(file_name:str=None, spider_name:str=None) -> list[dict]:
    """
    读取缓存文件
    :param file_name: 缓存文件名
    :param spider_name: 爬虫名称
    :return: list[dict]
    """
    files = f'{file_name}_{spider_name}.feather'
    file_exist = Path(files)
    if file_exist.exists():
        cache = pandas.read_feather(file_exist).to_dict(orient='records')
        return cache
    else:
        return []

