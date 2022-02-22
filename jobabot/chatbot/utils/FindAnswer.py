class FindAnswer:
    def __init__(self, db):
        self.db = db

    def _make_query(self, intent_name, ner_tag):
        intent_dic = {"자기소개": 1, "인사": 2, "막연한 질문": 3, "직업 관련 질문": 4, "학과 관련 질문": 5, "재능": 6, "끝맺음": 7}
        intent = intent_dic[intent_name]
        sql = "SELECT * FROM jobabot_train_data "
        if intent_name != None and ner_tag == None:
            sql = sql + f"WHERE label = {intent} "
        # elif intent_name != None and ner_tags != None:
        elif ner_tag != None:
            where = f"WHERE ner LIKE '%{ner_tag}%' "
            sql = sql + where
        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        if(intent == 5 and ((ner_tag is None) or ("J_MAJOR" not in ner_tag))):
            sql += "ORDER BY id DESC LIMIT 1 "
        elif intent in [1, 2, 3, 7]:
            sql += "ORDER BY RAND() LIMIT 1 "
        elif intent == 6 and ((ner_tag is None) or ("J_TELENT" not in ner_tag)):
            sql += "ORDER BY id DESC LIMIT 1 "
        elif intent == 4 and ((ner_tag is None) or ("J_B_JOB" not in ner_tag) or ("J_M_JOB" not in ner_tag)):
            sql += "ORDER BY id DESC LIMIT 1 "
        print(sql)
        return sql

    # 답변 검색
    def search(self, intent_name, ner_tag):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tag)
        answer = self.db.select_all(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_all(sql)
        return (answer)

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        print("predicts = ", ner_predicts)
        word, keyword, tag = ner_predicts
        ment = {"J_B_JOB": "해당 직군", "J_M_JOB": "해당 직업", "J_MAJOR": "해당 학과", "J_TELENT": "해당 능력"}
        description = {"major": 1, "big_mini": 2, "maj_mini": 3, "tel_mini": 4}
        
        for i in ment.keys():
            if i in answer:
                answer = answer.replace(i, word)
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        print("word = ", keyword)
        print("answer = ", answer)

        for i in description.keys():
            if i in answer:
                print("i = ", i)
                if description[i] == 5:
                    print(len(keyword), type(keyword))
                    print("result = ", self.get_telent(keyword))
                    answer = answer.replace(i, self.get_description(description[i], self.get_telent(keyword)))
                else:
                    print("durl?", self.get_description(description[i], keyword))
                    answer = answer.replace(i, self.get_description(description[i], keyword))
        print("ans = ", answer)
        return answer
    def get_description(self, section, word):
        sql = ""
        result = []
        if section == 1:
            sql = f"""SELECT major FROM job_major WHERE job LIKE '%{word}%'"""
            result = [i for i in self.db.select_all(sql)][0:3]
            result = [i["major"] for i in result]
        elif section == 2:
            sql = f"""SELECT job FROM job_seperate WHERE job_big LIKE '%{word}%'"""
            result = [i for i in self.db.select_all(sql)[0:3]]
            result = [i["job"] for i in result]
        elif section == 3:
            sql = f"""SELECT job FROM job_major WHERE major LIKE '%{word}%'"""
            print(sql)
            result = [i for i in self.db.select_all(sql)[0:3]]
            result = [i["job"] for i in result]
        elif section == 4:
            sql = f"""SELECT job FROM job_performance WHERE {word} > 0 ORDER BY {word} DESC LIMIT 3"""
            result = [i for i in self.db.select_all(sql)[0:3]]
            result = [i["job"] for i in result]
        result = str(result)[1:-1]
        print("result = ", result)
        return result
    def get_telent(self, tel):
        dic = {
            "읽고이해하기": "saq1",
            "듣고이해하기": "saq2",
            "글쓰기": "saq3",
            "말하기": "saq4",
            "수리력": "saq5",
            "논리적분석": "saq6",
            "창의력": "saq7",
            "범주화": "saq8",
            "기억력": "saq9",
            "공간지각력": "saq10",
            "추리력": "saq11",
            "학습전략": "saq12",
            "선택적집중력": "saq13",
            "모니터링": "saq14",
            "사람파악": "saq15",
            "행동조정": "saq16",
            "설득": "saq17",
            "협상": "saq18",
            "가르치기": "saq19",
            "서비스지향": "saq20",
            "문제해결": "saq21",
            "판단과의사결정": "saq22",
            "시간관리": "saq23",
            "재정관리": "saq24",
            "물적자원관리": "saq25",
            "인적자원관리": "saq26",
            "기술분석": "saq27",
            "기술설계": "saq28",
            "장비선정": "saq29",
            "설치": "saq30",
            "전산": "saq31",
            "품질관리분석": "saq32",
            "조작및통제": "saq33",
            "장비의유지": "saq34",
            "고장의발견.수리": "saq35",
            "작동점검": "saq36",
            "조직체계의분석및평가": "saq37",
            "정교한동작": "saq38",
            "움직임통제": "saq39",
            "반응시간과속도": "saq40",
            "신체적강인성": "saq41",
            "유연성및균형": "saq42",
            "시력": "saq43",
            "청력": "saq44"
        }
        return dic[tel]