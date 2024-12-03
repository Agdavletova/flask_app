from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.utils.exceptions import HttpError
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register/', methods=['POST'])
def register_user():
    """Регистрация пользователя"""
    json_data = request.json
    username = json_data.get('username')
    email = json_data.get('email')
    password = json_data.get('password')

    if not username or not email or not password:
        raise HttpError(400, "Необходимо заполнить все поля")

    session = request.session
    if session.query(User).filter_by(username=username).first():
        raise HttpError(400, "Пользователь с таким именем уже существует")

    user = User(**json_data)
    session.add(user)
    session.commit()
    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 201

@auth_bp.route('/login/', methods=['POST'])
def login_user():
    """Получение токена для пользователя"""
    json_data = request.json
    username = json_data.get('username')
    password = json_data.get('password')

    if not username or not password:
        raise HttpError(400, "Имя пользователя и пароль обязательны для получени токена")

    session = request.session
    user = session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        raise HttpError(401, "Неверное имя пользователя или пароль")