
class URL:

    BASE_URL = 'https://stellarburgers.nomoreparties.site/'
    REGISTER_USER_URL = f'{BASE_URL}api/auth/register'
    LOGIN_USER_URL = f'{BASE_URL}api/auth/login'
    UPDATE_USER_DATA_URL = f'{BASE_URL}api/auth/user'
    DELETE_USER_URL = f'{BASE_URL}api/auth/user'

    CREATE_ORDER_URL = f'{BASE_URL}api/orders'
    GET_USER_ORDERS_URL = f'{BASE_URL}api/orders'