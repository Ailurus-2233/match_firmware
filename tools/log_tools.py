import os
from pathlib import Path


# 创建log目录
def init_log_folder(log_folder):
    log_folder = Path(log_folder)
    if not log_folder.exists():
        os.mkdir(log_folder)


# 将结果写入log
def make_a_log(log_folder, result, files_folder):
    log_folder = Path(log_folder)
    may_models_info = result['may_models_info']
    file_name = result['file_name']
    flags = result['flags']
    # 匹配结果仅为一个公司，一个型号的情况
    if flags['simple_flag']:
        log_one_vendor_one_model(may_models_info, log_folder, files_folder, file_name, flags)
    # 匹配结果为一个公司，多个型号的情况
    if flags['models_flag']:
        log_one_vendor_more_model()
    # 匹配结果为，一个公司，无匹配型号
    if flags['no_model_flag']:
        log_one_vendor_no_model()
    # 匹配结果为，多个公司
    if flags['vendors_flag']:
        log_more_vendor()
    # 匹配结果为，未命中
    if flags['no_match_flag']:
        log_no_match()


# 一个公司，一个型号 的结果记录
def log_one_vendor_one_model(may_model_info, log_folder, files_folder, file_name, flags):
    vendor = list(may_model_info.keys())[0]
    model = may_model_info[vendor][0]
    log_file = log_folder / "{}_{}_{}.log".format(vendor, model, file_name)
    s = 'This firmware is extracted from vendor: {}, device:{}'.format(vendor, model)
    if flags['file_name_flag']:
        s += "(File name is one of the conditions)"
    cmd = 'echo "{}" > {}'.format(s, log_file)
    os.system(cmd)
    cmd = 'echo "--------------vendor info ({})--------------" >> {}'.format(vendor, log_file)
    os.system(cmd)
    cmd = 'cd temp;grep -rInaHse {} {} >> ../{}'.format(vendor, files_folder, log_file)
    os.system(cmd)
    cmd = 'echo "--------------model info ({})--------------" >> {}'.format(model, log_file)
    os.system(cmd)
    cmd = 'cd temp;grep -raIinHse {} {} >> ../{}'.format(model, files_folder, log_file)
    os.system(cmd)


# 一个公司，多个型号 的结果记录
def log_one_vendor_more_model():
    return 0


# 一个公司，无匹配型号 的结果记录
def log_one_vendor_no_model():
    return 0


# 多个公司 的结果记录
def log_more_vendor():
    return 0


# 无匹配 的结果记录
def log_no_match():
    return 0