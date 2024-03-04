from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200 и в запросе содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_create_pet_with_valid_data(name='Тигренок', animal_type='Полосатик', age=4, pet_photo='images/tiger.jpg'):
    """Проверяем, что можно добавить питомца с валидными данными"""

    # Получаем полный путь к изображению питомца и сохраняем в перменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ auth_key и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)
    assert result["pet_photo"] != ""


def test_put_update_pet_info_for_valid_data(name="Тигр", animal_type='Кот', age=7):
    """Проверяем, что обновление информации о питомце работает"""

    # Запрашиваем ключ auth_key и получаем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то обновляем имя, тип животного и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # проверяем, что статус ответа == 200 и измененные данные соответствуют заданным
        assert status == 200
        assert result['name'] == name
        assert result['animal_type'] == animal_type
        assert result['age'] == str(age)
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("У вас пока нет питомцев")


def test_successful_delete_pet_by_id():
    """Проверяем возможность удаления питомца"""

    # Запрашиваем ключ auth_key и получаем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список пустой, то создаем нового питомца и запрашиваем список своих питомцев
    if 0 == len(my_pets['pets']):
        pf.post_create_pet_simple(auth_key, "Рысь", "Кошка", 10)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берем ID первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что статус == 200 и в списке питомцев нет ID удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_post_create_pet_simple_for_valid_data(name='Цейс', animal_type='Собака', age=1):
    """Проверяем, что можно добавить питомца без фото с валидными данными"""

    # Запрашиваем ключ auth_key и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)


def test_post_add_photo_pet_with_valid_data():
    """Проверяем возможность добавить питомцу фотографию или заменить текущее фото на новое"""

    # Запрашиваем ключ auth_key и получаем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем в переменную pet_photo путь к фотографии
    pet_photo = 'images/dog1.jpeg'

    # Получаем полный путь к изображению питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Сохраняем текущее значение pet_photo
    current_photo = my_pets['pets'][0]["pet_photo"]

    # Если список не пустой, то добавляем фото питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что статус ответа == 200 и фотография питомца изменилась
        assert status == 200
        assert result["pet_photo"] != current_photo
    else:

        # Если список пустой, то создаем нового питомца и запрашиваем список своих питомцев
        pf.post_create_pet_simple(auth_key, "Рысь", "Кошка", 10)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        status, result = pf.post_add_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что статус ответа == 200 и фотография питомца изменилась
        assert status == 200
        assert result["pet_photo"] != current_photo
