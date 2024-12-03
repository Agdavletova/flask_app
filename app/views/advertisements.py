from flask import Blueprint, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.exceptions import HttpError
from app.models import Advertisement

advertisements_bp = Blueprint("advertisements", __name__)

def get_adv_by_id(adv_id:int):
    '''Получение объявления по id'''
    adv = request.session.get(Advertisement, adv_id)
    if not adv:
        raise HttpError(404, "Нет объявления с таким id")
    return adv

def add_obj_database(obj):
    '''Добавление объекта в бд'''
    request.session.add(obj)
    request.session.commit()
    return obj

def get_all_adv():
    '''Получение всех объявлений'''
    advs = request.session.query(Advertisement).all()
    if not advs:
        raise HttpError(404, "Объявлений нет")
    return advs

class AdvertisementView(MethodView):
    '''Класс для работы с объявлениями
    get - получение всех объявлений или объявления по id - доступно всем;
    post - создание объявления - только авторизованный пользователь;
    patch - обновление объявления - только владелец объявления;
    delete - удаление объявлени - только владелец объявления;
    '''
    def get(self, adv_id:int = None):
        if adv_id:
            adv = get_adv_by_id(adv_id=adv_id)
            return jsonify(adv.dict)
        else:
            advs = get_all_adv()
            return jsonify([adv.dict for adv in advs])

    @jwt_required()
    def post(self):
        json_data = request.json
        current_user_id = int(get_jwt_identity())
        json_data["owner_id"] = current_user_id
        adv = Advertisement(**json_data)
        adv = add_obj_database(adv)
        return jsonify(adv.dict)

    @jwt_required()
    def patch(self, adv_id:int):
        json_data = request.json
        adv = get_adv_by_id(adv_id=adv_id)
        current_user_id = int(get_jwt_identity())
        if adv.owner_id != current_user_id:
            raise HttpError(403, "У вас нет прав на редактирование этого объвления")
        for field, value in json_data.items():
            setattr(adv, field, value)
        adv = add_obj_database(adv)
        return jsonify(adv.dict)

    @jwt_required()
    def delete(self, adv_id: int):
        adv = get_adv_by_id(adv_id=adv_id)
        current_user_id = int(get_jwt_identity())
        if adv.owner_id != current_user_id:
            raise HttpError(403, "У вас нет прав на удаление этого объвления")
        session = request.session
        session.delete(adv)
        session.commit()
        return jsonify({"message": "Удалено объвление"})


advertisement_view = AdvertisementView.as_view("advertisement")

advertisements_bp.add_url_rule(
    "/", view_func=advertisement_view, methods=['POST']
)

advertisements_bp.add_url_rule(
    "/<int:adv_id>/", view_func=advertisement_view, methods=['GET', 'PATCH', 'DELETE']
)

advertisements_bp.add_url_rule(
    "/all/", view_func=advertisement_view, methods=['GET']
)