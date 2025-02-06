import os.path
import time

import pandas
import openpyxl


class SaveData:
    """
    数据保存
    """

    def __init__(self, path):
        """
        初始化path路径
        : param path: str
        : return: None
        """
        self.path = path

    def to_dataframe(self, info: list[dict] = None) -> pandas.DataFrame:
        """
        将列表数据转换为dataframe类型数据
        :param info: list
        :return: dataframe
        """
        dataframe = pandas.DataFrame(data=info, columns=list(info[0].keys()))
        return dataframe

    def df_to_csv(self, info: list[dict] = None) -> None:
        """
        保存到csv文件
        :param info: list
        :return: None
        """
        dataframe = self.to_dataframe(info=info)
        dataframe.to_csv(f'{self.path}.csv', encoding='utf-8-sig')

    def to_media(self, info=dict):
        """
        : param info: dict
        : return: None
        保存pdf文件到指定路径
        """
        file_name = f'{os.path.join(self.path, info.get("title"))}.pdf'
        with open(file_name, 'wb') as f:
            f.write(info.get('content'))
            print(info.get('title'), '已保存')

    def cache(self, info: list[dict] = None, spider_name:str=None) -> None:
        """
        缓存数据到文件
        :param info: list[dict]
        :param spider_name: str
        :return: None
        """
        dataframe = self.to_dataframe(info=info)
        dataframe.to_feather(f'{self.path}_{spider_name}.feather')
