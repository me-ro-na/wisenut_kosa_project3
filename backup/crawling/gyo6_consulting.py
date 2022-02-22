#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import requests

import os

# html 태그 제거
def del_html_tag(raw_text):
    return BeautifulSoup(raw_text, "lxml").text

page = 1
session = requests.session()
url = "https://www.gyo6.net/advice/counsel/openCounsel/list"

params = dict()

questions = []
answers = []

# 이번해 기준
year = 2022
# 이중 반복문 break하기 위해 변수 선언
breaker = False
while True:
    # 해당 페이지가 페이지 번호가 바뀔때마다 javascript로 넘어가는 형식이여서, 그에 따른 대처
    params['page_no'] = page
    params['counsel_open_flag'] = 'Y'
    res = session.post(url, data=params)

    # status = 200이 아니면 error
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find("div", "Board")

    for tags in table.select("li"):
        done = tags.find("span", "IconType2")
        if(done is not None):
            done = del_html_tag(str(done)).strip()
            year = int(del_html_tag(str(tags.find("span", "ListDate")))[:4])
            if(year < 2018):
                breaker = True
                break
            # 상담 완료 되고, 2018년 부터의 상담 게시물만
            if(done == "답변완료" and year >= 2018):
                q = del_html_tag(str(tags.find("div", "BoardContents"))).strip()
                a = del_html_tag(str(tags.find("div", "Answer_Contents"))).strip()
                questions.append(q)
                answers.append(a)
    if breaker == True:
        break
    page += 1

print("[GYO6] data to csv file")

resultDict = dict(Question = questions, Answer = answers)

dt = datetime.datetime.now()
fName = f'jobabot/crawling/datas/gyo6_{dt.year}_{dt.month}_{dt.day}.csv'
fName = rf'{os.path.abspath(fName)}'
print(fName)
df = pd.DataFrame(resultDict)

df.to_csv(fName, sep=',', encoding='utf-8-sig', index=False)