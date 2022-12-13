import hashlib
import base64
def my_hash(password:str):
    return base64.b64encode(hashlib.pbkdf2_hmac(
         'sha256', # The hash digest algorithm for HMAC
         password.encode('utf-8'), # Convert the password o ytes
         b'\r\xb26\xa2\xf9\xa2\xdb\xc2yu8R\x93\xf3;z\x16\xcf4@[\xfe\x90k\x9fX\xc9uV\x0c%\x9d', # Provide the salt
         100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )).decode("utf-8")
