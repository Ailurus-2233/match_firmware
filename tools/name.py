from os import name
from tools import file
import re


def for_3xlogic(file_name, path):
    vendor = "3xlogic"
    device = []
    version = ""
    md5 = file.get_file_md5(path + file_name)
    sp_name = file_name.split("+")
    for n in sp_name:
        flag = True
        if "zip" in n:
            flag = False
        if "R0" in n or "R1" in n or "R2" in n or "R3" in n or "R4" in n or "R5" in n or "R6" in n or "R7" in n or "R8" in n or "R9" in n:
            flag = False
        if flag:
            device.append(n.split(",")[0])
        else:
            pattern1 = re.compile(u"[1-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+")
            pattern2 = re.compile(u"[1-9]+\\.[0-9]+\\.[0-9]+")
            pattern3 = re.compile(u"[1-9][0-9][0-9][0-9][0-9][0-9]")
            p1 = pattern1.findall(n)
            if len(p1) == 1:
                version = p1[0]
            else:
                p2 = pattern2.findall(n)
                if len(p2) == 0:
                    continue
                p3 = pattern3.findall(n)
                if len(p3) == 1:
                    version = "{}.{}".format(p2[0], p3[0])
                else:
                    version = p2[0]
    return {
        "vendor": vendor,
        "device": device,
        "version": version,
        "md5": md5,
        "name": file_name
    }


def for_360(file_name, path):
    vendor = "360"
    device = []
    version = ""
    md5 = file.get_file_md5(path + file_name)
    if "bin" in file_name:
        device = ["360POP-P1"]
        version = file_name[10:-4]
    else:
        if file_name == "ota_diff_018_031_PX_stable_QK1801.zip":
            device = ["QK1801"]
        else:
            device = ["QK1809"]
        version = file_name[0:-4]
    return {
        "vendor": vendor,
        "device": device,
        "version": version,
        "md5": md5,
        "name": file_name
    }
