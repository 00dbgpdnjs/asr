import os
from datetime import datetime
from flask import (
    Blueprint, 
    render_template,
    request,
)
from werkzeug.utils import secure_filename
from config import UPLOAD_FILE_DIR
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

@bp.route('/upload/<user_id>', methods=['POST'])
def upload(user_id):
    # 파일 저장
    print(f'user_id: {user_id}')
    print('upload func working...')
    
    # 서버에 파일 저장
    user_upload_dir = os.path.join(UPLOAD_FILE_DIR, user_id)
    if not os.path.exists(user_upload_dir):
        os.mkdir(user_upload_dir)
    
    files = request.files.getlist('file') # 1st: attach_file_handler_no_socketio.js saveFilesToForm()에서 file라는 키값으로 append해서
    for file in files:
        print(f'file.name: {file.name}')
        prefix_name = f"{datetime.now().strftime('%y%m%d_%H_%M_%S.%f')}_." # ex. 20280623_00_12_34.327_.
        safe_filename = prefix_name + secure_filename(file.filename)
        print(f'safe_filename: {safe_filename}')
        file.save(os.path.join(user_upload_dir, safe_filename))
    return {
        'status': 'ok'
    }

@bp.route('/process', methods=['POST'])
def process():
    # ASR 인공지능 수행
    return '결과 텍스트'