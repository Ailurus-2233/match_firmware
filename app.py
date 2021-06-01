#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database, vendor_match
import sys
import os

# path为父文件夹
path = sys.argv[1]
files = os.listdir(path)

setting = database.get_props('config/sql_settings.json')
engine = database.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database.select_vendors(engine)

index = 0
for f in files:
    if f.find('.bin') != -1:
        index += 1
        if index != 1:
            continue
        position = path+f
        vendor_match.match_file(position, engine)
