import requests
import urllib3
from fake_useragent import UserAgent
from sniper.config import *


class Request:
    def __init__(self, verify: bool = True, proxy: dict = None):
        """
        发送请求类
        """
        self.headers = HEADERS
        self.cookies = COOKIES
        self.user_agent = UserAgent().random
        self.verify = verify
        self.proxy = proxy

    def get_(self, url: str = None, headers: dict = None, **kwargs):
        """
        get 请求
        :param headers:
        :param url: str = url+ ? + urlencoded(params)
        :param kwargs: cookies = dict{}
        :return: response
        """
        if kwargs:
            self.cookies = kwargs
        self.headers['UserAgent'] = self.user_agent
        headers_ = {**self.headers, **headers}
        response = requests.get(url=url, headers=headers_, cookies=self.cookies, verify=self.verify, proxies=self.proxy)
        return response

    def post_(self, url: str = None, json_data: dict = None, headers: dict = None, **kwargs):
        """
        post 请求
        :param headers:
        :param url: str https://www.xxx.com
        :param json_data: dict = {}
        :param kwargs: cookies
        :return: response
        """
        if kwargs:
            self.cookies = kwargs
        if json_data:
            data = json_data
        else:
            data = JSON_DATA
        self.headers['UserAgent'] = self.user_agent
        headers_ = {**self.headers, **headers}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(url=url, headers=headers_, data=data, cookies=self.cookies, verify=self.verify, proxies=self.proxy)
        return response
