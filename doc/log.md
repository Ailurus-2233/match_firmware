# Log

关于日志操作的工具包



## init_log_folder(log_folder)

描述：初始化log文件夹

输入：

```
log_folder: log文件夹位置，字符串类型
```



##  make_a_log(log_folder, result, files_folder)

描述： 将一次查询结果记录到对应的log文件中

输入：

```
log_folder: log文件夹位置，字符串类型
result: match工具中，find_models_info_by_firmware执行返回的结果
files_folder: bin文件解包路径，字符串类型
```



## log_one_vendor_one_model(may_models_info, log_folder, files_folder, file_name, flags)

描述：将匹配为一个公司，一个设备型号的结果，记录到log文件中，生成的文件名为

`{vendor}_{model}_{file-name}.log`

输入：

```
may_models_info: 字典类型，记录着查询结果
log_folder: log文件夹位置，字符串类型
files_folder: bin文件解包路径，字符串类型
file_name: 固件文件名
flags: 查询结果种类的标识，主要是为了用是否判断使用过名称匹配
```



## log_one_vendor_more_model(may_models_info, log_folder, files_folder, file_name)

描述：将匹配为一个公司，多个设备型号的结果，记录到log文件中，生成的文件名为

`{vendor}_moreModels_{file-name}.log`

输入：

```
may_models_info: 字典类型，记录着查询结果
log_folder: log文件夹位置，字符串类型
files_folder: bin文件解包路径，字符串类型
file_name: 固件文件名
```



## log_one_vendor_no_model(may_models_info, log_folder, files_folder, file_name)

描述：将匹配为一个公司，多个设备型号的结果，记录到log文件中，生成的文件名为

`{vendor}_noModel_{file-name}.log`

输入：

```
may_models_info: 字典类型，记录着查询结果
log_folder: log文件夹位置，字符串类型
files_folder: bin文件解包路径，字符串类型
file_name: 固件文件名
```



## log_more_vendor(may_models_info, log_folder, files_folder, file_name)

描述：将匹配为多个公司的结果，记录到log文件中，生成的文件名为

`moreVendors_{file-name}.log`

输入：

```
may_models_info: 字典类型，记录着查询结果
log_folder: log文件夹位置，字符串类型
files_folder: bin文件解包路径，字符串类型
file_name: 固件文件名
```



## log_no_match(file_name)

描述：将无匹配的结果，统一将其文件名记录到`noMatch.log`中

输入：

```
file_name: 固件文件名
```



## log_info(infos, log_file, files_folder, info_type)

描述：将`gerp`结果存入对应的log文件

输入：

```
infos: 带匹配信息的列表
log_file: log文件位置，字符串类型
files_folder: bin文件解包路径，字符串类型
info_type: 带匹配信息的类型
```

