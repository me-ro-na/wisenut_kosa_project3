from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import numpy as np
import pandas as pd

import sys, os
[sys.path.append(i) for i in ['.', '..']]
from chatbot_pre.utils.Preprocess import Preprocess
p = Preprocess(word2index_dic=rf'{os.path.abspath("chatbot_pre/train_tools/dict/chatbot_dict.bin")}')

job_mini = pd.read_csv(rf'{os.path.abspath("chatbot_pre/datasets/datas/job_mini.csv")}', header=None)
job_big = pd.read_csv(rf'{os.path.abspath("chatbot_pre/datasets/datas/job_big.csv")}', header=None)

new_sentence = '요리를 전공하고 요리사가 되고싶어요'
# new_sentence = '건축학과 가고싶어요'
pos = p.pos(new_sentence)
keywords = p.get_keywords(pos, without_tag=True)
new_seq = p.get_wordidx_sequence(keywords)

max_len = 40
new_padded_seqs = preprocessing.sequence.pad_sequences([new_seq], padding="post", value=0, maxlen=max_len)

print("새로운 유형의 시퀀스 : ", new_seq)
print("새로운 유형의 시퀀스 : ", new_padded_seqs)
max = np.argmax(new_padded_seqs)
print("max = ", keywords[max])
job_idxes = job_mini.index[(job_mini[0].str.contains(keywords[max]))].tolist()
big = False

if not job_idxes:
    job_idxes = job_big.index[(job_big[0].str.contains(keywords[max]))].tolist()
    big = False if not job_idxes else True
    print(big)
if job_idxes and big == True:
    keywords[max] = job_big[0][job_idxes[0]]
    tmp = 3
    if len(job_idxes) > 3:
        for i in range(1, 3):
            keywords.append(job_big[0][job_idxes[i]])
    big = False
elif job_idxes:
    keywords[max] = job_mini[0][job_idxes[0]]
    tmp = 3
    if len(job_idxes) > 3:
        for i in range(1, tmp):
            keywords.append(job_mini[0][job_idxes[i]])

new_seq = p.get_wordidx_sequence(keywords)
new_padded_seqs = preprocessing.sequence.pad_sequences([new_seq], padding="post", value=0, maxlen=max_len)

# NER 예측
model = load_model(rf"{os.path.abspath('chatbot_pre/models/ner/ner_model.h5')}")
p = model.predict(np.array([new_padded_seqs[0]]))
p = np.argmax(p, axis=-1) # 예측된 NER 인덱스 값 추출

print(f"{'단어':10} {'예측된 NER':5}")
print("-" * 50)
index_to_ner = {1: 'O', 2: 'J_MAJOR', 3: 'J_M_JOB', 4: 'J_TELENT', 5: 'J_B_JOB', 0: 'PAD'}
for w, pred in zip(keywords, p[0]):
    print("{:10} {:5}".format(w, index_to_ner[pred]))