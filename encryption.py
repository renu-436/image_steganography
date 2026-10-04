import os
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password, salt):
    """
    Convert the user's password into a Fernet encryption key.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000
    )

    key = kdf.derive(password.encode("utf-8"))

    return base64.urlsafe_b64encode(key)


def encrypt_message(message, password):
    """
    Encrypt a message using the user's password.
    Returns:
        salt, encrypted_data
    """

    # Generate a random salt
    salt = os.urandom(16)

    # Generate encryption key
    key = derive_key(password, salt)

    # Create Fernet cipher
    cipher = Fernet(key)

    # Encrypt message
    encrypted_data = cipher.encrypt(
        message.encode("utf-8")
    )

    return salt, encrypted_data


def decrypt_message(encrypted_data, password, salt):
    """
    Decrypt encrypted data using the user's password.

    Returns:
        Original message if password is correct.
        None if password is incorrect or data is invalid.
    """

    try:
        key = derive_key(password, salt)

        cipher = Fernet(key)

        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data.decode("utf-8")

    except (InvalidToken, UnicodeDecodeError, ValueError):
        return None