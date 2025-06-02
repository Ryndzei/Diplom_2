import allure
import requests
from urls import URL
from random_data import generate_user_register_body
from data import TestData


@allure.feature('Пользователь: создание')
class TestCreateUser:

    @allure.story('Создание уникального пользователя')
    @allure.title('Создание нового пользователя — успех')
    @allure.description('''
        Шаги:
        1. Сгенерировать уникальный email, пароль и имя.
        2. Отправить POST запрос на /api/auth/register с этим payload.
        Ожидаем:
        - Код ответа 200.
        - Поле 'success': true.
        ''')
    def test_create_unique_user_successfully(self, user_cleanup):
        with allure.step('Сгенерировать уникальный payload для регистрации'):
            payload = generate_user_register_body()

        with allure.step('Передать фикстуре данные для последующей очистки'):
            user_cleanup.update(payload)

        with allure.step('Отправить POST запрос на регистрацию нового пользователя'):
            response_register = requests.post(URL.REGISTER_USER_URL, json=payload)

        with allure.step('Проверить, что код ответа == 200 и success == True'):
            assert response_register.status_code == 200
            assert response_register.json()['success'] == True

    @allure.story('Создание пользователя, который уже зарегистрирован')
    @allure.title('Ошибка при повторной регистрации того же пользователя')
    @allure.description('''
        Шаги:
        1. Сгенерировать payload (email, password, name).
        2. Зарегистрировать пользователя — ожидаем success = true, код 200.
        3. Попытаться снова зарегистрировать того же пользователя — ожидаем код 403.
        Ожидаем:
        - Код ответа 403.
        - Поле 'message': 'User already exists'.
        ''')
    def test_create_already_existed_user_error(self, user_cleanup):
        with allure.step('Сгенерировать payload для нового пользователя'):
            payload = generate_user_register_body()

        with allure.step('Передать фикстуре данные для очистки'):
            user_cleanup.update(payload)

        with allure.step('Первый запрос на регистрацию (должен пройти успешно)'):
            response_first_register = requests.post(URL.REGISTER_USER_URL, json=payload)
            assert response_first_register.status_code == 200 and response_first_register.json()['success'] == True

        with allure.step('Второй запрос на регистрацию тем же payload (ожидаем ошибку)'):
            response_second_register = requests.post(URL.REGISTER_USER_URL, json=payload)

        with allure.step('Проверить, что код ответа == 403 и сообщение User already exists'):
            assert response_second_register.status_code == 403
            assert response_second_register.json()['message'] == 'User already exists'

    @allure.story('Создание пользователя без одного из обязательных полей')
    @allure.title('Ошибка при отсутствии обязательного поля')
    @allure.description('''
        Шаги:
        1. Сформировать payload без поля 'email' (только 'password' и 'name').
        2. Отправить POST запрос на /api/auth/register.
        Ожидаем:
        - Код ответа 403.
        - Поле 'message': 'Email, password and name are required fields'.
        ''')
    def test_create_user_with_one_required_field_missing_error(self):
        with allure.step('Отправить POST запрос на /api/auth/register c неполным payload'):
            response_register = requests.post(URL.REGISTER_USER_URL, json=TestData.user_payload_with_no_required_field)

        with allure.step('Проверить, что код ответа == 403 и сообщение Email, password and name are required fields'):
            assert response_register.status_code == 403
            assert response_register.json()['message'] == 'Email, password and name are required fields'