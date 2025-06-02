import allure
import pytest
import requests
from random_data import generate_updated_user_body
from urls import URL


@allure.feature('Пользователь: обновление данных')
class TestUpdateUserData:

    @allure.story('Изменение данных авторизованным пользователем')
    @allure.title('Успешное изменение поля {field} для авторизованного пользователя')
    @allure.description('''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Залогиниться (POST /api/auth/login) и получить токен.
        3. Сформировать body = {field: new_data}.
        4. Отправить PATCH запрос на /api/auth/user с заголовком Authorization и этим body.
        Ожидаем:
        - Код ответа 200.
        - Поле 'success': true.
        ''')
    @pytest.mark.parametrize('field, new_data', generate_updated_user_body())
    def test_update_user_data_when_logged_in_successfully(self, field, new_data, user_create_and_cleanup):
        with allure.step("Получить payload созданного пользователя из фикстуры"):
            payload = user_create_and_cleanup

        with allure.step('Выполнить логин и получить accessToken'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)
            token = response_login.json().get('accessToken')

        with allure.step(f'Сформировать тело запроса для обновления: поле {field} = {new_data}'):
            body = {field: new_data}

        with allure.step('Отправить PATCH запрос на обновление данных пользователя'):
            response_update = requests.patch(URL.UPDATE_USER_DATA_URL, headers={'Authorization': token}, json=body)

        with allure.step('Проверить, что код ответа == 200 и success == True'):
            assert response_update.status_code == 200
            assert response_update.json()['success'] == True

        payload[field] = new_data

    @allure.story('Изменение данных без авторизации')
    @allure.title('Ошибка при изменении поля {field} без токена')
    @allure.description('''
        Шаги:
        1. Сформировать body = {field: new_data} без заголовка Authorization.
        2. Отправить PATCH запрос на /api/auth/user.
        Ожидаем:
        - Код ответа 401.
        - Поле 'success': false.
        ''')
    @pytest.mark.parametrize('field, new_data', generate_updated_user_body())
    def test_update_user_data_when_not_logged_in_error(self, field, new_data):
        with allure.step(f'Сформировать тело запроса без токена: поле {field} = {new_data}'):
            body = {field: new_data}

        with allure.step('Отправить PATCH запрос без заголовка Authorization'):
            response_update = requests.patch(URL.UPDATE_USER_DATA_URL, json=body)

        with allure.step('Проверить, что код ответа == 401 и success == False'):
            assert response_update.status_code == 401
            assert response_update.json()['success'] == False