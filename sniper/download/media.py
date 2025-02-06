import requests
from concurrent.futures import ThreadPoolExecutor


class Down:
    """
    数据下载类
    """

    def __init__(self,
                 path: str = None,
                 verify: bool = True,
                 max_num: int = 32) -> None:
        """
        :param path: 保存路径
        :param verify: 是否验证ssl
        :param max_num: 最大线程数
        :return: None
        """
        self.path = path
        self.verify = verify
        self.max_num = max_num

    def request(self,
                info: dict = None,
                headers: dict = None,
                cookies: dict = None,
                file: str = None,
                method: str = None) -> None:
        """
        :param info: 信息
        :param headers: 请求头
        :param cookies: cookie
        :param file: 文件路径
        :param method: 请求方法
        :return: None
        需传入保存数据的下载路径， 函数发送请求并获取二进制数据并保存
        """
        title = info.get('title')
        url = info.get('url')
        filename = file + title + '.pdf'
        if method == 'get':
            response = requests.get(url=url, headers=headers, cookies=cookies, verify=self.verify).content
            if response:
                self.save(content=response, filename=filename)
        elif method == 'post':
            response = requests.post(url=url, headers=headers, cookies=cookies, verify=self.verify).content
            if response:
                self.save(content=response, filename=filename)

    def save(self, content=None, filename: str = None):
        """
        :param content: 二进制数据
        :param filename: 文件名
        """
        with open(filename, 'wb') as f:
            f.write(content)
            print(filename, '已保存')

    def down(self,
             info: list[dict] = None,
             cookies: dict = None,
             headers: dict = None,
             file: str = None,
             method:str = None) -> None:
        """
        :param info: 数据
        :param cookies: cookie
        :param headers: 请求头
        :param file: 文件路径
        :param method: 请求方法
        :return: None
        多进程文件下载
        """
        with ThreadPoolExecutor(max_workers=self.max_num) as tp:
            for data in info:
                tp.submit(self.request,
                          info=data,
                          headers=headers,
                          cookies=cookies,
                          file=file,
                          method=method)
