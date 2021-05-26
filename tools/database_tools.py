import pandas as pd
from sqlalchemy import create_engine
import json


# 从settings文件中获取配置信息
def get_props(filename):
    with open(filename, 'r') as file:
        dirt = json.loads(file.read())
    return dirt


# 创建数据库链接
def create_mysql_engine(user, passwd, host, port, database):
    return create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user, passwd, host, port, database))


# 执行有返回的数据库指令 如查询操作 这里返回的是pandas的存储格式
def run_sql(sql_query, engine):
    return pd.read_sql_query(sql_query, engine)


# 单列数据库查询结果转为数组的操作
def analysis_req(req):
    req = req.to_dict()
    for key in req.keys():
        req[key] = req[key][0]
    return json.dumps(req)


# 从数据库中 获取所有的公司名称
def get_companies(engine):
    companies_temp = run_sql("select distinct company from list", engine)
    companies = []
    for i in companies_temp.values:
        companies.append(i[0])
    return companies


# 在数据库中 获取该公司的所有设备名称
def get_versions_by_company(engine, company):
    version_temp = run_sql("select distinct version from list where company like '{}'".format(company), engine)
    versions = []
    for i in version_temp.values:
        versions.append(i[0])
    return versions
