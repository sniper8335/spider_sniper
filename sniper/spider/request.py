from sniper.request import Request
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed
from urllib.parse import urlencode
from sniper.config import CUSTOMER_CURRENT, COOKIES, PARAMS
import time


class Spider:
    """
    整理发送请求数据，模块判断发送get或者post请求
    """
    spider_name = 'spider'
    verify = True
    proxy = None
    wait_time = 0

    def __init__(self):
        self.request = Request(verify=self.verify)
        self.name = self.spider_name

    def url_(self):
        """
        组装请求数据
        :return: iterator
        自动生成请求数据的迭代器
        """
        for url, cookies, headers, params, json_data in self.start_request():
            yield url, cookies, headers, params, json_data


    def response(self, max_req=CUSTOMER_CURRENT):
        """
        多线程发送请求
        :return: iterator
        """
        with ThreadPoolExecutor(max_workers=max_req) as tp:
            for result in as_completed([tp.submit(self.request_,
                                                  url=url,
                                                  cookies=cookies,
                                                  params=params,
                                                  headers=headers,
                                                  json_data=json_data,
                                                  ) for url, cookies, headers, params, json_data in
                                        self.url_()]):
                yield result.result()


    def request_(self, **kwargs):
        """
        获取响应数据
        :param kwargs: json_data,cookies,headers,params
        :return: response
        post请求为判断是否为json数据，是则post请求，否则get请求
        """
        if kwargs.get('json_data'):
            url = kwargs.get('url')
            cookies = kwargs.get('cookies')
            COOKIES_ = {**COOKIES, **cookies}
            headers = kwargs.get('headers')
            HEADERS_ = {**self.request.headers, **headers}
            json_data = kwargs.get('json_data')
            response = self.request.post_(url=url, headers=HEADERS_, json_data=json_data, **COOKIES_)
            time.sleep(self.wait_time)
            return response
        else:
            url = kwargs.get('url') + '?' + urlencode({**PARAMS, **kwargs.get('params')})
            cookies = kwargs.get('cookies')
            COOKIES_ = {**COOKIES, **cookies}
            headers = kwargs.get('headers')
            HEADERS_ = {**self.request.headers, **headers}
            verify = kwargs.get('verify')
            response = self.request.get_(url=url, headers=HEADERS_, verify=verify, **COOKIES_)
            time.sleep(self.wait_time)
            return response

    def start_request(self):
        """
        此方法许重写并组装请求所需参数
        url = str https://www.xxx.com
        cookies = {}
        headers = {}
        params = {}
        json_data = {}
        :return: iterator
        """
        pass
