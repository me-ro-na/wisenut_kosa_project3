import os, sys
[sys.path.append(i) for i in ['.', '..']]
from chatbot_pre.utils.Preprocess import Preprocess
from chatbot_pre.utils.Database import Database
# 전처리 객체 생성
p = Preprocess(word2index_dic=rf'{os.path.abspath("chatbot_pre/train_tools/dict/chatbot_dict.bin")}')

# 질문/답변 학습 디비 연결 객체 생성
db = Database()
db.connect()    # 디비 연결

# 원문
# query = "오전에 탕수육 10개 주문합니다"
# query = "화자의 질문 의도를 파악합니다."
query = "춤추는걸 좋아해요"
# query = "자장면 주문할게요"

# 의도 파악
from chatbot_pre.models.intent.IntentModel import IntentModel
intent = IntentModel(model_name=rf"{os.path.abspath('chatbot_pre/models/intent/intent_model.h5')}", proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식
from chatbot_pre.models.ner.NerModel import NerModel
ner = NerModel(model_name=rf"{os.path.abspath('chatbot_pre/models/ner/ner_model_test.h5')}", proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)

# 답변 검색
from chatbot_pre.utils.FindAnswer import FindAnswer

try:
    f = FindAnswer(db)
    answer_text = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except Exception as e:
    print(e)
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변 : ", answer)

db.close() # 디비 연결 끊음