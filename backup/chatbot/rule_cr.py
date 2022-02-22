import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

import os

ling_nowcode = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/2020_code.csv")}')
ling_survey = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/first_2020.csv")}')
abil = ["읽고이해하기", "듣고이해하기", "글쓰기", "말하기", "수리력", "논리적분석", "창의력", "범주화", "기억력", "공간지각력", "추리력", "학습전략",  "선택적집중력",  "모니터링" , "사람파악",  "행동조정",  "설득",  "협상",  "가르치기",  "서비스지향" , "문제해결", "판단과의사결정", "시간관리",  "재정관리",  "물적자원관리",  "인적자원관리",  "기술분석",  "기술설계",  "장비선정", "설치",  "전산","품질관리분석", "조작및통제",  "장비의유지", "고장의발견.수리", "작동점검", "조직체계의분석및평가",  "정교한동작", "움직임통제","반응시간과속도", "신체적강인성", "유연성및균형", "시력", "청력"]

df0 = pd.DataFrame({"규칙":["안녕|ㅎㅇ|하이", "고맙|고마워|수고|종료|끝|감사합니다"],
                    "답변":["안녕하세요","안녕히가세요"],
                    "종류":["인사","종료"]})
df1 = pd.DataFrame()
df2 = pd.DataFrame()
#저는 시력이 좋습니다. 무슨직업을 가지면 좋을까요?  종류:능력
#저는 비누및화장품화학공학기술자및연구원이 되고 싶습니다. 어떤 능력이 필요할까요?  종류:직업

df1["규칙"] = ling_nowcode["직업"]
df1["답변"] = ling_nowcode["직업"]#능력을 리턴해야함
df1["종류"] = "직업"

df2["규칙"] = abil
df2["답변"] = abil#직업을 리턴해야함
df2["종류"] = "능력"


df = pd.concat([df0,df1,df2])

df.to_csv("rule_test.csv",index=False)