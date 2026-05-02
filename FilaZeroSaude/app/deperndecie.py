from app.models import db
from sqlalchemy.orm import sessionmaker  # para criar uma sessão no banco de dados (sempre ao criar, finaliza)

"""
    Dependência reutilizável do FastAPI para gerenciamento de sessão do banco de dados.
    Substitui a criação manual de sessão a cada rota, garantindo abertura e fechamento corretos.
"""

def pegarSessão():
    """
    Gera e gerencia uma sessão de banco de dados para o sistema Fila Zero Saúde.
    Utilizado via Depends() nas rotas do FastAPI para injeção de dependência.
    """
    try:
        Sassion = sessionmaker(bind=db)  # criar uma sessão vinculada ao banco de dados
        session = Sassion()              # cria a conexão com o banco de dados
        yield session                   # retorna sem encerrar a função (padrão gerador do FastAPI)
    finally:                            # executa ao final, com ou sem erro
        session.close()