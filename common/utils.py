import exrex
from string import Template
from common.context import Context
from common.logger import logger
from common.mysql_data import MySqlData


class BaseUtils:

    def __init__(self):
        self.db_conf = getattr(Context, "ENV")["mysql"]
        host = self.db_conf["host"]
        port = self.db_conf["port"]
        user = self.db_conf["user"]
        pwd = self.db_conf["password"]
        self.db = MySqlData(host, user, pwd, port=port)

    def data_generator(self, pattern, sql):
        """
        数据生成器
        :param pattern: 正则表达式,用来生成符合该规则的数据
        :param sql: 用于判断生成数据是否唯一的sql
        :return:
        """
        while True:
            value = exrex.getone(pattern)
            sql = Template(sql).substitute(**self.__dict__)
            sql = sql.format(value)
            if not self.db.single_execute(sql):
                break
        logger.info("生成的数据为 ---->---> {}".format(value))
        return value


class IndiaUtils(BaseUtils):

    def __init__(self):
        super().__init__()
        self.region = self.db_conf["region"]
        self.sql_env = self.db_conf["sql_env"]

    def get_account(self):
        pattern = r"136\d{8}"
        sql = "SELECT id FROM ${region}_appbackend_${sql_env}.v_codes where phone = '{}' order by id desc;"
        phone = self.data_generator(pattern, sql)
        return phone

    def get_code(self, cellphone):
        sql = f"select v_code from {self.region}_appbackend_{self.sql_env}.v_codes where phone = '{cellphone}' " \
              "order by id desc limit 1;"
        return self.db.find_one(sql)[0]

