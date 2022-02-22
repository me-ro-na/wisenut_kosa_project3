import sys

[sys.path.append(i) for i in ['.', '..']]
from chatbot_pre.utils.Database import Database


# 학습 데이터 초기화
def all_clear_train_data(db):
    # 기존 학습 데이터 삭제
    sql = '''
            DELETE FROM jobabot_train_data
        '''
    db.execute(sql)
    # auto increment 초기화
    sql = '''
        ALTER TABLE jobabot_train_data AUTO_INCREMENT=1
    '''
    db.execute(sql)



# db에 데이터 저장
def insert_data(db, xls_row):
    label, intent, ner, question, answer = xls_row
    sql = f'''
        INSERT jobabot_train_data(label, intent, ner, questions, answers) 
        VALUES(
         '{label}', '{intent}', '{ner}', '{question}', '{answer}'
        )
    '''
    # 엑셀에서 불러온 cell에 데이터가 없는 경우, null 로 치환
    sql = sql.replace("'nan'", "null")
    # print(sql)
    db.execute(sql)
    print(f'{question} 저장')


import os
import pandas as pd
train_file = rf'{os.path.abspath("chatbot_pre/train_tools/qna/answers_train_data.csv")}'
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
        if(not wb):
            break
        datas = wb[row]
        lists = [i for i in datas]
        insert_data(db, lists)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()

# CREATE TABLE jobabot_train_data (
#     id INT UNSIGNED AUTO_INCREMENT,
#     label INT NOT NULL,
#     intent TEXT NOT NULL,
#     ner TEXT NULL DEFAULT NULL,
#     questions TEXT NULL DEFAULT NULL,
#     answers TEXT NOT NULL,
#     PRIMARY KEY(id)
# );