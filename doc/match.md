# Match

主要用来匹配查找固件中对应的信息的工具包

## is_in_word(req, vendor)

描述：在grep的过程中，会将单词内部匹配的字符返回出来，这个函数是为了将这种情况识别出来

输入参数：
```
req：grep返回的的结果，该参数是os.popen(cmd)返回类型
vendor：待比较的公司名称，字符串类型
```
输出结果：
```
bool类型
如果所有的结果都是在单词中的话，则为True
至少有一个结果不在单词中，则为False
```

## is_exist_vendor(folder_name, vendor_name)

描述：判断这个解压出来的文件，是否是属于该公司的产品的，判断方式是通过grep查找这个文件夹下是否有该公司名称，有则认为该固件是从该公司的产品中提取出来的。

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
vendor_name：待匹配的公司名称，字符串类型
```

输出结果：
```
bool 类型
如果认为该固件属于该公司产品，则为True
否则，则为False
```

## is_exist_model(folder_name, model_name)
描述：判断这个解压出来的文件，是否是属于该型号的设备，判断方式是通过grep查找这个文件夹下是否有该公司名称，有则认为该固件是从该型号的设备中提取出来的。

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
model_name：待匹配的型号名称，字符串类型
```

输出结果：
```
bool 类型
如果认为该固件属于该型号的设备，则为True
否则，则为False
```

## find_exist_vendors(folder_name, vendors)

描述：判断这个解压出来的文件，是否是属于那些公司的设备的，判断是基于is_exist_vendor()该函数实现的。

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
vendors：待匹配的公司名称，字符串列表
```

输出结果：
```
字符串列表
记录所有的匹配到的公司名称
```

## find_exist_models_by_vendor(folder_name, models, vendor)

描述：判断这个解压出来的文件，是否是属于特定公司的那些型号的设备，判断是基于is_exist_model()该函数实现的。

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
vendor：公司名称，字符串
models：待匹配型号，字符串列表
```

输出结果：
```
字符串列表类型
记录所有的匹配到的型号名称
```

## find_all_models(folder_name, may_vendors, engine)

描述：基于find_exist_models_by_vendor()函数，对所有出现的公司，查找所有的匹配型号

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
may_vendors：所有匹配的公司，函数find_exist_vendors()返回的列表
engine：数据库引擎
```

输出结果：
```
字典类型
匹配到的公司与匹配型号对应的型号信息
{vendor:[models]}
```

## extra_models_match(folder_name, models)
描述：额外的型号匹配，在匹配到多个型号时，采用的方法，这里仅仅是实现了与名称匹配，即固件名称有可能会包含型号信息，通过这个额外条件来匹配信息

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
models：当前匹配剩余的型号列表，字符串列表
```

输出结果：
```
bool类型，字符串类型
如果匹配到一个型号，返回True及型号名称
否则，返回False
```

## more_vendor_extra_models_match(may_info, folder_name)
描述：多公司的额外匹配，基于extra_models_match()函数，扩展为多公司多型号的名称匹配。

输入参数：
```
may_info：find_all_models()函数的查询结果，字典类型
folder_name：固件解压的具体位置，字符串类型
```

输出结果：
```
bool类型，字符串类型
如果匹配到一个型号，返回True及{vendor:[model]}
否则，返回False
```

## find_models_info_by_firmware(folder_name, engine, file_name)
描述：实现了匹配的完整过程

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
engine：数据库引擎
file_name：固件文件名称
```

输出结果：
```
字典类型
{
    'may_models_info': 可能结果信息，字典类型{vendor:[models]},
    flag: 情况分类标识，
    file_name: 文件名称
}
```

情况分类

|            分类标识             |         may_models_info的数据         |
| :-----------------------------: | :-----------------------------------: |
|  simple_flag，一公司一型号情况  |           {vendor:[model]}            |
|  models_flag，一公司多型号情况  |     {vendor:[model1,model2,...]}      |
| no_model_flag，一公司无型号情况 |              {vendor:[]}              |
|    vendors_flag ，多公司情况    | {'may_venders':[vendor1, vendor2...]} |
|   no_match_flag，匹配失败情况   |                  {}                   |
| file_name_flag，文件名匹配标识  |                                       |

