import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import os
import pandas as pd

# 전처리 객체 생성
job_mini = pd.read_csv(rf'{os.path.abspath("chatbot_pre/datasets/datas/job_mini.csv")}', header=None)
job_big = pd.read_csv(rf'{os.path.abspath("chatbot_pre/datasets/datas/job_big.csv")}', header=None)

# 개체명 인식 모델 모듈
class NerModel:
    def __init__(self, model_name, proprocess):

        # BIO 태그 클래스 별 레이블
        self.index_to_ner = {1: 'O', 2: 'J_MAJOR', 3: 'J_M_JOB', 4: 'J_TELENT', 5: 'J_B_JOB', 0: 'PAD'}

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)

        # 챗봇 Preprocess 객체
        self.p = proprocess


    # 개체명 클래스 예측
    def predict(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)

        max = np.argmax(padded_seqs)
        job_idxes = job_mini.index[(job_mini[0].str.contains(keywords[max]))].tolist()
        big = False

        if not job_idxes:
            job_idxes = job_big.index[(job_big[0].str.contains(keywords[max]))].tolist()
            big = False if not job_idxes else True
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
                    
        sequences = [self.p.get_wordidx_sequence(keywords)]
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)


        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)
        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]
        return list(zip(keywords, tags))

    def predict_tags(self, query):
        # 형태소 분석
        pos = self.p.pos(query)

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)

        max = np.argmax(padded_seqs)
        job_idxes = job_mini.index[(job_mini[0].str.contains(keywords[max]))].tolist()
        big = False

        if not job_idxes:
            job_idxes = job_big.index[(job_big[0].str.contains(keywords[max]))].tolist()
            big = False if not job_idxes else True
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

        sequences = [self.p.get_wordidx_sequence(keywords)]

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1: continue
            tags.append(self.index_to_ner[tag_idx])

        if len(tags) == 0: return None
        return tags

