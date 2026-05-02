# ALtera direto no banco de dados 
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Date, Time
from sqlalchemy.orm import declarative_base

# criar uma conexão com o banco de dados
db = create_engine("sqlite:///banco.db") # create_engine(link do banco de dados) /// é o padrão do SQLite

# criar a base do nosso banco de dados
Base = declarative_base() # parâmetro que permite criar tabelas no banco (subclasse)

# Status possíveis para uma consulta médica
STATUS_CONSULTA = (
    ("pendente", "Pendente"),
    ("confirmado", "Confirmado"),
    ("cancelado", "Cancelado"),
)

# Tabela: Paciente (id, nome, email, senha, credencial, telefone)
class Paciente(Base):
    __tablename__ = "Paciente" # definir o nome da tabela

    id = Column("id", Integer, primary_key=True, autoincrement=True) # chave primária, incrementa automaticamente
    nome = Column("nome", String) # nome completo do paciente
    email = Column("email", String, nullable=False) # nullable=False = não pode ser nulo
    senha = Column("senha", String, nullable=False)
    credencial = Column("credencial", Integer) # nível de acesso do usuário
    telefone = Column("telefone", String) # número de telefone para envio de lembretes (SMS/WhatsApp)

    #def __init__(self, nome, email, senha, credencial=None, telefone=None):
     #   self.nome = nome
      #  self.email = email
       # self.senha = senha
        #self.credencial = credencial
     #   self.telefone = telefone


# Tabela: Consulta (id, paciente_id, especialidade, unidade_saude, data_consulta, horario, status)
class Consulta(Base):
    __tablename__ = "Consulta"

    # STATUS: pendente | confirmado | cancelado

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    paciente_id = Column("paciente_id", ForeignKey("Paciente.id")) # ForeignKey("Paciente.id") --> chave estrangeira
    especialidade = Column("especialidade", String) # ex: Cardiologia, Clínica Geral, Ortopedia
    unidade_saude = Column("unidade_saude", String) # Unidade Básica de Saúde (UBS) responsável
    data_consulta = Column("data_consulta", Date) # Data da consulta no formato YYYY-MM-DD
    horario = Column("horario", Time) # Horário da consulta no formato HH:MM
    status = Column("status", String) # Status atual: pendente, confirmado ou cancelado

     # O PROPRIO SQLALQHEMI DEFINE O TIPO DA ENTRADA 

    #def __init__(self, paciente_id, especialidade, unidade_saude, data_consulta, horario, status="pendente"):
     #   self.paciente_id = paciente_id
     #   self.especialidade = especialidade
     #   self.unidade_saude = unidade_saude
     #   self.data_consulta = data_consulta
     #   self.horario = horario
     #   self.status = status

# executa a criação dos metadados do banco (efetiva a criação das tabelas)