import threading, json, datetime, os, sys
[sys.path.append(i) for i in ['.', '..']]

from config.DatabaseConfig import *
from jobabot.chatbot.utils.Database import Database
from jobabot.chatbot.utils.BotServer import BotServer
from jobabot.chatbot.utils.Preprocess import Preprocess
from jobabot.chatbot.models.intent.IntentModel import IntentModel
from jobabot.chatbot.models.ner.NerModel import NerModel
from jobabot.chatbot.utils.FindAnswer import FindAnswer


# 전처리 객체 생성
p = Preprocess(word2index_dic=rf'{os.path.abspath("jobabot/chatbot/train_tools/dict/chatbot_dict.bin")}')

# 의도 파악 모델
intent = IntentModel(model_name=rf"{os.path.abspath('jobabot/chatbot/models/intent/intent_model.h5')}", proprocess=p)

# 개체명 인식 모델
ner = NerModel(model_name=rf"{os.path.abspath('jobabot/chatbot/models/ner/ner_model_test.h5')}", proprocess=p)


def to_client(conn, addr, params):
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

        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]

        # 개체명 파악
        ner_predicts = ner.predict(query, intent_name)
        ner_tag = ner.predict_tags(query, intent_name)

        print(ner_tag)
        # 답변 검색
        try:
            f = FindAnswer(db)
            answers = f.search(intent_name, ner_tag)
            print(answers)
            for a in answers:
                result.append(f.tag_to_word(ner_predicts, a['answers']) if ner_tag else a['answers'])

        except Exception as e:
            print(e)
            result.append("죄송해요 무슨 말인지 모르겠어요. 조금 더 공부 할게요.")

        send_json_data_str = {
            "Query" : query,
            "Answer": result
            # "Intent": intent_name,
            # "NER": str(ner_predicts)
        }
        f = open(rf"{os.path.abspath('jobabot/chatbot/datas/export_msg_log.txt')}", "a", encoding="UTF-8")
        f.write(f"[{str(datetime.datetime.now())[:-7]}] [{addr[0]}, {addr[1]}]: {query}\n")
        for i in result:
            f.write(f"[{str(datetime.datetime.now())[:-7]}] [Answer]: {i}\n")
        f.close()

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
            addr,
            params
        ))
        client.start()
