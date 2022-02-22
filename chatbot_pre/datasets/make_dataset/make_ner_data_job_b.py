import csv
from konlpy.tag import Komoran
from random import  *
import os
from kiwipiepy import Kiwi

job_big_file = rf"{os.path.abspath('chatbot_pre/datasets/make_dataset/datas/job_big.csv')}"
sent_file = rf"{os.path.abspath('chatbot_pre/datasets/make_dataset/datas/data.csv')}"

kiwi = Kiwi()

file = open(rf"{os.path.abspath('chatbot_pre/datasets/make_dataset/datas/ner_output.txt')}", 'a', encoding='utf-8-sig')

job_sel = 10
while(job_sel >= 0) :
    with open(job_big_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            # if i != job_sel: continue

            sel = randint(0, 397)
            with open(sent_file, mode="r", encoding="utf-8") as qf:
                qreader = csv.reader(qf)
                for qi, qrow in enumerate(qreader):
                    if(qi != sel): continue

                    sentence = []
                    word = row[0].split(':')
                    sentence.append(tuple(word))

                    q = qrow[0]
                    q = q.replace('\ufeff', '')
                    pos = kiwi.analyze(q)[0][0]
                    for p in pos:
                        x = (p[0], 'O', p[1])
                        sentence.append(x)
                    break

                # 파일 저장
                raw_q = ";"
                res_q = '$'
                line = ""
                for i, s in enumerate(sentence):
                    raw_q += "{} ".format(s[0])
                    res_q += "{} ".format(s[0])
                    if s[1] == "J_B_JOB":
                        line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], 'NNG', s[1])
                    else:
                        line += "{}\t{}\t{}\t{}\n".format(i + 1, s[0], s[2], s[1])
                
                print(raw_q)
                print(res_q)
                print(line)
                file.write(raw_q + "\n")
                file.write(res_q + "\n")
                file.write(line + "\n")
                
            job_sel -= 1

file.close()