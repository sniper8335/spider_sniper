from pathlib import Path

# 项目根路径
BASE_DIR = Path(__file__).parent.parent

# 项目数据路径
DATA_DIR = BASE_DIR / 'database'

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


# 解析params类
class PARAMS_:
    """
    params参数解析
    对URL字符串进行拆解， 返回字典格式数据， 添加参数，并返回encode后的URL链接数据
    """

    def __init__(self, url_str: str = None):
        """
        初始化参数
        :param url_str: str
        :return: None
        传入URL字符串
        """
        self.url_str = url_str

    def params(self) -> dict:
        """
        拆解params参数
        :return: dict
        传入URL字符串，对字符串进行分割，返回字典格式数据
        """
        params_str = self.url_str.split('?')[-1].split('&')
        params = {}
        for info in params_str:
            params[info.split('=')[0]] = info.split('=')[-1]
        return params
