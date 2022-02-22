import json, re, os, threading
import pandas as pd
import datetime
# from konlpy.tag import Okt
# okt = Okt()
import sys
[sys.path.append(i) for i in ['.', '..']]
# 파일 임포트 오류 방지

from jobabot.chatbot.utils.Database import Database
from jobabot.chatbot.utils.BotServer import BotServer
from jobabot.chatbot.utils.FindAnswer import FindAnswer



df = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/rule_test.csv")}')
df2 = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/first_2020.csv")}')
df3 = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datasets/2020_code.csv")}')

# 규칙 만족 여부
def matching(pattern, sentence):
    p = re.compile(pattern)
    m = p.findall(sentence)
    result = False if len(m) < 1 else True
    return result
# 규칙을 만족하는 행을 전달
def getRule(query):
    return df[df['규칙'].apply(matching, args=(query,))]
# know코드와 직업 대조표를 이용해 know코드 리스트를 직업으로 반환
def knowcode_list_to_job(cod):
    df_inner = pd.DataFrame()
    for i in cod:
        k = df3.loc[df3["knowcode"] == i]
        df_inner = pd.concat([df_inner,k])
        
    job_list = df_inner["직업"].tolist()

    return job_list



# def to_client(conn, addr, params):
def to_client(conn, addr):
    db = params['db']
    result = []
    try:
        db.connect()  # 디비 연결
        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('=' * 100)
        print(f'[bot] Connection from: {str(addr)}')

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('[bot] Client connection disconnected')
            exit(0)

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print(f"[bot] Received data : {recv_json_data}")
        query = recv_json_data['Query']
        # query_ = okt.morphs(query.replace("[^a-zA-Z가-힣0-9\s]", ""))

        # 답변 검색
        try:
            f = FindAnswer(db)
            df_rows = getRule(query)

            answers = []
            types = []
            answer, type  = f.search(df_rows['답변'].values[0])

            for i in df_rows["답변"].values:
                answer, type  = f.search(i)
                answers.append(answer)
                types.append(type)
                if '인사' in type:
                    result.append(answer)
                elif ('직업' or '진로') in type:
                    # 저는 비누및화장품화학공학기술자및연구원이 되고 싶습니다. 어떤 능력이 필요할까요?
                    #저는 행정부고위공무원이 되고 싶습니다. 어떤 능력이 필요할까요?
                    ##저는 행정부고위공무원이 되고 싶습니다. 어떤 #####공부가 필요할까요?
                    fltmxm = []

                    job_code = df3.loc[df3["직업"] == answer]
                    for i in job_code["knowcode"]:
                        fltmxm.append(i)
                    
                    for i in fltmxm:
                        first = df2.loc[df2["knowcode"] == i]
                        first.dropna()
                    skills = str(first.columns.values[0:-1])[1:-1].replace("\n", "")
                    word_ = f'{answer}이(가) 되기 위해서는 {skills} 능력이 필요합니다.' if type in "직업" else '그것에 필요한 공부를 하세요.'
                    result.append(word_)
                elif '능력' in type:
                    # 저는 시력이 좋습니다. 무슨직업을 가지면 좋을까요?
                    fltmxm = []
                    top3 = df2.sort_values(answer, ascending = False).head(3)

                    for i in top3["knowcode"]:
                        fltmxm.append(i)

                    rufrhk = str(knowcode_list_to_job(fltmxm))[1:-1]

                    word_ = (f'업무수행능력가치관 설문에서의 {answer} 능력이 필요한 상위 3개의 직업 탐색 결과 {rufrhk} 을(를) 추천드립니다.')
                    result.append(word_)
                elif '추천' in type:
                    result.append(answer)
            if not types:
                result = ['죄송합니다. 무슨 말인지 모르겠습니다.']
        except Exception as e:
            result = ["죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."]
            print(e)

        send_json_data_str = {
            "Query" : query,
            "Answer": result
        }
        f = open(rf"{os.path.abspath('jobabot/chatbot/datasets/export_msg.txt')}", "a", encoding="UTF-8")
        f.write(f"[{str(datetime.datetime.now())[:-7]}] [{addr[0]}, {addr[1]}]: {query}\n")
        for i in result:
            f.write(f"[{str(datetime.datetime.now())[:-7]}] [Answer]: {i}\n")
        f.close()
        message = json.dumps(send_json_data_str, ensure_ascii=False)
        conn.send(message.encode())

    except Exception as ex:
        print(ex)

    finally:
        if db is not None: # db 연결 끊기
            db.close()
        conn.close()


if __name__ == '__main__':
    # 질문/답변 학습 디비 연결 객체 생성
    db = Database()
    print("[bot] DB connected")
    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("[bot] server started")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }
        client = threading.Thread(target=to_client, args=(
            conn,
            addr
        ))
        client.start()