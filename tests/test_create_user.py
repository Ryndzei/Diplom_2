import allure
import pytest
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
    @allure.description(f'''
        Шаги:
        1. Сгенерировать payload (email, password, name).
        2. Зарегистрировать пользователя — ожидаем success = true, код 200.
        3. Попытаться снова зарегистрировать того же пользователя — ожидаем код 403.
        Ожидаем:
        - Код ответа 403.
        - Поле 'message': {TestData.user_already_exists_message}.
        ''')
    def test_create_already_existed_user_error(self, user_create_and_cleanup):
        with allure.step('Использовать уже зарегистрированный payload для нового пользователя'):
            payload = user_create_and_cleanup

        with allure.step('Запрос на регистрацию тем же payload (ожидаем ошибку)'):
            response_second_register = requests.post(URL.REGISTER_USER_URL, json=payload)

        with allure.step(f'Проверить, что код ответа == 403 и сообщение {TestData.user_already_exists_message}'):
            assert response_second_register.status_code == 403
            assert response_second_register.json()['message'] == TestData.user_already_exists_message

    @allure.story('Создание пользователя без одного из обязательных полей')
    @allure.title('Ошибка при отсутствии обязательного поля')
    @allure.description(f'''
        Шаги:
        1. Сформировать payload без поля 'email' (только 'password' и 'name').
        2. Отправить POST запрос на /api/auth/register.
        Ожидаем:
        - Код ответа 403.
        - Поле 'message': '{TestData.fields_required_message}'.
        ''')
    @pytest.mark.parametrize(
        "payload, missing_field",[
        (TestData.user_payload_with_no_required_field_email, "email"),
        (TestData.user_payload_with_no_required_field_password, "password")
        ],
        ids=["missing email", "missing password"]
    )
    def test_create_user_with_missing_required_field_error(self, payload, missing_field):
        with allure.step(f'Отправить POST запрос на /api/auth/register c неполным payload (без {missing_field})'):
            response_register = requests.post(URL.REGISTER_USER_URL, json=payload)

        with allure.step(f'Проверить, что код ответа == 403 и сообщение {TestData.fields_required_message}'):
            assert response_register.status_code == 403
            assert response_register.json()['message'] == TestData.fields_required_message