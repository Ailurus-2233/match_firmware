#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database, match
import sys
# import os

# path为bin文件路径
path = sys.argv[1]

setting = database.get_props('config/sql_settings.json')
engine = database.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database.select_vendors(engine)

match.match_file_nodb(path, engine)
