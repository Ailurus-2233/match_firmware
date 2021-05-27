#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database_tools, file_tools, matching_tools, log_tools
import sys

paths = sys.argv[1:]

setting = database_tools.get_props('config/sql_settings.json')
engine = database_tools.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database_tools.select_vendors(engine)


for path in paths:
    md5 = file_tools.get_file_md5(path)
    folder = file_tools.unpack_firmware(path)
    result = matching_tools.find_models_info_by_firmware(folder, engine, path.split("/")[-1])
    print('Search result: {}'.format(result['may_models_info']))
    print('result flags: {}'.format(result['flags']))
    log_tools.make_a_log('log', result, folder)

    file_tools.remove_file()
