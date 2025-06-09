
class TestData:

    user_payload_with_no_required_field_email = {
            'password': '123456789',
            'name': 'Nikolay'
        }

    user_payload_with_no_required_field_password = {
        'email': 'test@yandex.ru',
        'name': 'Nikolay'
    }

    create_order_valid_ingredients_body = {
            'ingredients': ['61c0c5a71d1f82001bdaaa6f', '61c0c5a71d1f82001bdaaa79']
    }

    create_order_no_ingredients_body = {
        'ingredients': []
    }

    create_order_wrong_hash_ingredients_body = {
        'ingredients': ['62c0c5a71d1f82001bdaaa6f', '62c0c5a71d1f82001bdaaa79']
    }