#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database, match
import os

# path为bin文件夹路径
path = "/home/wzy/firmware/bins/"
files = os.listdir(path)

setting = database.get_props('config/sql_settings.json')
engine = database.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database.select_vendors(engine)

for f in files:
    position = path+f
    try:
        match.match_file_nodb(position, engine)
    except IndexError:
        print('unpack error')
