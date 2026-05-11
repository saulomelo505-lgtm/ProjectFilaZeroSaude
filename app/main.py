from fastapi import FastAPI
from dotenv import load_dotenv # para importar arquivos do env 
from app.models import Base, db

load_dotenv()

Base.metadata.create_all(bind=db) # executa a criação dos metadados do banco/ cria ou ignora caso ja tenha 


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