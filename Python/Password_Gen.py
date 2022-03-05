import secrets
import string

Password_length = 8

chars = string.digits + string.ascii_letters #+ string.punctuation 

print(''.join(secrets.choice(chars) for _ in range(Password_length)))