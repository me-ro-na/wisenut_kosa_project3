import openpyxl
import sys
[sys.path.append(i) for i in ['.', '..']]
from project_name.chatbot.utils.Database import Database


# 학습 데이터 초기화
def all_clear_train_data(db):
    # 기존 학습 데이터 삭제
    sql = '''
            DELETE chatbot_train_data
        '''
    db.execute(sql)
    # auto increment 초기화
    sql = '''
        ALTER TABLE chatbot_train_data AUTO_INCREMENT=1
    '''
    db.execute(sql)



# db에 데이터 저장
def insert_data(db, xls_row):
    query, answer, type = xls_row
    sql = f'''
        INSERT chatbot_train_data(query, answer, type) 
        values(
         '{query}', '{answer}', '{type}'
        )
    '''
    # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
    sql = sql.replace("'None'", "null")
    # print(sql)
    db.execute(sql)
    print(f'{query} 저장')


def sp_query(row):
    query = row[0]
    result = []
    if '|' in query:
        query = query.split("|")[0::1]
        for q in query:
            result.append([q, row[1], row[2]])
            # row.append([q, row[idx][1], row[idx][2]])
    return result

import os
import pandas as pd
train_file = rf'{os.path.abspath("project_name/chatbot/datasets/rule_test.csv")}'
db = None
try:
    db = Database()
    db.connect()
    # 기존 학습 데이터 초기화
    all_clear_train_data(db)
    # 학습 엑셀 파일 불러오기
    wb = pd.read_csv(train_file).values.tolist()
    lists = []
    for row in range(len(wb)):
        datas = wb[row]
        lists = [i for i in sp_query(datas)]
        # print(lists)
        if len(lists) > 1:
            for i in lists: insert_data(db, i)
        else:
            insert_data(db, wb[row])
        if(not wb):
            break

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()

