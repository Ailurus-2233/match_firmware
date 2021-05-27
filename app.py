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
    may_model_info = matching_tools.find_models_info_by_firmware(vendors, folder, engine)
    # if (len(models_info)) > 0:
    #     print("The firmware matched from the database as as follows:")
    #     for model in models_info:
    #         print(model)
    # else:
    #     print("No matching file was found in the database")
    print(may_model_info)
    file_tools.remove_file()
