#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools import database, file, match, log
import sys

paths = sys.argv[1:]

setting = database.get_props('config/sql_settings.json')
engine = database.create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
vendors = database.select_vendors(engine)


for path in paths:
    md5 = file.get_file_md5(path)
    folder = file.unpack_firmware(path)
    result = match.find_models_info_by_firmware(folder, engine, path.split("/")[-1])
    print('Search result: {}'.format(result['may_models_info']))
    print('result flags: {}'.format(result['flags']))
    log.make_a_log('log', result, folder)

    file.remove_file()
