import config
from flask import Flask
from ai_asr.inference import WhisperInference

whisper = WhisperInference()

def create_app() -> Flask:
    '''서비스용 앱 생성'''
    app = Flask(__name__) # __name__ : server/ 폴더명
    app.config.from_object(config)
    
    # Blueprint 등록
    from .views import main_views
    from .views import asr_file_views
    app.register_blueprint(main_views.bp) # 서버가 알 수 있게 등록
    app.register_blueprint(asr_file_views.bp) # 서버가 알 수 있게 등록
    
    
    return app