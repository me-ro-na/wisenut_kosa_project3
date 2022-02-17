import pymysql
import pymysql.cursors
import logging

import sys
[sys.path.append(i) for i in ['.', '..']]
from project_name.chatbot.config.DatabaseConfig import *

class Database:
    '''
    database 제어
    '''
    def __init__(self):
        self.conn = None
    # DB 연결
    def connect(self):
        if self.conn != None:
            return
        self.conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8'
        )
    # DB 연결 닫기
    def close(self):
        if self.conn is None:
            return
        if not self.conn.open:
            self.conn = None
            return
        self.conn.close()
        self.conn = None
    # SQL 구문 실행
    def execute(self, sql):
        last_row_id = -1
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
            self.conn.commit()
            last_row_id = cursor.lastrowid
        except Exception as ex:
            logging.error(ex)
        finally:
            return last_row_id
    # SELECT 구문 실행 후, 단 1개의 데이터 ROW만 불러옴
    def select_one(self, sql):
        result = None
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
        except Exception as ex:
            logging.error(ex)
        finally:
            return result
    # SELECT 구문 실행 후, 전체 데이터 ROW만 불러옴
    def select_all(self, sql):
        result = None
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as ex:
            logging.error(ex)
        finally:
            return result