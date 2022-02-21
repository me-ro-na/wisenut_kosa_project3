import pandas as pd
import numpy as np
import math
import os

BASE_DF = pd.read_csv(rf"{os.path.abspath('jobabot/static/csvs/career_experience.csv')}")

def get_data():
    result = to_trunc(BASE_DF).values.tolist()

    for row in result:
        if isinstance(row[15], str) and "|" in row[15]:
            row[15] = ','.join(row[15].split("|"))
            # row[15].replace("|", ",")
        if "&" in row[4]:
            row[4] = ",".join(row[4].split("&"))
    return result

def get_addrs(fors, jobs):
    if fors == "전체": fors = None
    if jobs == "전체": jobs = None
    df = BASE_DF
    addrs = []
    fors_dicts = {'초등학생': '초', '중학생': '중', '고등학생': '고'}
    # 초기 페이지
    if fors is None and jobs is None:
        addrs = pd.factorize(df['체험지역'])[1].tolist()
    # 체험 대상만 선택한 경우
    elif jobs is None and fors is not None:
        for i in range(len(df)):
            if fors_dicts[fors] in df.loc[i, "체험대상"] and (df.loc[i, "체험지역"]) not in addrs:
                addrs.append(df.loc[i, "체험지역"])
    # 직업만 선택한 경우
    elif jobs is not None and fors is None:
        for i in range(len(df)):
            if df.loc[i, "직무/학과"] == jobs and (df.loc[i, "체험지역"]) not in addrs:
                addrs.append(df.loc[i, "체험지역"])
    # 지역, 체험 대상 모두 선택한 경우
    else:
        for i in range(len(df)):
            if fors_dicts[fors] in df.loc[i, "체험대상"] and (df.loc[i, "직무/학과"]) == jobs and df.loc[i, "체험지역"] not in addrs:
                addrs.append(df.loc[i, "체험지역"])
    addrs.sort()
    return addrs

def get_jobs(addr, fors):
    if addr == "전체": addr = None
    if fors == "전체": fors = None
    df = BASE_DF
    jobs = []
    fors_dicts = {'초등학생': '초', '중학생': '중', '고등학생': '고'}
    # 초기 페이지
    if addr is None and fors is None:
        jobs = pd.factorize(df['직무/학과'])[1].tolist()
    # 체험 대상만 선택한 경우
    elif addr is None and fors is not None:
        for i in range(len(df)):
            if fors_dicts[fors] in df.loc[i, "체험대상"] and (df.loc[i, "직무/학과"]) not in jobs:
                jobs.append(df.loc[i, "직무/학과"])
    # 지역만 선택한 경우
    elif addr is not None and fors is None:
        for i in range(len(df)):
            if df.loc[i, "체험지역"] == addr and (df.loc[i, "직무/학과"]) not in jobs:
                jobs.append(df.loc[i, "직무/학과"])
    # 지역, 체험 대상 모두 선택한 경우
    else:
        for i in range(len(df)):
            if df.loc[i, "체험지역"] == addr and fors_dicts[fors] in df.loc[i, "체험대상"] and (df.loc[i, "직무/학과"]) not in jobs:
                jobs.append(df.loc[i, "직무/학과"])
    return jobs

def get_fors(addr, jobs):
    if addr == "전체": addr = None
    if jobs == "전체": jobs = None
    df = BASE_DF
    fors = []
    result = []
    dicts = {'초': '초등학생', '중': '중학생', '고': '고등학생'}
    # 초기 페이지
    if addr is None and jobs is None:
        fors = pd.factorize(df['체험대상'])[1].tolist()
    # 체험 직무만 선택한 경우
    elif addr is None and jobs is not None:
        for i in range(len(df)):
            if df.loc[i, "직무/학과"] == jobs and (df.loc[i, "체험대상"]) not in fors:
                fors.append(df.loc[i, "체험대상"])
    # 지역만 선택한 경우
    elif addr is not None and jobs is None:
        for i in range(len(df)):
            if df.loc[i, "체험지역"] == addr and (df.loc[i, "체험대상"]) not in fors:
                fors.append(df.loc[i, "체험대상"])
    # 지역, 체험 직무 모두 선택한 경우
    else:
        for i in range(len(df)):
            if df.loc[i, "체험지역"] == addr and df.loc[i, "직무/학과"] == jobs and (df.loc[i, "체험대상"]) not in fors:
                fors.append(df.loc[i, "체험대상"])
    
    for i in range(len(fors)):
        splited = fors[i].split('|')
        for word in splited:
            if dicts[word] not in result:
               result.append(dicts[word])
    return result


