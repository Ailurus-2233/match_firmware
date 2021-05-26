import os
import re
from tqdm import tqdm
from tools.database_tools import run_sql, get_versions_by_company


# 比对固件信息，获取该固件所述的设备信息
# 返回为一个字典类型
def find_firmware(companies, folder_name, engine):
    print("Searching")
    may_firmwares = {}
    # tqdm()是显示一个进度条，遍历公司名称
    for company in tqdm(companies):
        if company is None:
            continue
        # 执行grep查询，如果固件中有该公司的字段，则进行设备型号比对
        cmd = "cd temp;grep -rInHse '{}' {}".format(company, folder_name)
        req = os.popen(cmd, "r")
        if not is_in_word(req, company):
            versions = get_versions_by_company(engine, company)
            flag = False
            # 设备型号比对
            for version in versions:
                if version is None:
                    continue
                cmd = "cd temp;grep -rInHsie '{}' {}".format(version, folder_name)
                req_in = os.popen(cmd, "r")
                if len(req_in.readlines()) >= 1:
                    if not flag:
                        may_firmwares[company] = []
                        flag = True
                    may_firmwares[company].append(version)
                req_in.close()
        req.close()
    return may_firmwares


# 最后将排查结果整理为数组形式
def last_matching(may_firmwares, engine):
    ans = []
    for key in may_firmwares.keys():
        for ver in may_firmwares[key]:
            sql = "select * from list where company = '{}' and version = '{}';".format(key, ver)
            req = run_sql(sql, engine).values
            for r in req:
                ans.append(r)
            # print(sql)
    return ans


# 通过正则表达式，规避掉字段出现在单词中的情况
def is_in_word(req, company):
    count = 0
    pattern = re.compile(r'[^a-zA-Z]{}[^a-zA-Z]'.format(company))
    for line in req.readlines():
        if pattern.search(line) is not None:
            count += 1
    return count == 0
