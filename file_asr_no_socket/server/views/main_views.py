from flask import (
    Blueprint, # 웹에 라우팅이 많으면 발생할 순환참조 문제 (서로가 서로를 파일 참조/import)로 인한 에러 방지
    render_template,
)
 
bp = Blueprint('main', __name__, url_prefix='/') # 1st: 별명

@bp.route('/')
def index():
    '''메인 페이지'''
    return render_template('main.html')