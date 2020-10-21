#!/usr/bin/env python

"""
Django SECRET_KEY generator.
"""
from django.utils.crypto import get_random_string


chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"

CONFIG_STRING = """
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS=127.0.0.1, .localhost
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=postgres
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
""".strip() % get_random_string(
    50, chars
)

# Writing our configuration file to '.env'
with open(".env", "w") as configfile:
    configfile.write(CONFIG_STRING)
