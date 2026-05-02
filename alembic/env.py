from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys  # para permitir editar no sistema
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # garante que o caminho da pasta raiz seja encontrado

# Objeto de configuração do Alembic (lê o alembic.ini)
config = context.config

# Configura o sistema de logging conforme definido no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa os metadados dos modelos para suporte ao autogenerate
from app.models import Base
target_metadata = Base.metadata  # Base.metadata contém as informações das tabelas (Paciente, Consulta)


def run_migrations_offline() -> None:
    """Executa as migrações em modo 'offline' (sem conexão ativa com o banco).

    Configura o contexto apenas com a URL do banco de dados.
    As chamadas a context.execute() emitem SQL diretamente na saída.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações em modo 'online' (com conexão ativa com o banco).

    Cria um Engine e associa uma conexão ao contexto do Alembic.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
