from ast import arg
import logging
import re
import numpy as np
import pandas as pd

import os

# 규칙 만족 여부
def matching(pattern, sentence):
  p = re.compile(pattern)
  m = p.findall(sentence)

  result = False if len(m) < 1 else True
  return result


# 규칙을 만족하는 행을 전달
def getRule(str):
  return df[df['규칙'].apply(matching, args=(str,))]


# know코드와 직업 대조표를 이용해 know코드 리스트를 직업으로 반환
def knowcode_list_to_job(cod):
  df_inner = pd.DataFrame()
  for i in cod:
    k = df3.loc[df3["knowcode"] == i]
    df_inner = pd.concat([df_inner,k])
    
  job_list = df_inner["직업"].tolist()

  return job_list
  
#csv파일 불러오기###########################################
df = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/rule_test.csv")}')
df2 = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/first_2020.csv")}')
df3 = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/2020_code.csv")}')


print('안녕하세요. 진로 상담사 입니다.\n무엇을 도와 드릴까요?')
qus = input('> ')

while True:
  df_rows = getRule(qus)
  type = df_rows['종류'].values
  msg = df_rows['답변'].values

  logging.info(f'{type}, {msg}')

  if '종료' in type:
    print(msg[0])
    break

  elif set(type) & set(['직업','진로']):
    #DB완성되면 수정할 사항###########################################################
    if '인사' in type:
      print(msg[0])

    job = df_rows.loc[df_rows['종류'] == '직업', '답변'].values
    maj = df_rows.loc[df_rows['종류'] == '진로', '답변'].values

    #저는 비누및화장품화학공학기술자및연구원이 되고 싶습니다. 어떤 능력이 필요할까요?
    #저는 행정부고위공무원이 되고 싶습니다. 어떤 능력이 필요할까요?
    ##저는 행정부고위공무원이 되고 싶습니다. 어떤 #####공부가 필요할까요?
    fltmxm = []
    soqn = []

    job = df_rows.loc[df_rows['종류'] == '직업', '답변'].values
    job = job[0]
    job_code = df3.loc[df3["직업"] == job]
    for i in job_code["knowcode"]:
      fltmxm.append(i)
      
    for i in fltmxm:
      first = df2.loc[df2["knowcode"] == i]
      first.dropna()
    print("glglglgl", first.columns.values)
    word_ = f'{first}능력이 필요합니다.' if len(maj) < 1 else '그것에 필요한 공부를 하세요.'
    print(word_)

  elif set(type) & set(['능력']):
    #저는 시력이 좋습니다. 무슨직업을 가지면 좋을까요?
    if '인사' in type:
      print(msg[0])
    ability = df_rows.loc[df_rows['종류'] == '능력', '답변'].values
    ability = ability[0]
    #DB완성되면 수정할 사항###########################################################

    fltmxm = []
    top3 = df2.sort_values(ability, ascending = False).head(3)
    for i in top3["knowcode"]:
      fltmxm.append(i)

    rufrhk = knowcode_list_to_job(fltmxm)

    print(f'업무수행능력가치관 설문에서의 {ability}능력이 필요한 상위 3개의 직업 탐색 결과{rufrhk}을(를) 추천드립니다.')
  elif '추천' in type:
    print(msg[0])
  elif '모름' in type:
    print(msg[0])
  elif '인사' in type:
    print(msg[0])
  else:
    print('죄송합니다. 무슨 말인지 모르겠습니다.')

  qus = input('> ')