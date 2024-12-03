import requests

#создание пользователя
#все уникально
response = requests.post("http://127.0.0.1:5000/auth/register/",
                         json={"username":"admin", "email":"admin@gmail.com", "password":"admin"})

#получение объвления по id
# response = requests.get("http://127.0.0.1:5000/advertisement/3")


#получение всех объявлений
# response = requests.get("http://127.0.0.1:5000/advertisement/all")

#получение токена
# response = requests.post("http://127.0.0.1:5000/auth/login/",
#                         json={
#                             "username":"admin0",
#                             "password":"admin0"
#                         },
#                         headers={
#                             "Content-Type": "application/json"
#                         })
#
# TOKEN_ADMIN_2 = response.json().get('access_token')
# response = requests.post("http://127.0.0.1:5000/auth/login/",
#                         json={
#                             "username":"admin10",
#                             "password":"admin10"
#                         },
#                         headers={
#                             "Content-Type": "application/json"
#                         })
# TOKEN_ADMIN_3 = response.json().get('access_token')


#создание объявления
# response = requests.post("http://127.0.0.1:5000/advertisement/",
#                          json={"title": "объявление 3",
#                                "description":"Описание 3"},
#                          headers={"Content-Type": "application/json",
#                                   "Authorization": f"Bearer {TOKEN_ADMIN_2}"})


#редактирование объявления
# response = requests.patch("http://127.0.0.1:5000/advertisement/4",
#                           json={
#                               "title":"Объявление 3 изменили"
#                           },
#                          headers={
#                              "Content-Type": "application/json",
#                              "Authorization": f"Bearer {TOKEN_ADMIN_3}"})


#удаление объявления
# response = requests.delete("http://127.0.0.1:5000/advertisement/4",
#                            headers={
#                                "Content-Type": "application/json",
#                                 "Authorization": f"Bearer {TOKEN_ADMIN_2}"})


print(response.status_code)
print(response.json())
