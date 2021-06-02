# Match

主要用来匹配查找固件中对应的信息的工具包



## re_match(line, info)

描述：在grep的过程中，会将单词内部匹配的字符返回出来，这个函数是为了将这种情况识别出来

输入参数：
```
line: 待检测行，是grep结果的一行数据
info: 匹配数据，可以是公司名称，也可以是型号名称
```
输出结果：
```
bool类型
如果行中的结果都是在单词中的话，则为True
至少有一个结果不在单词中，则为False
```



## is_skip_keywords(line)

描述：有些grep结果会出现一些特殊文件，这些文件不足以证明信息的相关性，所以我们需要把他跳过

输入参数：

```
line: 待检测行，是grep结果的一行数据
```

输出结果：

```
bool类型
如果是需要跳过的文件，则为True
否则，则为False
```



## is_function_name(line, info)

描述：在检查log文件的过程中，我们发现有些公司的字段会被作为函数名称，例如：Capture()，查询结果也是需要跳过的。

输入参数：

```
line: 待检测行，是grep结果的一行数据
info: 匹配数据，可以是公司名称，也可以是型号名称
```

输出结果：

```
bool类型
如果是函数形式，如info()，则为True
否则，则为False
```



## is_decodable(info)

描述：因为增加了对二进制文件的检查，但有些二进制是无法解码出信息的，所以需要进行判断

输入参数：

```
line: 待检测行，是grep结果的一行数据
```

输出结果：

```
bool类型
如果是可以解码的行信息，则为True
否则，则为False
```



## is_available_line(line, info)

描述：整合上述所有的判断标准，来判断这一行信息是否可用

输入参数：

```
line: 待检测行，是grep结果的一行数据
info: 匹配数据，可以是公司名称，也可以是型号名称
```

输出结果：

```
bool类型
如果是所有检查通过了，则为True
否则，则为False
```



## find_availabe_lines(info)

描述：传入待匹配信息，将所有可用行返回

输入参数：

```
info: 匹配数据，可以是公司名称，也可以是型号名称
```

输出结果：

```
list类型：
将所有的可用行返回为一个数组
```



## is_exist_info(folder_name, info, info_type)

描述：判断这个解压出来的文件，是否是属于该公司的产品的，判断方式是通过grep查找这个文件夹下是否有该公司（设备）名称

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
info：待匹配的信息，字符串类型
info_type："vendor","model"表示匹配信息类型为公司，或者型号
```

输出结果：
```
bool 类型
匹配成功，则为True
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



## find_exist_models_by_vendor(folder_name, models)

描述：判断这个解压出来的文件，是否是属于特定公司的那些型号的设备，判断是基于is_exist_model()该函数实现的。因为逻辑上models是基于vendor信息查询的，所以不再作为参数传入

输入参数：
```
folder_name：固件解压的具体位置，字符串类型
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



## match_file(path, engine)

描述：执行一次完整的查询操作和记录操作

操作步骤：

1. 提取文件`md5`信息，解压文件到`temp`文件夹
2. 执行`find_models_info_by_firmware`获取结果
3. 将结果存入`log`文件
4. 如果一对一匹配，将文件记录到数据库

具体逻辑，见逻辑文件

输入参数：

```
path: 文件路径，字符串类型
engine: 数据库引擎
```

