import os
from pathlib import Path
from tools import match


# 创建log目录
def init_log_folder(log_folder):
    log_folder = Path(log_folder)
    if not log_folder.exists():
        os.mkdir(log_folder)


# 将结果写入log
def make_a_log(log_folder, result, files_folder):
    log_folder = Path(log_folder)
    init_log_folder(log_folder)
    may_models_info = result["may_models_info"]
    file_name = result["file_name"]
    flags = result["flags"]
    # 匹配结果仅为一个公司，一个型号的情况
    if flags["simple_flag"]:
        log_one_vendor_one_model(may_models_info, log_folder, files_folder, file_name, flags)
    # 匹配结果为一个公司，多个型号的情况
    if flags["models_flag"]:
        log_one_vendor_more_model(may_models_info, log_folder, files_folder, file_name)
    # 匹配结果为，一个公司，无匹配型号
    if flags["no_model_flag"]:
        log_one_vendor_no_model(may_models_info, log_folder, files_folder, file_name)
    # 匹配结果为，多个公司
    if flags["vendors_flag"]:
        log_more_vendor(may_models_info, log_folder, files_folder, file_name)
    # 匹配结果为，未命中
    if flags["no_match_flag"]:
        log_no_match(file_name)


# 一个公司，一个型号 的结果记录
def log_one_vendor_one_model(may_models_info, log_folder, files_folder, file_name, flags):
    vendor = list(may_models_info.keys())
    model = may_models_info[vendor[0]]
    log_file = log_folder / "{}_{}_{}.log".format(vendor[0], model[0], file_name)
    s = "This firmware is extracted from vendor: {}, device:{}".format(vendor[0], model[0])
    if flags["file_name_flag"]:
        s += "(File name is one of the conditions)"
    write_file(s + "\n", log_file, "w")
    log_info(vendor, log_file, files_folder, "vendor")
    log_info(model, log_file, files_folder, "model")
    print("log file is saved in {}".format(log_file))


# 一个公司，多个型号 的结果记录
def log_one_vendor_more_model(may_models_info, log_folder, files_folder, file_name):
    vendor = list(may_models_info.keys())
    models = may_models_info[vendor[0]]
    log_file = log_folder / "{}_moreModels_{}.log".format(vendor[0], file_name)
    s = "This firmware is extracted from vendor: {}, device:{}\n".format(vendor[0], ",".join(models))
    write_file(s, log_file, "w")
    log_info(vendor, log_file, files_folder, "vendor")
    log_info(models, log_file, files_folder, "model")
    print("log file is saved in {}".format(log_file))


# 一个公司，无匹配型号 的结果记录
def log_one_vendor_no_model(may_models_info, log_folder, files_folder, file_name):
    vendor = may_models_info["may_vendor"]
    log_file = log_folder / "{}_noModel_{}.log".format(vendor[0], file_name)
    s = "This firmware is extracted from vendor: {}\n".format(vendor[0])
    write_file(s, log_file, "w")
    log_info(vendor, log_file, files_folder, "vendor")
    print("log file is saved in {}".format(log_file))


# 多个公司 的结果记录
def log_more_vendor(may_models_info, log_folder, files_folder, file_name):
    vendors = may_models_info["may_vendors"]
    log_file = log_folder / "moreVendors_{}.log".format(file_name)
    s = "This firmware is extracted from vendor: {}\n".format(",".join(vendors))
    write_file(s, log_file, "w")
    log_info(vendors, log_file, files_folder, "vendor")
    print("log file is saved in {}".format(log_file))


# 无匹配 的结果记录
def log_no_match(file_name):
    write_file(file_name + "\n", "log/noMatch.log", "a")
    print("log file is saved in log/no_match.log")


def get_re_result(log, info):
    result = []
    for line in log.readlines():
        if match.is_available_line(line, info):
            result.append(line)
    return result


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


def log_info(infos, log_file, files_folder, info_type):
    for info in infos:
        s = "--------------{} info ({})--------------\n".format(info_type, info)
        write_file(s, log_file, "a")
        cmd = "cd temp;grep -Hrain {} {} >> temp.txt".format(info, files_folder)
        os.system(cmd)
        re_info = match.find_availabe_lines(info)
        os.remove("temp/temp.txt")
        if info_type == "vendor":
            if len(re_info) > 5:
                flag = True
        else:
            if len(re_info) != 0:
                flag = True
        if flag:
            for line in re_info:
                write_file(line.decode('utf8'), log_file, "a")
