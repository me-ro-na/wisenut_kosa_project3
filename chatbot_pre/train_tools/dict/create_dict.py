import sys
[sys.path.append(i) for i in ['.', '..']]
from chatbot_pre.utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle
import os

# 말뭉치 데이터 읽어오기
def read_corpus_data(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        data = [line.split(',') for line in f.read().splitlines()]
    return data


# 말뭉치 데이터 가져오기
corpus_data = read_corpus_data(rf'{os.path.abspath("chatbot_pre/train_tools/dict/corpus.csv")}')


# 망뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
p = Preprocess()
dict = []
for c in corpus_data:
    pos = p.pos(c[0])
    for k in pos:
        dict.append(k[0])

# 사전에 사용될 word2index 생성
# 사전의 첫번 째 인덱스에는 OOV 사용
tokenizer = preprocessing.text.Tokenizer(oov_token='OOV')
tokenizer.fit_on_texts(dict)
word_index = tokenizer.word_index

# 사전 파일 생성
f = open(rf'{os.path.abspath("chatbot_pre/train_tools/dict/chatbot_dict.bin")}', "wb")
try:
    pickle.dump(word_index, f)
except Exception as e:
    print(e)
finally:
    f.close()
