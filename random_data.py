from faker import Faker


faker = Faker()

def generate_user_register_body():

    return {
        'email': faker.email(domain='yandex.ru'),
        'password': faker.password(),
        'name': faker.user_name()
    }

def generate_updated_user_body():

    return [('email', faker.email(domain='yandex.ru')), ('name', faker.user_name())]
