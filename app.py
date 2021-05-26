#!/usr/bin/python
# -*- coding: utf-8 -*-

from tools.database_tools import get_props, create_mysql_engine, get_companies
from tools.file_tools import get_file_md5, unpack_firmware, remove_file
from tools.find_tools import find_firmware, last_matching
import sys

paths = sys.argv[1:]

setting = get_props('config/sql_settings.json')
engine = create_mysql_engine(setting['user'], setting['password'], setting['host'], setting['port'], setting['database'])
companies = get_companies(engine)


for path in paths:
    md5 = get_file_md5(path)
    folder = unpack_firmware(path)
    may_firmwares = find_firmware(companies, folder, engine)
    firmwares = last_matching(may_firmwares, engine)
    if (len(firmwares)) > 0:
        print("The firmware matched from the database as as follows:")
        for firmware in firmwares:
            print(firmware)
    else:
        print("No matching file was found in the database")
    remove_file()
