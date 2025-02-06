
class Loader:
    """
    爬虫加载器，加载实例化爬虫对象
    """
    def __init__(self, spider: object = None):
        self.spider = spider
        self.res = {'code': 200, 'msg': ''}

    def load_spider(self):
        """
        加载实例化爬虫对象和状态码
        :return: spider
        """
        spider_name = self.spider.name
        if spider_name:
            self.res['msg'] = spider_name
            spider = self.spider
            return self.res, spider
        else:
            self.res['msg'] = '未找到spider'
            self.res['code'] = 400
            return self.res, None

    def export_spider(self):
        """
        返回爬虫名称和实例化爬虫对象
        :return: spider
        """
        res, spider = self.load_spider()
        if res.get('code') == 200:
            return res, spider
        else:
            return res, None
