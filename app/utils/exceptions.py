from flask import jsonify


class HttpError(Exception):
    '''Клас для обработки ошибок и правильного отображения пользователю'''
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message
