import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import warnings

import os

warnings.filterwarnings(action = 'ignore')


train_2020 = pd.read_csv(rf'{os.path.abspath("project_name/chatbot/datasets/KNOW_2020.csv")}')


# null값이 빈공간으로 표기돼서 Nan으로 표시하도록 함
for col in train_2020:
        train_2020[col].replace(' ', np.nan, inplace = True)


# 인덱스 제외하고 saq1_1 ~ saq44_2까지 가져와서 float타입으로 변환
df_2020 = train_2020.iloc[0: ,1:89]
df_2020 = df_2020.astype('float')


df = pd.DataFrame()

# 중요도와 수준을 더하기 + saq1 대신 한글 라벨 붙이기
df["글쓰기"] = df_2020["saq1_1"] + df_2020["saq1_2"]
abil = ["읽고이해하기", "듣고이해하기", "글쓰기", "말하기", "수리력", "논리적분석", "창의력", "범주화", "기억력", "공간지각력", "추리력", "학습전략",  "선택적집중력",  "모니터링" , "사람파악",  "행동조정",  "설득",  "협상",  "가르치기",  "서비스지향" , "문제해결", "판단과의사결정", "시간관리",  "재정관리",  "물적자원관리",  "인적자원관리",  "기술분석",  "기술설계",  "장비선정", "설치",  "전산","품질관리분석", "조작및통제",  "장비의유지", "고장의발견.수리", "작동점검", "조직체계의분석및평가",  "정교한동작", "움직임통제","반응시간과속도", "신체적강인성", "유연성및균형", "시력", "청력"]
for i, col in enumerate(abil):
    saq1 = "saq" + str(i+1) + "_1"
    saq2 = "saq" + str(i+1) + "_2"
    df[col] = df_2020[saq1] + df_2020[saq2]

# knowcode 포함시키기
df["knowcode"] = train_2020["knowcode"]

#배출
df.to_csv(rf'{os.path.abspath("project_name/chatbot/datasets/first_2020.csv")}',index=False)