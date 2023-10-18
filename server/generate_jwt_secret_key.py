import secrets
import os

key_length = 134

secret_key = secrets.token_hex(key_length)

with open('.env', 'w') as env_file:
    env_file.write(f'SECRET_KEY={secret_key}\n')

print(f'Secret key generated and saved to .env file: {secret_key}')