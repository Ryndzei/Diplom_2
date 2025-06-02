import allure
import requests
from urls import URL
from random_data import generate_user_register_body


@allure.feature('Пользователь: авторизация')
class TestLoginUser:

    @allure.story('Логин под существующим пользователем')
    @allure.title('Успешный логин с корректными данными')
    @allure.description('''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Отправить POST запрос на /api/auth/login с email и password.
        Ожидаем:
        - Код ответа 200.
        - Поле 'success': true.
        ''')
    def test_login_with_existed_user_data_successfully(self, user_create_and_cleanup):
        with allure.step('Получить payload созданного пользователя из фикстуры'):
            payload = user_create_and_cleanup

        with allure.step('Отправить POST запрос на логин'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)

        with allure.step('Проверить статус-код 200 и наличие success == True'):
            assert response_login.status_code == 200
            assert response_login.json()['success'] == True

    @allure.story('Логин с неверными данными')
    @allure.title('Ошибка при неверном email или пароле')
    @allure.description('''
        Шаги:
        1. Сгенерировать случайный payload, не зарегистрированный в системе.
        2. Отправить POST запрос на /api/auth/login.
        Ожидаем:
        - Код ответа 401.
        - Поле 'message': 'email or password are incorrect'.
        ''')
    def test_login_with_wrong_user_data_error(self):
        with allure.step('Сгенерировать несуществующие email и password'):
            payload = generate_user_register_body()

        with allure.step('Отправить POST запрос на логин с неверными данными'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)

        with allure.step('Проверить код ответа 401 и сообщение об ошибке'):
            assert response_login.status_code == 401
            assert response_login.json()['message'] == 'email or password are incorrect'