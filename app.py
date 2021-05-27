#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database_tools, file_tools, matching_tools
import sys

paths = sys.argv[1:]

setting = database_tools.get_props('config/sql_settings.json')
engine = database_tools.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database_tools.select_vendors(engine)


for path in paths:
    md5 = file_tools.get_file_md5(path)
    folder = file_tools.unpack_firmware(path)
    may_model_info, flags = matching_tools.find_models_info_by_firmware(folder, engine)
    print('Search result: {}'.format(may_model_info))
    print('result flags: {}'.format(flags))
    file_tools.remove_file()
