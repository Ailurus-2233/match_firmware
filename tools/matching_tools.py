import os
import re
# from tqdm import tqdm
from tools import database_tools


# 比对固件信息，获取该固件所述的设备信息
# 返回为一个字典类型
def find_models_info_by_firmware(folder_name, engine):
    print("Searching")
    may_models_info = {}
    vendors = database_tools.select_vendors(engine)
    may_vendors = get_exist_vendors(folder_name, vendors)
    if len(may_vendors) > 0:
        for vendor in may_vendors:
            models = database_tools.select_models_by_vendor(engine, vendor)
            may_info = get_exist_models_by_vendor(folder_name, models, vendor)
            if len(may_info[vendor]) > 0:
                may_models_info[vendor] = may_info[vendor]
        # if len(may_models_info.keys()) == 0:
            # TODO 记录到仅仅匹配公司的log文件中
        # else :
            # TODO 记录到匹配公司-设备的log文件中
    # else :
        # TODO 记录到无匹配log文件中
    return may_models_info


# 通过正则表达式，规避掉字段出现在单词中的情况
def is_in_word(req, vendor):
    count = 0
    pattern = re.compile(r'[^a-zA-Z]{}[^a-zA-Z]'.format(vendor))
    for line in req.readlines():
        if pattern.search(line) is not None:
            count += 1
    return count == 0


# 判断该固件是否属于该公司
def is_exist_vendor(folder_name, vendor_name):
    # 执行grep查询，如果固件中有该公司的字段，则进行设备型号比对
    cmd = "cd temp;grep -rInHse '{}' {}".format(vendor_name, folder_name)
    req = os.popen(cmd, "r")
    ans = not is_in_word(req, vendor_name)
    req.close()
    return ans


# 判断该固件是否属于该设备
def is_exist_model(folder_name, model_name):
    cmd = "cd temp;grep -rIinHse '{}' {}".format(model_name, folder_name)
    req = os.popen(cmd, "r")
    ans = len(req.readlines()) >= 1
    req.close()
    return ans


# 返回解包文件夹中，出现过的公司列表
def get_exist_vendors(folder_name, vendors):
    ans = []
    for vendor in vendors:
        if vendor is None:
            continue
        if is_exist_vendor(folder_name, vendor):
            ans.append(vendor)
    return ans


# 返回解包文件中，出现过该公司的设备列表
def get_exist_models_by_vendor(folder_name, models, vendor):
    ans = []
    for model in models:
        if model is None:
            continue
        if is_exist_model(folder_name, model):
            ans.append(model)
    return {vendor: ans}
