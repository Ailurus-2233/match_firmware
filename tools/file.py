import hashlib
import os
from pathlib import Path


# 获取文件的md5
def get_file_md5(file):
    with open(file, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(10240)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


# 使用binwalk将.bin文件解包到temp中
def unpack_firmware(file):
    print("unpacking firmware file: {}".format(file.split("/")[-1]))
    temp_folder = Path('temp')
    if not temp_folder.exists():
        os.mkdir(temp_folder)
    cmd = "cd temp; binwalk -eq '{}'".format(file)
    os.system(cmd)
    dir = os.listdir("temp")
    print("The files are saved in Temp folder")
    return dir[0]


# 删除生成的temp文件夹
def remove_file():
    print("remove Temp folder")
    cmd = "rm -rf temp"
    os.system(cmd)


# 以str的方式写入文件
def write_file(s, file_name, m):
    with open(file_name, m) as f:
        f.write(s)


# 以字节的方式写入文件
def write_file_bytes(s, file_name, m):
    with open(file_name, m + "b") as f:
        if isinstance(s, str):
            s = s.encode()
        f.write(s)
