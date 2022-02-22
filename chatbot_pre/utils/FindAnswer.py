class FindAnswer:
    def __init__(self, db):
        self.db = db

    def _make_query(self, intent_name, ner_tags):
        sql = "SELECT * FROM jobabot_train_data "
        if intent_name != None and ner_tags == None:
            sql = sql + f"WHERE intent = '{intent_name}' "

        elif intent_name != None and ner_tags != None:
            where = f'WHERE intent = "{intent_name}" '
            if (len(ner_tags) > 0):
                where += 'AND ('
                for ne in ner_tags:
                    where += f"ner LIKE '%{ne}%' OR "
                where = where[:-3] + ') '
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + "ORDER BY RAND() LIMIT 1 "
        return sql

    # 답변 검색
    def search(self, intent_name, ner_tags):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)

        return (answer['answers'])

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts:
            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'J_B_JOB' or tag == 'J_M_JOB' or tag == 'J_MAJOR' or tag == 'J_TELENT':
                answer = answer.replace(tag, word)

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
