import bcrypt


def encrypt_string(string: str):
    bytes = string.encode("utf-8")
    salt = bcrypt.gensalt()
    encrypted_bytes = bcrypt.hashpw(bytes, salt)
    encrypted_string = encrypted_bytes.decode("utf-8")
    return encrypted_string


# encrypt = encrypt_string("abc123")


# db_password = {"password": encrypt}
# db_password = db_password.get("password")
# db_password_bytes = db_password.encode("utf-8")


def compare_password(user_password: bytes, db_password_bytes: bytes) -> bool:
    user_password_bytes = user_password.encode("utf-8")

    result = bcrypt.checkpw(user_password_bytes, db_password_bytes)
    return result


# print(compare_password("abc123", db_password_bytes))

#jwt 
#oAuth