def get_search_result(addr, fors, jobs):
    if addr == "전체": addr = None
    if jobs == "전체": jobs = None
    if fors == "전체": fors = None

    df = BASE_DF
    # df = df.astype({'column' : 'type'})
    fors_dicts = {'초등학생': '초', '중학생': '중', '고등학생': '고'}
    result = []
    # 전체 모두 선택되지 않은 경우    
    if(addr is None and jobs is None and fors is None):
        get_data()
    # 대상만 선택된 경우
    elif(addr is None and jobs is None and fors is not None):
        for i in range(len(df)):
            if (fors_dicts[fors] in df.loc[i, "체험대상"]):
                result.append(to_int(df.loc[i].values.tolist()))
    # 직무만 선택된 경우
    elif(addr is None and jobs is not None and fors is None):
        for i in range(len(df)):
            if (df.loc[i, "직무/학과"]) == jobs:
                result.append(to_int(df.loc[i].values.tolist()))
    # 지역만 선택된 경우
    elif(addr is not None and jobs is None and fors is None):
        for i in range(len(df)):
            if (df.loc[i, "체험지역"]) == addr:
                result.append(to_int(df.loc[i].values.tolist()))
    # 대상, 직무만 선택된 경우
    elif(addr is None and jobs is not None and fors is not None):
        for i in range(len(df)):
            if (df.loc[i, "직무/학과"]) == jobs and (fors_dicts[fors] in df.loc[i, "체험대상"]):
                result.append(to_int(df.loc[i].values.tolist()))
    # 대상, 지역만 선택된 경우
    elif(addr is not None and jobs is None and fors is not None):
        for i in range(len(df)):
            if (df.loc[i, "체험지역"]) == addr and (fors_dicts[fors] in df.loc[i, "체험대상"]):
                result.append(to_int(df.loc[i].values.tolist()))
    # 지역, 직무만 선택된 경우
    elif(addr is not None and jobs is not None and fors is None):
        for i in range(len(df)):
            if (df.loc[i, "체험지역"]) == addr and (df.loc[i, "직무/학과"]) == jobs:
                result.append(to_int(df.loc[i].values.tolist()))
    # 전체 선택된 경우
    else:
        for i in range(len(df)):
            if (df.loc[i, "체험지역"]) == addr and (df.loc[i, "직무/학과"]) == jobs and (fors_dicts[fors] in df.loc[i, "체험대상"]):
                result.append(to_int(df.loc[i].values.tolist()))
    return result

def get_modal_data(data_no):
    df = BASE_DF
    resultList = []
    result = df.loc[(df["NO"] == int(data_no))]
    for_dict = {"초": "초등학생", "중": "중학생", "고": "고등학생"}
    
    edu_temp = str(result["교육부지원프로그램"].values[0])
    job_temp = str(result["직무/학과"].values[0])
    appr_loc_temp = str(result["신청가능지역"].values[0])


    for_temp = str(result["체험대상"].values[0]).split("|")
    for_temp = ",".join([for_dict[i] for i in for_temp])
    title_temp = ",".join(str(result["프로그램명"].values[0]).split("&"))

    if result["교육부지원프로그램"].values[0] is not None:
        edu_temp = ""
    if result["직무/학과"].values[0] is not None:
        job_temp = ""
    if result["신청가능지역"].values[0] is not None:
        appr_loc_temp = ""
    
    
    resultList.append(title_temp)
    resultList.append(str(result["체험지역"].values[0]))
    resultList.append(str(result["체험유형"].values[0]))
    resultList.append(str(result["체험처"].values[0]))
    resultList.append(str(result["체험처유형"].values[0]))
    resultList.append(edu_temp)
    resultList.append(job_temp)
    resultList.append(str(result["체험일"].values[0]))
    resultList.append(str(result["모집인원"].values[0]) + " 명")
    resultList.append(str(result["이수시간"].values[0]))
    resultList.append(str(result["비용"].values[0]))
    resultList.append(appr_loc_temp)
    resultList.append(for_temp)
    resultList.append(int(result["만족도"].values[0]))
    resultList.append(int(result["안전도"].values[0]))
    
    return resultList

# ------------------------------------기타------------------------------------
def to_trunc(df):
    for i in range(len(df)):
        if (np.isnan(df.loc[i, '만족도'])):
            df.loc[i, '만족도'] = 0
        else:
            df.loc[i, "만족도"] = math.trunc(df.loc[i, "만족도"])
        if (np.isnan(df.loc[i, '안전도'])):
            df.loc[i, '안전도'] = 0
        else:
            df.loc[i, "안전도"] = math.trunc(df.loc[i, "안전도"])
    return df

def to_int(list):
    for i in range(len(list)):
        if (i == 18):
            if(np.isnan(list[i])):
                list[i] = 0
            else:
                list[i] = math.trunc(list[i])
        elif(i == 19):
            if (np.isnan(list[i])):
                list[i] = 0
            else:
                list[i] = math.trunc(list[i])
        else:
            if i == 0 or i == 3 or i == 10:
                list[i] = int(list[i])
    return list