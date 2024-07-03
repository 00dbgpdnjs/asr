'''사용자 데이터(.mp3) 수신을 위한 form 정의'''

from flask_wtf import FlaskForm
from wtforms import MultipleFileField
from wtforms.validators import DataRequired # 데이터가 있을 때만 보내주고, 없으면 에러 (분석할 음성 파일을 안보내서)

class FileUploadForm(FlaskForm):
    '''사용자로부터 파일을 전송받을 폼'''
    # 1st: label
    files = MultipleFileField(
        '첨부파일',
        validators=[DataRequired()]
    )

