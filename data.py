
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

    user_already_exists_message = 'User already exists'

    fields_required_message = 'Email, password and name are required fields'

    you_should_be_authorised_message = 'You should be authorised'

    ingredient_ids_must_be_provided_message = 'Ingredient ids must be provided'

    one_or_more_ids_provided_are_incorrect_message = 'One or more ids provided are incorrect'

    email_or_password_are_incorrect = 'email or password are incorrect'