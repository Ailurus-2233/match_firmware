# File

关于文件操作的工具包



## get_file_md5(file)

描述：获取文件的md5

输入：

```
file: 文件路径，字符串类型
```

输出：

```
字符串类型: 文件的md5
```



## unpack_firmware(file)

描述：将固件通过binwalk解包，解压到temp文件夹中

输入：

```
file: 文件路径，字符串类型
```

输出：

```
字符串类型: 解压后的文件夹路径
```



## remove_file()

描述：删除生成的`temp`文件夹