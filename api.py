import json
import requests


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и password"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str='') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_create_pet(self, auth_key: json, name: str, animal_type: str,
                        age: int, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str,
                        age: int) -> json:
        """Метод обновляет информацию о питомце по указанному ID.
        Возвращает статус запроса и result в формате JSON с обновленными данными питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод отправляет запрос на удаление питомца по указанному ID.
        Возвращает ствтус запроса и результат в формате JSON с текстом о успешном удалении"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def post_create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос с данными для создания питомца без фото.
        Возвращает статус запроса и результат в формате JSON с данными созданного питомца"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def post_add_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер запрос о добавлении питомцу новой фотографии или изменении текущей и возвращает
        статус запроса на сервер и результат в формате JSON с данными питомца"""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=file)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result
