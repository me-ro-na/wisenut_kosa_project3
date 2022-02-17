import json, re, os, threading
import pandas as pd
import sys
[sys.path.append(i) for i in ['.', '..']]
# 파일 임포트 오류 방지

from project_name.chatbot.utils.Database import Database
from project_name.chatbot.utils.BotServer import BotServer
# from utils.Preprocess import Preprocess
# from models.intent.IntentModel import IntentModel
# from models.ner.NerModel import NerModel
from project_name.chatbot.utils.FindAnswer import FindAnswer


df = pd.read_csv(rf'{os.path.abspath("project_name/chatbot/datasets/rule_test.csv")}')
df2 = pd.read_csv(rf'{os.path.abspath("project_name/chatbot/datasets/first_2020.csv")}')
df3 = pd.read_csv(rf'{os.path.abspath("project_name/chatbot/datasets/2020_code.csv")}')

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



# def to_client(conn, addr, params):
def to_client(conn, addr):
    db = params['db']
    try:
        db.connect()  # 디비 연결
        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 답변 검색
        try:
            f = FindAnswer(db)
            df_rows = getRule(query)
            answer, type  = f.search(df_rows['답변'].values[0])
            if type in ['직업','진로']:
                # job = df_rows.loc[df_rows['종류'] == '직업', '답변'].values[0]
                # maj = df_rows.loc[df_rows['종류'] == '진로', '답변'].values[0]
                #DB완성되면 수정할 사항###########################################################

                # 저는 비누및화장품화학공학기술자및연구원이 되고 싶습니다. 어떤 능력이 필요할까요?
                #저는 행정부고위공무원이 되고 싶습니다. 어떤 능력이 필요할까요?
                ##저는 행정부고위공무원이 되고 싶습니다. 어떤 #####공부가 필요할까요?
                fltmxm = []
                soqn = []

                # job = df_rows.loc[df_rows['종류'] == '직업', '답변'].values
                # job = job[0]
                job_code = df3.loc[df3["직업"] == answer]
                for i in job_code["knowcode"]:
                    fltmxm.append(i)
                
                for i in fltmxm:
                    first = df2.loc[df2["knowcode"] == i]
                    first.dropna()
                word_ = f'{str(first.columns.values[0:-1])[1:-1]}능력이 필요합니다.' if type in "직업" else '그것에 필요한 공부를 하세요.'
                answer = word_

            elif type in ['능력']:
                # 저는 시력이 좋습니다. 무슨직업을 가지면 좋을까요?
                # if '인사' in type:
                #     print(msg[0])
                # ability = df_rows.loc[df_rows['종류'] == '능력', '답변'].values
                # ability = ability[0]
                #DB완성되면 수정할 사항###########################################################

                fltmxm = []
                top3 = df2.sort_values(answer, ascending = False).head(3)

                for i in top3["knowcode"]:
                    fltmxm.append(i)

                rufrhk = knowcode_list_to_job(fltmxm)

                answer = (f'업무수행능력가치관 설문에서의 {answer}능력이 필요한 상위 3개의 직업 탐색 결과{rufrhk}을(를) 추천드립니다.')
            elif '인사' in type:
                answer = answer
            else:
                answer = ('죄송합니다. 무슨 말인지 모르겠습니다.')
            # answer = f.tag_to_word(ner_predicts, answer_text)
        except Exception as e:
            answer = "죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요."
            print(e)

        send_json_data_str = {
            "Query" : query,
            "Answer": answer
        }
        message = json.dumps(send_json_data_str)
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
    print("DB 접속")
    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }
        client = threading.Thread(target=to_client, args=(
            conn,
            addr
            # params
        ))
        client.start()