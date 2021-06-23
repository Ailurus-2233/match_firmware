# %%
from tools import database, file, log, match, name
import os
import re

# %%
path = "/mnt/e/20210621/360/"
files = os.listdir(path)

# %%
data = []
for f in files:
    data.append(name.for_360(f, path))

# %%
user = "test"
passwd = "1234"
host = "localhost"
port = "3306"
db = "testDB"

engine = database.create_mysql_engine(user, passwd, host, port, db)

#%%
for d in data:
    database.insert_info(engine, d)

# %%
sql = "select id from firmwares where firmware_md5 = '{}'".format("216f616f7b66c20cec07d7b1cf7613e9")
req = database.run_sql(sql, engine)
req.values[0][0]
# %%
file.get_file_md5("/mnt/e/20210621/acer/Acer_E200_G1Router_update_package.rar")

# %%
