"""This module contains every key helper needed inside the API."""


import os
import string
from secrets import choice
import bcrypt


LOG_ROUNDS = os.getenv("LOG_ROUNDS", default=12)
KEY_LENGTH = os.getenv("KEY_LENGTH", default=6)
ALPHABET = string.ascii_uppercase + string.digits


def generate_random_key():
    """
    Generates a random alphanumeric key of length :KEY_LENGTH
    with at least 3 uppercase characters and at least 1 digit.
    """
    # Based on the secrets module documentation
    while True:
        key = ''.join(choice(ALPHABET) for _ in range(int(KEY_LENGTH)))
        if (sum(c.isupper() for c in key) >= 3 and sum(
                c.isdigit() for c in key) >= 1):
            return key


def generate_key_digest(plain_key):
    """Digests a key using :LOG_ROUNDS log rounds."""
    return bcrypt.hashpw(
        plain_key.encode('utf-8'), bcrypt.gensalt(int(LOG_ROUNDS))
    ).decode()


def check_key(plain_key, key_digest):
    """Checks if :plain_key is the key to :key_digest"""
    plain_key = plain_key.encode('utf-8')
    key_digest = key_digest.encode('utf-8')
    return bcrypt.checkpw(plain_key, key_digest)
