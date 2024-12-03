from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from .models import Session
from datetime import timedelta
from .utils.exceptions import HttpError

def create_app():
    '''Создание экземпляра приложения и системы авториазции через JWT токены, регистрация blueprint'''
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = '112233SecretKeyJWT'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=5)

    jwt = JWTManager(app)

    from .views.advertisements import advertisements_bp
    from .views.auth import auth_bp
    app.register_blueprint(advertisements_bp, url_prefix="/advertisement")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.before_request
    def before_request():
        '''Создание сессии до запроса - для подключения к бд'''
        session = Session()
        request.session = session

    @app.after_request
    def after_request(response):
        '''Закрытие сессии после запроса'''
        request.session.close()
        return response

    @app.errorhandler(HttpError)
    def error_handler(error: HttpError):
        '''Обработка ошибок для кореектного вывода пользователю'''
        response = jsonify({"error": error.error_message})
        response.status_code = error.status_code
        return response

    return app