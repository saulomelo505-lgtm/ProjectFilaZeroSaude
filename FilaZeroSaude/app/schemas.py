from pydantic import BaseModel
from typing import Optional


# Schemas de Paciente
class PacienteBase(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None  # Usado para envio de lembretes via SMS/WhatsApp


class PacienteCreate(PacienteBase):
    email: str
    senha: str
    nome: str
    telefone: str | None = None


class PacienteResponse(PacienteBase):
    id: int
    credencial: Optional[int] = None

    class Config:
        from_attributes = True


# Schemas de Consulta
class ConsultaBase(BaseModel):
    especialidade: str       # ex: Cardiologia, Clínica Geral, Ortopedia
    unidade_saude: str       # Unidade Básica de Saúde (UBS)
    data_consulta: str       # Formato: YYYY-MM-DD
    horario: str             # Formato: HH:MM


class ConsultaCreate(ConsultaBase):
    paciente_id: int


class ConsultaResponse(ConsultaBase):
    id: int
    paciente_id: int
    status: str              # pendente | confirmado | cancelado

    class Config:
        from_attributes = True