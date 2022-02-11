from flask import Blueprint, render_template, request

import datetime

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

# 서브페이지
@bp.route('/maps')
def mango():
    return render_template('maps-gmap.html')