# __init__.py

from .auth import auth


def token(token_value):
    auth.set_token(token_value)
