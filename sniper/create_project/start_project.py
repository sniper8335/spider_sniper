from datetime import datetime
from sniper.database import base, System, ORM
from sniper.config.settings import BASE_DIR
from pathlib import Path

System.metadata.create_all(base.base_engin)


class Create:
    """
    项目创建类
    创建爬虫项目，需要输入项目名称和URL，此处项目名称为爬虫的名称
    """

    def __init__(self, BASE=None):
        """
        初始化类，需要传入数据库配置信息
        params: BASE: 数据库配置信息
        returns: None
        此处创建爬虫项目为自动创建，无需手动创建
        *** 注意：
            1. 项目名称为爬虫的名称，如：东方财富网
            2. 项目名称为项目文件夹名称，如：东方财富网
            3. 项目名称为英文格式
            4. URL不需要携带http://，如：www.eastmoney.com，系统默认为https格式
        """
        self.template_path = Path(f'{BASE_DIR}/template').stat()
        self.project_path = BASE_DIR.parent
        self.base = BASE

    def input_project_info(self):
        """
        手动输入项目信息， 包括项目名称和URL
        """
        project_name = input('请输入项目名称：')
        url = input('请输入项目URL：')
        Project_name = project_name.capitalize()
        return project_name, Project_name, url

    def create_project(self):
        """
        创建项目，通过模版文件创建项目文件夹，创建爬虫文件，创建模型文件，创建配置文件
        """
        project_name, Project_name, url = self.input_project_info()
        if Path(f'{self.project_path}/{project_name}').exists():
            self.create_spider(project_name=project_name, Project_name=Project_name, url=url)
            self.create_model(project_name=project_name, Project_name=Project_name)
            self.create_settings(project_name=project_name)
        else:
            Path(f'{self.project_path}/{project_name}').mkdir()
            self.create_spider(project_name=project_name, Project_name=Project_name, url=url)
            self.create_model(project_name=project_name, Project_name=Project_name)
            self.create_settings(project_name=project_name)

    def create_spider(self, **kwargs):
        """
        通过模版文件创建爬虫文件
        params: project_name: 项目名称
        项目名称（spider_name）为必要参数
        """
        with open(f'{BASE_DIR}/template/spider.tmpl', 'r', encoding='utf-8') as file:
            new_spider = file.read().replace('$project_name',
                                             kwargs.get('project_name')).replace('${ProjectName}',
                                             kwargs.get('Project_name')).replace('$url', kwargs.get('url'))
        with open(Path(f"{self.project_path}/{kwargs.get('project_name')}/{kwargs.get('project_name')}_spider.py"), 'w',
                  encoding='utf-8') as file:
            file.write(new_spider)
        orm = ORM(model=System, BASE=self.base)
        orm.update_or_create(project_name=kwargs.get('project_name'),
                             create_time=datetime.now())

    def create_model(self, **kwargs):
        """
        通过模版文件创建模型文件
        params: project_name: 项目名称
        项目名称（spider_name）为必要参数
        """
        with open(f"{BASE_DIR}/template/model.tmpl", 'r', encoding='utf-8') as file:
            new_spider = file.read().replace('$project_name',
                                             kwargs.get('project_name')).replace('${ProjectName}',
                                             kwargs.get('Project_name'))
        with open(Path(f"{self.project_path}/{kwargs.get('project_name')}/model.py"), 'w', encoding='utf-8') as file:
            file.write(new_spider)

    def create_settings(self, **kwargs):
        """
        通过模版文件创建配置文件
        params: project_name: 项目名称
        项目名称（spider_name）为必要参数
        """
        with open(f"{BASE_DIR}/template/settings.tmpl", 'r', encoding='utf-8') as file:
            new_spider = file.read()
        with open(Path(f"{self.project_path}/{kwargs.get('project_name')}/settings.py"), 'w', encoding='utf-8') as file:
            file.write(new_spider)
