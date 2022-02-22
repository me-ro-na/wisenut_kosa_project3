from ast import keyword
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import os
import pandas as pd

# 전처리 객체 생성
job_mini = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datas/job_mini.csv")}', header=None)
job_big = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datas/job_big.csv")}', header=None)
telent = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datas/interest.csv")}', header=None)
major = pd.read_csv(rf'{os.path.abspath("jobabot/chatbot/datas/jobmajor.csv")}', header=None)

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
    def predict(self, query, intent):
        # 형태소 분석
        pos = self.p.pos(query)
        intent_dic = {"자기소개": 1, "인사": 2, "막연한 질문": 3, "직업 관련 질문": 4, "학과 관련 질문": 5, "재능": 6, "끝맺음": 7}
        intent = intent_dic[intent]
        print(intent)
        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
        
        # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)

        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]

        max = np.argmax(padded_seqs)
        tag = tags[max]
        keyword = None

        if intent == 6:
            interest_idx = telent.index[(telent[0].str.contains(keywords[max]))].tolist()
            if interest_idx:
                keyword = keywords[max]
                keywords[max] = telent[0][interest_idx[0]].split(":")[0]
                # keywords[max] = telent[0][interest_idx[0]].split(":")[0]
                # if len(interest_idx) > tmp:
                #     for i in range(1, tmp):
                #         keywords.append(telent[0][interest_idx[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 4 or intent == 3:
            # print(keywords[max])
            job_idxes = job_big.index[(job_big[0].str.contains(keywords[max]))].tolist()
            mini = False
            print(job_idxes)
            if not job_idxes:
                job_idxes = job_mini.index[(job_mini[0].str.contains(keywords[max]))].tolist()
                print("job!!!: ", job_idxes)
                mini = False if not job_idxes else True
            if job_idxes and mini == True:
                keyword = keywords[max]
                keywords[max] = job_mini[0][job_idxes[0]].split(":")[0]
                tag = "J_M_JOB"
                # keywords[max] = )job_mini[0][job_idxes[0]].split(":")[0]
                # if len(job_idxes) > tmp:
                    # for i in range(1, tmp):
                        # keywords.append(job_mini[0][job_idxes[i]].split(":")[0])
                mini = False
            elif job_idxes and mini == False:
                keyword = keywords[max]
                keywords[max] = job_big[0][job_idxes[0]].split(":")[0]
                tag = "J_B_JOB"
                # keywords[max] = job_big[0][job_idxes[0]].split(":")[0]
                # if len(job_idxes) > tmp:
                    # for i in range(1, tmp:
                        # keywords.append(job_big[0][job_idxes[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 5:
            major_idx = major.index[(major[0].str.contains(keywords[max]))].tolist()
            if major_idx:
                keyword = keywords[max]
                keywords[max] = major[0][major_idx[0]].split(":")[0]
                # keywords[max] = major[0][major_idx[0]].split(":")[0]
                # if len(major_idx) > tmp:
                    # for i in range(1, tmp):
                        # keywords.append(major[0][major_idx[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 1 or intent == 2 or intent == 7:
            return None
        # else:
        #     return None

        if keyword is None: return None
        
        return (keywords[max], keyword, tag)

    def predict_tags(self, query, intent):
        # 형태소 분석
        pos = self.p.pos(query)
        intent_dic = {"자기소개": 1, "인사": 2, "막연한 질문": 3, "직업 관련 질문": 4, "학과 관련 질문": 5, "재능": 6, "끝맺음": 7}
        intent = intent_dic[intent]

        # 문장내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

        # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, padding="post", value=0, maxlen=max_len)
        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)

        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1: continue
            tags.append(self.index_to_ner[tag_idx])
        if len(tags) == 0: return None

        max = np.argmax(padded_seqs)
        keyword = None
        tag = tags[max]

        if intent == 6:
            interest_idx = telent.index[(telent[0].str.contains(keywords[max]))].tolist()
            if interest_idx:
                keyword = keywords[max]
                keywords[max] = telent[0][interest_idx[0]].split(":")[0]
                # keywords[max] = telent[0][interest_idx[0]].split(":")[0]
                # if len(interest_idx) > tmp:
                #     for i in range(1, tmp):
                #         keywords.append(telent[0][interest_idx[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 4 or intent == 3:
            # print(keywords[max])
            job_idxes = job_big.index[(job_big[0].str.contains(keywords[max]))].tolist()
            mini = False
            if not job_idxes:
                job_idxes = job_mini.index[(job_mini[0].str.contains(keywords[max]))].tolist()
                mini = False if not job_idxes else True
            if job_idxes and mini == True:
                keyword = keywords[max]
                keywords[max] = job_mini[0][job_idxes[0]].split(":")[0]
                tag = "J_M_JOB"
                # keywords[max] = )job_mini[0][job_idxes[0]].split(":")[0]
                # if len(job_idxes) > tmp:
                    # for i in range(1, tmp):
                        # keywords.append(job_mini[0][job_idxes[i]].split(":")[0])
                mini = False
            elif job_idxes and mini == False:
                keyword = keywords[max]
                keywords[max] = job_big[0][job_idxes[0]].split(":")[0]
                tag = "J_B_JOB"
                # keywords[max] = job_big[0][job_idxes[0]].split(":")[0]
                # if len(job_idxes) > tmp:
                    # for i in range(1, tmp:
                        # keywords.append(job_big[0][job_idxes[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 5:
            major_idx = major.index[(major[0].str.contains(keywords[max]))].tolist()
            if major_idx:
                keyword = keywords[max]
                keywords[max] = major[0][major_idx[0]].split(":")[0]
                # keywords[max] = major[0][major_idx[0]].split(":")[0]
                # if len(major_idx) > tmp:
                    # for i in range(1, tmp):
                        # keywords.append(major[0][major_idx[i]].split(":")[0])
            # else:
            #     keyword = None
        elif intent == 1 or intent == 2 or intent == 7:
            return None
        # else:
        #     return None

        if keyword is None: return None
        
        
        return tag

