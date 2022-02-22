class FindAnswer:
    def __init__(self, db):
        self.db = db

    # 검색 쿼리 생성
    def _make_query(self, answer):
        sql = "select * from chatbot_train_data "
        sql = sql + f"where answer='{answer}' "
        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + "order by rand() limit 1 "
        return sql

    # 답변 검색
    def search(self, answer):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(answer)
        answer = self.db.select_one(sql)

        return (answer['answer'], answer['type'])

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_FOOD' or tag == 'B_DT' or tag == 'B_TI':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
