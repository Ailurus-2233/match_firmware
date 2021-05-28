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


# 从数据库中 获取所有的公司名称
def select_vendors(engine):
    vendors_temp = run_sql("select distinct vendor from list_tmp", engine)
    vendors = []
    for i in vendors_temp.values:
        vendors.append(i[0])
    return vendors


# 在数据库中 获取该公司的所有设备名称
def select_models_by_vendor(engine, vendor):
    model_temp = run_sql("select distinct productModel from list_tmp where vendor like '{}'".format(vendor), engine)
    models = []
    for i in model_temp.values:
        models.append(i[0])
    return models
