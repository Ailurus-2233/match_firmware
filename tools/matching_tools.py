import os
import re
from tqdm import tqdm
from tools import database_tools


# 比对固件信息，获取该固件所述的设备信息
# 返回为一个字典类型
def find_models_info_by_firmware(folder_name, engine):
    no_match_flag = False
    no_model_flag = False
    vendors_flag = False
    models_flag = False
    file_name_flag = False
    may_models_info = {}

    vendors = database_tools.select_vendors(engine)
    may_vendors = get_exist_vendors(folder_name, vendors)

    # 匹配公司为空，标注 no_match
    if len(may_vendors) == 0:
        no_match_flag = True

    # 至少有一个匹配公司
    if len(may_vendors) > 0:
        # 遍历比对型号信息
        may_models_info = find_all_models(folder_name, may_vendors, engine)

    # 结果为空，标注 no_match 将may_venders记录为结果
    if len(may_models_info.keys()) == 0:
        no_model_flag = True
        may_models_info['may_venders'] = may_vendors
    # 结果公司数量多于1，标注 公司数量过多 将may_venders记录为结果
    elif len(may_models_info.keys()) > 1:
        vendors_flag = True
        may_models_info['may_venders'] = may_vendors
    else:
        # 公司数量为1，型号数量多于1，标注 型号数量过多，进行额外匹配
        if len(may_models_info[list(may_models_info.keys())[0]]) > 1:
            models_flag = True
            # 进行额外匹配
            vendor = list(may_models_info.keys())[0]
            models = may_models_info[vendor]
            file_name_flag, may_info = extra_models_match(folder_name, models)
            # 匹配成功，记录匹配信息
            if file_name_flag:
                may_models_info[vendor] = [may_info]
    return may_models_info, {'no_match_flag': no_match_flag, 'no_model_flag': no_model_flag, 'vendors_flag': vendors_flag, 'models_flag': models_flag, 'file_name_flag': file_name_flag}


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
    print('Searching vendors')
    for vendor in tqdm(vendors):
        if vendor is None:
            continue
        if is_exist_vendor(folder_name, vendor):
            ans.append(vendor)
    print('may vendors: {}'.format(ans))
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


# 遍历查找所有的型号
def find_all_models(folder_name, may_vendors, engine):
    print('Searching models')
    ans = {}
    for vendor in tqdm(may_vendors):
        models = database_tools.select_models_by_vendor(engine, vendor)
        may_info = get_exist_models_by_vendor(folder_name, models, vendor)
        if len(may_info[vendor]) > 0:
            ans[vendor] = may_info[vendor]
    return ans


# 多型号的情况下，需要进行额外的匹配，这里先只是匹配名称
def extra_models_match(folder_name, models):
    for model in models:
        if model in folder_name:
            return True, model
    else:
        return False
