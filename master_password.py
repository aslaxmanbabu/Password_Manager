from hashlib import sha256
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
from base64 import b64decode, b64encode

salt = b'0010'


def query_master_pwd(master_password, second_FA_location):
    master_password_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

    compile_factor_together = sha256(
        master_password + second_FA_location).hexdigest()

    if compile_factor_together == master_password_hash:
        return True


def encrypt_password(password_to_encrypt, master_password_hash):

    key = PBKDF2(str(master_password_hash), salt).read(32)
    data_convert = str.encode(password_to_encrypt)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data_convert)
    add_nonce = ciphertext + nonce
    encoded_ciphertext = b64encode(add_nonce).decode()
    return encoded_ciphertext


def decrypt_password(password_to_encrypt, master_password_hash):

    if len(password_to_encrypt) % 4:
        password_to_encrypt += '=' * (4 - len(password_to_encrypt) % 4)

    convert = b64decode(password_to_encrypt)
    key = PBKDF2(str(master_password_hash), salt).read(32)
    nonce = convert[-16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(convert[:-16])
    return plaintext
