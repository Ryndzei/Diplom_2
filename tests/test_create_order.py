import allure
import requests
from urls import URL
from data import TestData


@allure.feature('Заказы: создание')
class TestCreateOrder:

    @allure.story('Создание заказа авторизованным пользователем')
    @allure.title('Успешное создание заказа для авторизованного пользователя')
    @allure.description('''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Залогиниться (POST /api/auth/login) и получить токен.
        3. Отправить POST запрос на /api/orders с заголовком Authorization и валидным списком ингредиентов.
        Ожидаем:
        - Код ответа 200.
        - Поле 'success': true.
        ''')
    def test_create_order_when_logged_in_successfully(self, user_create_and_cleanup):
        with allure.step('Получить payload созданного пользователя из фикстуры'):
            payload = user_create_and_cleanup

        with allure.step('Выполнить логин и получить accessToken'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)
            token = response_login.json().get('accessToken')

        with allure.step('Отправить POST запрос на создание заказа c корректным телом'):
            response_create_order = requests.post(URL.CREATE_ORDER_URL, headers={'Authorization': token}, json=TestData.create_order_valid_ingredients_body)

        with allure.step('Проверить, что код ответа == 200 и success == True'):
            assert response_create_order.status_code == 200
            assert response_create_order.json()['success'] == True

    @allure.story('Создание заказа без авторизации')
    @allure.title('Ошибка при создании заказа без токена')
    @allure.description(f'''
        Шаги:
        1. Отправить POST запрос на /api/orders без заголовка Authorization, но с валидным списком ингредиентов.
        Ожидаем:
        - Код ответа 401.
        - Поле 'message': '{TestData.you_should_be_authorised_message}.
        ''')
    def test_create_order_when_not_logged_in_error(self):
        with allure.step('Отправить POST запрос на создание заказа без токена и с корректным телом'):
            response_create_order = requests.post(URL.CREATE_ORDER_URL, json=TestData.create_order_valid_ingredients_body)

        with allure.step(f'Проверить, что код ответа == 401 и сообщение {TestData.you_should_be_authorised_message}'):
            assert response_create_order.status_code == 401
            assert response_create_order.json()['message'] == TestData.you_should_be_authorised_message

    @allure.story('Создание заказа без ингредиентов')
    @allure.title('Ошибка при создании заказа без ингредиентов')
    @allure.description(f'''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Залогиниться (POST /api/auth/login) и получить токен.
        3. Отправить POST запрос на /api/orders с пустым массивом ingredients.
        Ожидаем:
        - Код ответа 400.
        - Поле 'message': {TestData.ingredient_ids_must_be_provided_message}.
        ''')
    def test_create_order_without_ingredients_error(self, user_create_and_cleanup):
        with allure.step('Получить payload созданного пользователя из фикстуры'):
            payload = user_create_and_cleanup

        with allure.step('Выполнить логин и получить accessToken'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)
            token = response_login.json().get('accessToken')

        with allure.step('Отправить POST запрос на создание заказа с пустым списком ингредиентов в теле'):
            response_create_order = requests.post(URL.CREATE_ORDER_URL, headers={'Authorization': token}, json=TestData.create_order_no_ingredients_body)

        with allure.step(f'Проверить, что код ответа == 400 и сообщение {TestData.ingredient_ids_must_be_provided_message}'):
            assert response_create_order.status_code == 400
            assert response_create_order.json()['message'] == TestData.ingredient_ids_must_be_provided_message

    @allure.story('Создание заказа с неверными хешами ингредиентов')
    @allure.title('Ошибка при создании заказа с неправильными хешами ингредиентов')
    @allure.description(f'''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Залогиниться (POST /api/auth/login) и получить токен.
        3. Отправить POST запрос на /api/orders с несуществующими id ингредиентов.
        Ожидаем:
        - Код ответа 400.
        - Поле 'message': {TestData.one_or_more_ids_provided_are_incorrect_message}.
        ''')
    def test_create_order_with_wrong_ingredients_hash_error(self, user_create_and_cleanup):
        with allure.step('Получить payload созданного пользователя из фикстуры'):
            payload = user_create_and_cleanup

        with allure.step('Выполнить логин и получить accessToken'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)

        with allure.step('Отправить POST запрос на создание заказа с неверными id'):
            token = response_login.json().get('accessToken')
            response_create_order = requests.post(URL.CREATE_ORDER_URL, headers={'Authorization': token}, json=TestData.create_order_wrong_hash_ingredients_body)

        with allure.step(f'Проверить код ответа 400 и сообщение {TestData.one_or_more_ids_provided_are_incorrect_message}'):
            assert response_create_order.status_code == 400
            assert response_create_order.json()['message'] == TestData.one_or_more_ids_provided_are_incorrect_message
