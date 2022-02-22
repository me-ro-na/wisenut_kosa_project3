#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from selenium import webdriver

import os

driver = webdriver.Chrome(rf"{os.path.abspath('jobabot/crawling/utils/chromedriver')}")

detail_url = []
page = 1
# 상세 페이지 url 추출
while True:
    url = f"https://www.career.go.kr/cnet/front/counsel/counselList.do?pageIndex={page}"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    tbody = soup.find('tbody')
    
    if(len(tbody.select("tr")) == 2):
        break
    for tags in tbody.select("tr"):
        out = tags.find("td", text="이주의 공감상담")
        done = str(tags.select(".c33a501"))[23:27]
        middle = tags.find("td", text="중학생(14~16세 청소년)")
        high = tags.find("td", text="고등학생(17~19세 청소년)")
        # 상담 완료(답변이 존재함), 중-고등학생 데이터만 추출, 이주의 공감상담 제외(반복으로 나오기 때문에)
        if(done == "상담완료" and out is None and (middle is not None or high is not None)):
            detail_url.append(tags.find("a")["href"])
    page +=1

def del_html_tag(raw_text):
    return BeautifulSoup(raw_text, "lxml").text

questions = []
answers = []
# ages = []
# 사이트 내 상세 페이지에서 질문, 답변 데이터 추출
for i in range(len(detail_url)):
    url = "https://www.career.go.kr" + detail_url[i]
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 연령대
    # age = del_html_tag(str(soup.select(".cff6633")[0]))
    # 질문 부분
    q = del_html_tag(str(soup.select(".board_view>tbody>tr>td")[0])).strip()
    # 답변 부분
    a = del_html_tag(str(soup.select(".advice_reply>tbody>tr>td")[0])).strip()

    questions.append(q)
    answers.append(a)
    # ages.append(age)

print("[CAREERNET] data to csv file")
# resultDict = dict(Questions = questions, Answers = answers, Ages = ages)
resultDict = dict(Questions = questions, Answers = answers)

dt = datetime.datetime.now()
fName = f'jobabot/crawling/datas/careernet_{dt.year}_{dt.month}_{dt.day}.csv'
fName = rf'{os.path.abspath(fName)}'
df = pd.DataFrame(resultDict)

df.to_csv(fName, sep=',', encoding='utf-8-sig', index=False)