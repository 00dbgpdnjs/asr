from flask import (
    Blueprint, 
    render_template,
)
from server.forms import FileUploadForm # 서버 입장에서는 path가 server/ 부터 시작
 
bp = Blueprint('asr_file', __name__, url_prefix='/asr_file') 

@bp.route('/') # / = /asr_file
def index():
    '''메인 페이지'''
    form = FileUploadForm()
    return render_template(
        'asr_file.html',
        form=form, # 파라미터명을 asr_file.html에 form.csrf_token 즉 form과 똑같이
    )