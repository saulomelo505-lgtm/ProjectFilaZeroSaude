import os
from passlib.context import CryptContext # pega o texto e combina com uma chave secreta 

SECRET_KEY = os.getenv("SECRET_KEY") # pegar a chave secreta no env 
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # como um indicador para criptografar ou comparar se as chaves são iguais mesmo criptografadas