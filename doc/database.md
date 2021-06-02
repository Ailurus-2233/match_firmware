# Database

数据库操作相关的工具包



## get_props(filename)

描述： 从settings文件中获取配置信息

输入：

```
filename: settings的路径，字符串类型
```

输出：

```
字典类型，记录创建数据库链接的各种参数
```



## create_mysql_engine(user, passwd, host, port, database)

描述：创建sqlalchemy数据库引擎

输入：

```
user: 数据库用户名
passwd: 数据库密码
host: 数据库地址
port: 数据库端口
database: 待链接的数据库
```

输出：

```
sqlalchemy数据库引擎
```



##  run_sql(sql_query, engine)

描述：执行一条有返回的数据库指令，返回的数据使用pandas的存储格式记录

输入：

```
sql_query: 数据库执行指令
engine: sqlalchemy数据库引擎
```



## select_vendors(engine)

描述：获取所有的vendor信息

输入：

```
engine: sqlalchemy数据库引擎
```

输出：

```
list类型，记录所有的vendor信息
```



## select_models_by_vendor(engine, vendor)

描述：获取该vendor下所有的model信息

输入：

```
engine: sqlalchemy数据库引擎
vendor: 带查询的vendor，字符串类型
```

输出：

```
list类型，记录所有的model信息
```



## insert_firmware_md5(engine, firmware_name, firmware_md5, firmware_version)

描述：将固件信息插入到固件表（firmwares）

输入：

```
engine: sqlalchemy数据库引擎
firmware_name: 固件文件名称，字符串类型
firmware_md5: 固件的md5，字符串类型
firmware_version: 固件的版本号，字符串类型
```



## insert_device(engine, vendor, device)

描述：将设备信息插入到设备表中(devices)

输入：

```
engine: sqlalchemy数据库引擎
vendor: 公司名称，字符串类型
device: 设备名称，字符串类型
```



## insert_firmware_device_rel(engine, firmware_id, device_id, is_name_match)

描述：插入匹配的固件和设备关系记录（firmware_to_device）

输入：

```
engine: sqlalchemy数据库引擎
firmware_id: 数据库中记录的固件id
device_id: 数据库中记录的设备id
is_name_match: 是否采用了名称匹配，bool类型
```



## insert_firmware_device_two(engine, firmware_md5, vendor, device, is_name_match)

描述：插入厂商和型号均匹配的设备信息，同时插入固件和设备关系记录

输入：

```
engine: sqlalchemy数据库引擎
firmware_md5: 固件的md5，字符串类型
vendor: 公司名称，字符串类型
device: 设备名称，字符串类型
is_name_match: 是否采用了名称匹配，bool类型
```

