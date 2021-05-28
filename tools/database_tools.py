import pandas as pd
from sqlalchemy import create_engine
import json
import traceback


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


# 新增固件MD5，没有返回值
def insert_firmware_md5(engine, firmware_name,firmware_md5,firmware_version):
    try :
        # 去除字符串两侧空格
        firmware_name = firmware_name.strip()
        firmware_md5 = firmware_md5.strip()
        firmware_version = firmware_version.strip()           
        if len(firmware_name) < 1 : # firmware_name不能为空字符串
            print("firmware_name could not be null")
        elif len(firmware_md5) < 1 :# firmware_md5不能为空字符串
            print("firmware_md5 could not be null")
        else :
            # 查询MD5 是否已存在
            select_md5 = "select firmware_md5 from firmwares where firmware_md5='{}'".format(firmware_md5)
            exist_md5 = run_sql(select_md5, engine)
            if len(exist_md5.values) == 0 : # MD5不存在
                if len(firmware_version) > 0 : # 版本号不为空
                    insert_firmware =  "insert into firmwares (firmware_name,firmware_md5,version) values ( '{}', '{}', '{}')".format(firmware_name,firmware_md5,firmware_version)
                else :
                    insert_firmware =  "insert into firmwares (firmware_name,firmware_md5) values ( '{}', '{}')".format(firmware_name,firmware_md5)
                engine.execute(insert_firmware)
            else :
                print("md5 has exist")
    except :
        print('wrong---',insert_firmware)
        # 记入db log
        #traceback.print_exc()


# 新增匹配设备，没有返回值
def insert_device(engine, vendor,device):    
    try :
        vendor = vendor.strip()
        device = device.strip()        
        if len(vendor) < 1 : # vendor不能为空字符串
            print("vendor could not be null")
        elif len(device) < 1 :# device不能为空字符串
            print("device could not be null")
        else :
            # 查询vendor,device 是否已存在
            select_device = "select device from devices where vendor='{}' and device='{}'".format(vendor,device)
            exist_device = run_sql(select_device, engine)
            if len(exist_device.values) == 0 : # device不存在
                insert_dev =  "insert into devices (vendor,device) values ( '{}', '{}')".format(vendor,device)
                engine.execute(insert_dev)
            else :
                print("device has exist")
    except :
            print('wrong---',vendor,',   ',device)
            # 记入db log
            #traceback.print_exc()


# 新增匹配的固件和设备，没有返回值
def insert_firmware_device(engine,firmware_id,device_id,is_name_match):    
    try :   
        if firmware_id is None or firmware_id < 1 : # firmware_id应大于1
            print("firmware_id should be bigger than one")
        elif device_id is None or device_id < 1 :# device_id应大于1
            print("device_id should be bigger than one")
        else :
            if is_name_match is None or is_name_match !=1 :
                is_name_match = 0
            # 查询firmware_id,device_id 是否已存在
            select_firm_dev = "select firmware_id from firmware_device where firmware_id={} and device_id={}".format(firmware_id,device_id)
            exist_firm_dev = run_sql(select_firm_dev, engine)
            if len(exist_firm_dev.values) == 0 : # device不存在
                insert_firm_dev =  "insert into firmware_device (firmware_id,device_id,is_name_match) values ( {}, {}, {})".format(firmware_id,device_id,is_name_match)
                engine.execute(insert_firm_dev)
            else :
                print("firmware_id & device_id  has exist   ",firmware_id,',   ',device_id)
    except :
            print('wrong---',firmware_id,',   ',device_id)
            # 记入db log
            #traceback.print_exc()