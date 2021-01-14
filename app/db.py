import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# POSTGRESQL = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'scssf',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbvcn79q2e0c8',
        'USER': 'mwlitggifsvotw',
        'PASSWORD': 'mwlitggifsvotw',
        'HOST': 'ec2-34-202-5-87.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}