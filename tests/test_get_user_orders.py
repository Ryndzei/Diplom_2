import allure
import requests
from urls import URL
from data import TestData


@allure.feature('Заказы: получение заказов пользователя')
class TestGetUserOrders:

    @allure.story('Получение заказов авторизованным пользователем')
    @allure.title('Успешное получение списка своих заказов')
    @allure.description('''
        Шаги:
        1. С помощью фикстуры user_create_and_cleanup создать нового пользователя.
        2. Залогиниться (POST /api/auth/login) и получить токен.
        3. Отправить POST запрос на /api/orders, чтобы создать хотя бы один заказ.
        4. Отправить GET запрос на /api/orders с заголовком Authorization.
        Ожидаем:
        - Код ответа 200.
        - Поле 'success': true.
        ''')
    def test_get_user_orders_when_logged_in_successfully(self, user_create_and_cleanup):
        with allure.step('Получить payload созданного пользователя из фикстуры'):
            payload = user_create_and_cleanup

        with allure.step('Выполнить логин и получить accessToken'):
            response_login = requests.post(URL.LOGIN_USER_URL, json=payload)
            token = response_login.json().get('accessToken')

        with allure.step('Создать заказ для того же пользователя'):
            response_create_order = requests.post(URL.CREATE_ORDER_URL, headers={'Authorization': token}, json=TestData.create_order_valid_ingredients_body)
            assert response_create_order.status_code == 200 and response_create_order.json()['success'] == True

        with allure.step('Отправить GET запрос на получение заказов пользователя'):
            response_get_orders = requests.get(URL.GET_USER_ORDERS_URL, headers={'Authorization': token})

        with allure.step('Проверить, что код ответа == 200 и success == True'):
            assert response_get_orders.status_code == 200
            assert response_get_orders.json()['success'] == True

    @allure.story('Получение заказов без авторизации')
    @allure.title('Ошибка при попытке получить заказы без токена')
    @allure.description(f'''
        Шаги:
        1. Отправить GET запрос на /api/orders без заголовка Authorization.
        Ожидаем:
        - Код ответа 401.
        - Поле 'message': {TestData.you_should_be_authorised_message}.
        ''')
    def test_get_user_orders_when_not_logged_in_error(self):
        with allure.step("Отправить GET запрос на получение заказов без заголовка Authorization"):
            response_get_orders = requests.get(URL.GET_USER_ORDERS_URL)

        with allure.step(f'Проверить, что код ответа == 401 и сообщение {TestData.you_should_be_authorised_message}'):
            assert response_get_orders.status_code == 401
            assert response_get_orders.json()['message'] == TestData.you_should_be_authorised_message