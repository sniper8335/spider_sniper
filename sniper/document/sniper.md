# 一、 项目架构
    sniper
        |——config
            |——__init__.py
            |——settings.py
        |——create_project
            |——__init__.py
            |——start_project.py
        |——database
            |——__init__.py
            |——model.py
            |——save_to_loca.py
        |——document
            |——__init__.py
            |——sniper.eddx
            |——sniper.jpg
        |——download
            |——__init__.py
            |——media.py
        |——request
            |——__init__.py
            |——request.py
        |——response
            |——__init__.py
            |——parse.py
        |——scheduler
            |——__init__.py
            |——actuator.py
            |——loader.py
        |——spider
            |——__init__.py
            |——request.py
        |——template
            |——__init__.py
            |——model.tmpl
            |——settings.tmpl
            |——spider.tmpl
        |——utils
            |——__init__.py
            |——tools.py
        |——__init__.py
        |——sniper.md
---

# 二、 项目架构图
![图片描述](sniper.jpg)

---
# 三、 项目概述

* 该项目为轻量级爬虫脚本，皆在简化爬虫设计，符合开发习惯，高并发场景下创建多爬虫进行任务爬取，
  秉承多个爬虫一定比单个爬虫效率高的理念，使用python中常用库进行开发而成。
---
## 3.1 创建爬虫

### 3.1.1 模板创建爬虫

* 通过导入sniper中create模块实现自动通过模板文件创建爬虫，简化爬虫创建过程，减少重复代码的编写，提高工作效率
* Example
****
    from sniper import Create

    Create().create_project()

**** 
    请输入项目名称：baidu
    请输入项目URL：www.baidu.com
*
    右键正常执行脚本后，项目名称和项目URL回车，即可完成爬虫项目的创建，其中包括基础框架代码，数据模型创建等
 ---
### 3.1.2 已创建的爬虫项目目录
### 
    baidu
      |——baidu_spider.py
      |——bmodel.py
      |——settings.py
---
* baidu_spider.py 生成代码如下：
###
    from pathlib import Path
    from sniper import Crawl
    from sniper import get_params
    from settings import *


    class BaiduSpider(Crawl):
        spider_name = 'your_spider_name'
    
        def __init__(self, **kwargs):
            """
            配置爬虫所需参数：
            name='your_spider_name' # csv文件名， 必要参数,
            CACHE_PATH=CACHE_PATH # 缓存路径, 必要参数,
            ROOT_PATH=ROOT_PATH # 项目根目录, 必要参数,
            """
            super().__init__(**kwargs)
    
        def start_request(self):
            """
            请替换自己项目的URL
            :return: Iterator
            """
            url = 'https://www.baidu.com'
            yield url, COOKIES, HEADERS, PARAMS, JSON_DATA
    
        def html_pars(self, response=None) -> list:
            """
            返回列表形式：[{str, str},{str, str}]
            :param response: response
            :return: list
            """
            data = [{}]
            return data
    
        if __name__ == '__main__':
            BaiduSpider(name='your_spider_name',
                        BASE=base,
                        CACHE_PATH=CACHE_PATH,
                        ROOT_PATH=ROOT_PATH).save()
---
* model.py 生成代码如下：
###
    from sniper import base
    from sqlalchemy import Column, Integer, String, ForeignKey, Text, BigInteger, DATETIME, Float


    class BaiduModel(base.Base):
        """
        请按照爬取字段设置模型字段
        """
        __tablename__ = 'baidu'
        id = Column(Integer, primary_key=True)
    
    
    if __name__ == '__main__':
        BaiduModel.metadata.create_all(base.base_engin)

* 此处需要填写爬虫所需保存的所有字段，该字段与数据库和csv字段相同。
---
* settings.py 生成代码如下：

###
    import os
    from pathlib import Path
    from sniper.database.model import BaseConfig

    # 设置cookies
    COOKIES = {}
    
    # 设置headers
    HEADERS = {}
    
    # 设置get请求的params参数
    PARAMS = {}
    
    # 设置post请求的JSON_DATA参数
    JSON_DATA = {}
    
    # 用户并发数量设置
    CUSTOMER_CURRENT = 32
    
    # 设置缓存路径
    ROOT_PATH = Path(__file__).parent.parent
    CACHE_PATH = ROOT_PATH / 'cache'
    if not CACHE_PATH.exists():
        CACHE_PATH.mkdir()
        os.system(f'idea . --add-excluded {CACHE_PATH}')
    
    # 设置csv路径
    CSV_PATH = ROOT_PATH / 'csv'
    if not CSV_PATH.exists():
        CSV_PATH.mkdir()
        CSV_PATH = str(CSV_PATH.resolve())
    
    # 数据库配置项
    DATABASE = {
        'sqlite': 'data.db'
    }
    
    base = BaseConfig(DATABASE=DATABASE)

* 此处需要设置root_path等路径及数据库配置信息（暂时仅支持MySQL与sqlite数据库）
---
### 3.1.3 批量执行爬虫操作

