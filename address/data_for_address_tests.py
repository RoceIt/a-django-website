"""Functions to create test address models."""

ADDRESS_NAME = 'address_name'
NAME = 'name'
NAME2 = 'name2'
STREET = 'street'
NUMBER = 'number'
BUS = 'bus'
POSTAL_CODE = 'postal_code'
CITY = 'city'
PROVINCE = 'province'
COUNTRY = 'country'

def full_address_n(n):
    return {
        ADDRESS_NAME: f'address_name_{n}',
        NAME: f'name_{n}',
        NAME2: f'name2_{n}',
        STREET: f'street_{n}',
        NUMBER: f'{n}',
        BUS: f'{n}',
        POSTAL_CODE: f'B{str(n)*4}',
        CITY: f'city_{n}',
        PROVINCE: f'province_{n}',
        COUNTRY: f'country_{n}',
    }
