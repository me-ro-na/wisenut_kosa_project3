from flask import Blueprint, render_template, request
import os

from pj3.templates.job_experience import get_job_experience
from pj3.templates.charts import charts

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

# 서브페이지
@bp.route('/maps')
def map():
    lists = get_job_experience.get_data()
    addrs = get_job_experience.get_addrs("전체", "전체")
    jobs = get_job_experience.get_jobs("전체", "전체")
    switchs = {0.0: 0, 1.0: 1, 2.0: 2, 3.0: 3, 4.0: 4, 5.0: 5}
    return render_template('maps.html', lists=lists, switchs=switchs, addrs=addrs, jobs=jobs)

# 기타 잡
@bp.route('/get_fors', methods=("GET",))
def get_fors():
    addr = request.values.get("addr")
    jobs = request.values.get("jobs")
    return {"fors": get_job_experience.get_fors(addr, jobs)}

@bp.route('/get_jobs', methods=("GET",))
def get_jobs():
    addr = request.values.get("addr")
    fors = request.values.get("fors")
    return {"jobs": get_job_experience.get_jobs(addr, fors)}

@bp.route('/get_addrs', methods=("GET",))
def get_addrs():
    jobs = request.values.get("jobs")
    fors = request.values.get("fors")
    return {"addrs": get_job_experience.get_addrs(fors, jobs)}

@bp.route('/get_search_result', methods=("GET",))
def get_search_result():
    addr = request.values.get("addr")
    jobs = request.values.get("jobs")
    fors = request.values.get("fors")
    result = str(get_job_experience.get_search_result(addr, fors, jobs))
    return {"result_lists": result}

@bp.route('/get_modal_data', methods=("GET",))
def get_modal_data():
    data_no = request.values.get("dataNo")
    result = get_job_experience.get_modal_data(data_no)
    return {"modal_data": result}



# ---------------- 차트 데이터 ----------------
@bp.route('/get_chart1', methods=("GET",))
def get_chart1():
    chart1 = charts.get_data_chart1()
    labels = chart1["대분류"].values.tolist()
    values = chart1["sum"].values.tolist()
    return {"labels": labels, "values": values}

@bp.route('/get_chart2', methods=("GET",))
def get_chart2():
    chart2 = charts.get_data_chart2()
    labels = chart2["job"].values.tolist()
    values = chart2["bq30_1"].values.tolist()
    return {"labels": labels, "values": values}

@bp.route('/get_chart3', methods=("GET",))
def get_chart3():
    chart3 = charts.get_data_chart3()
    labels = chart3["대분류"].values.tolist()
    values = chart3["bq3"].values.tolist()
    return {"labels": labels, "values": values}

@bp.route('/get_chart4', methods=("GET",))
def get_chart4():
    chart3 = charts.get_data_chart4()
    labels = chart3["job"].values.tolist()
    values = chart3["bq19"].values.tolist()
    return {"labels": labels, "values": values}




# ---------------- 챗봇 서버 ----------------
@bp.route('/server', methods=("POST",))
def server():
    import socket
    import json
    # 챗봇 엔진 서버 접속 정보
    host = "182.215.79.79"  # 챗봇 엔진 서버 IP 주소
    port = 5050  # 챗봇 엔진 서버 통신 포트
    query = request.form["query"]
    result = ""
    if query != "quit":
        # 챗봇 엔진 서버 연결
        mySocket = socket.socket()
        mySocket.connect((host, port))
        print(mySocket.getsockname())
        # 챗봇 엔진 질의 요청
        json_data = {
            'Query': query
        }
        message = json.dumps(json_data)
        mySocket.send(message.encode())

        # 챗봇 엔진 답변 출력
        data = mySocket.recv(2048).decode()
        result = json.loads(data)
    return result