###
    orm = ORM(model=YourSpiderModel)
    query_set = orm.get_query_set(model=YourSpiderModel)
    kwargs_list = [{'keyword1': item['keyword1'],
                    'keyword2': item['keyword2'],
                    'CACHE_PATH': CACHE_PATH,
                    'ROOT_PATH': ROOT_PATH,
                    } for item in query_set]
    TaskList(spider=YourSpider, query_set=kwargs_list).put_task(cache_path=CACHE_PATH)
    TaskList(spider=YourSpider, query_set=kwargs_list).task_run(cache_path=CACHE_PATH)
---
* 此处TaskList类中包含两种执行方式：
*** 
    A：put_task 使用队列进行爬取
    B：task_run 不使用队列进行爬取

    其中B的执行速度是A的五倍，但是此处需要消耗大量计算机性能，此处需根据自己计算机硬件配置进行选择。
    该模块使用需对爬虫模块编写完成，方可执行此处方法，此处执行不限于一个爬虫类，可多个类同时执行。
    方法内均提供保存到csv文件和SQL文件方法，不同之处在于所需参数不同。
    将任务列表添加到任务列表中
---
* 以下为该方法参数列表：
***   
    :param model: object
    :param cache_path: str
    :param BASE: object
    :param max_number: int=32
    :param csv_path: str
---
## 3.2 缓存机制
    项目缓存路径为根目录向cache文件夹，根据对应爬虫创建缓存目录
    缓存格式为feather格式
    为减少不必要的访问请求，保存为csv文件和SQL数据库时均采用从缓存读取并保存到指定路径内。
## 3.3爬虫执行
    项目执行爬虫是分为两种执行方式：
    A： 单独执行爬虫
        次方访在Spider文件中右键执行就可以执行单个爬虫项目，所有关于爬虫的解析与参数配置均在
    次模块中完成。
    以下为东方财富网获取股票代码及名称爬虫文件
*** 
    class KlineSpider(Crawl):
    spider_name = 'kline'


    def __init__(self,**kwargs):
        """
        配置爬虫所需参数：
        name='603516' # csv文件名， 必要参数,
        CACHE_PATH=CACHE_PATH # 缓存路径, 必要参数,
        ROOT_PATH=ROOT_PATH # 项目根目录, 必要参数,
        """
        super().__init__(**kwargs)
        secid = kwargs.get('secid')
        if secid[0] == '6':
            self.secid ='1.' + secid
        elif secid[0] == '0':
            self.secid = '0.' + secid
        elif secid[0] == '3':
            self.secid = '0.' + secid


    def start_request(self):
        """
        请替换自己项目的URL
        :return: Iterator
        """
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        url_ = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=0.002323&klt=101&fqt=1&cb=jsonp1733501557389'
        params = get_params(url_str=url_)
        params['secid'] = self.secid
        yield url, COOKIES, HEADERS, params, JSON_DATA

    def html_pars(self, resp=None) -> list:
        """
        返回列表形式：[{str, str},{str, str}]
        :param resp: response
        :return: list
        """
        data = []
        # print(resp.url)
        info = re.findall(r'jsonp\d+\((.*)\)', resp.text)
        if info:
            kline_list = json.loads(info[0]).get('data').get('klines')
            for kline in kline_list:
                k_info = kline.split(',')
                if k_info:
                    secid = get_params(resp.url).get('secid')
                    data.append({
                        'secid': secid[2:],
                        'day': k_info[0],
                        'open': k_info[1],
                        'close': k_info[2],
                        'high': k_info[3],
                        'low': k_info[4],
                        'cheng_jiao_liang': k_info[5],
                        'cheng_jiao_e': k_info[6],
                        'zhen_fu': k_info[7]+'%',
                        'zhang_die_fu': k_info[8]+'%',
                        'zhang_die_e': k_info[9],
                        'huan_shou_lv': k_info[10]+'%',
                    })
        return data
    if __name__ == '__main__':
        kline_ = KlineSpider(secid='603516',
                             name='603516',
                             CACHE_PATH=CACHE_PATH,
                             ROOT_PATH=ROOT_PATH)
        kline_.save_to_csv(model=KlineModel)
---
    右键执行便可获取到东方财富A股代码及名称数据，此处可通过爬虫对象调取相应方法实现保存到csv文件或数据库操作
---
    B:批量执行爬虫
        项目中批量执行爬虫通过模块提供的执行器进行多进程执行爬虫，此处可执行多个不同爬虫项目
    下图为东方财富批量执行示例代码：
***
    class EastMoney:

        def __init__(self):
            EastmoneySpider(pn_size=284,
                            name='code',
                            CACHE_PATH=CACHE_PATH,
                            ROOT_PATH=ROOT_PATH,).save_to_sql(model=EastmoneyModel)

        def kline(self):
            orm = ORM(model=EastmoneyModel)
            query_set = orm.get_query_set(model=EastmoneyModel)
            kwargs_list = [{'secid': item['code'],
                            'name': item['code'],
                            'CACHE_PATH': CACHE_PATH,
                            'ROOT_PATH': ROOT_PATH,
                            } for item in query_set]
            TaskList(spider=KlineSpider, query_set=kwargs_list).put_task(cache_path=CACHE_PATH)
            # TaskList(spider=KlineSpider, query_set=kwargs_list).task_run(cache_path=CACHE_PATH)

    if __name__ == '__main__':
        start = time.time()
        EastMoney().kline()
        end = time.time()
        print(end - start)