from fastapi import FastAPI
from passlib.context import CryptContext # pega o texto e combina com uma chave secreta 
from dotenv import load_dotenv # para importar arquivos do env 
import os 
from app.models import Base, db

load_dotenv()

Base.metadata.create_all(bind=db)
print(Base.metadata.tables.keys())

SECRET_KEY = os.getenv("SECRET_KEY") # pegar a chave secreta no env 
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # como um indicador para criptografar ou comparar se as chaves são iguais mesmo criptografadas

app = FastAPI(
    title="Fila Zero Saúde",
    description="API para redução de faltas em consultas médicas públicas (SUS). Permite agendamento, confirmação, cancelamento e repasse automático de vagas.",
    version="1.0.0"
)

from app.Rotas.consult_routes import consulta_router
from app.Rotas.user_routes import user_router
# Rotas.study_routes --> na pasta Rotas no arquivo study_routes (importado a partir da pasta app/)
app.include_router(consulta_router)
app.include_router(user_router)
# o app (variável que instancia o FastAPI) vai incluir as rotas importadas