import allure
import pytest
import requests
from random_data import generate_user_register_body
from urls import URL


@pytest.fixture
def user_cleanup():
    payload = {}
    yield payload

    with allure.step("POST /auth/login — получаем token для удаления"):
        login_response = requests.post(URL.LOGIN_USER_URL, json=payload)
        assert login_response.status_code == 200
        token = login_response.json().get('accessToken')

    with allure.step("DELETE /auth/user — удаляем пользователя по полученному token"):
        delete_response = requests.delete(URL.DELETE_USER_URL, headers={'Authorization': token})

        assert delete_response.status_code == 202
        assert delete_response.json().get('message') == 'User successfully removed'

@pytest.fixture
def user_create_and_cleanup():
    with allure.step("POST /auth/register — создаем пользователя"):
        payload = generate_user_register_body()
        response_register = requests.post(URL.REGISTER_USER_URL, json=payload)
        assert response_register.status_code == 200 and response_register.json()['success'] == True

    yield payload

    with allure.step("POST /auth/login — получаем token для удаления"):
        login_response = requests.post(URL.LOGIN_USER_URL, json=payload)
        assert login_response.status_code == 200
        token = login_response.json().get('accessToken')

    with allure.step("DELETE /auth/user — удаляем пользователя по полученному token"):
        delete_response = requests.delete(URL.DELETE_USER_URL, headers={'Authorization': token})

        assert delete_response.status_code == 202
        assert delete_response.json().get('message') == 'User successfully removed'
