import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
import os

intent_labels = {1: "자기소개", 2: "인트로", 3: "단순 진로 탐색", 4: "직업 관련 질문", 5: "학과 관련 질문", 6: "능력 관련 질문", 7: "기타"}

# 의도 분류 모델 불러오기
model = load_model(rf'{os.path.abspath("chatbot_pre/models/intent/intent_model.h5")}')

# query = '건축공학과를 나와서 건축가가 되고싶은데 어떻게 해야되나요?'
# query = "암기가 좀 되요"
# query = "병원쪽 일에 관심이 있어요"
# query = "가수가 되고싶어요"
# query = "가수가 되고싶어요"
query = '요리를 전공하고 요리사가 되고싶어요'
# query = "건축학과 가고싶어요"

# query = "저에겐 꿈도 미래도 없어요"
# query = "저는 앞으로 큰 인물이 될거에요. 지켜봐주세요. 감사합니다"
# query = "저는 왜 사는걸까요"
# query = "정말 앞으로 뭘 해야 할지 모르겠어요.. 이렇게 사는게 맞을까요"
# query = "제 성적이 요즘에 바닥을 치고 있는데 어떻게 하면 좋을까요ㅠㅠ 선생님"
# query = "안녕하세요?"
# query = "안늉안늉"

import sys
[sys.path.append(i) for i in ['.', '..']]
from chatbot_pre.utils.Preprocess import Preprocess
p = Preprocess(word2index_dic=rf'{os.path.abspath("chatbot_pre/train_tools/dict/chatbot_dict.bin")}')
pos = p.pos(query)
keywords = p.get_keywords(pos, without_tag=True)
seq = p.get_wordidx_sequence(keywords)
sequences = [seq]

# 단어 시퀀스 벡터 크기
from chatbot_pre.config.GlobalParams import MAX_SEQ_LEN
padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

predict = model.predict(padded_seqs)
predict_class = tf.math.argmax(predict, axis=1)
print(query)
print(f"의도 예측 점수: \n{predict}")
print(f"의도: {predict_class.numpy()}-{intent_labels[predict_class.numpy()[0]]}")