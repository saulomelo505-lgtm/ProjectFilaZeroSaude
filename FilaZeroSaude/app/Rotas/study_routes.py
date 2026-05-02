from fastapi import APIRouter, Depends, HTTPException
from app.models import Consulta, Paciente
from app.deperndecie import pegarSessão

consulta_router = APIRouter(prefix="/consultas", tags=["consultas"])
"""
    Rotas de gerenciamento de consultas médicas do sistema Fila Zero Saúde.
    Permite agendar, confirmar, cancelar consultas e visualizar a fila de espera,
    além de repassar vagas automaticamente para o próximo paciente da fila.
"""


@consulta_router.get("/")  # rota.requisição("Caminho") -> decorator
async def listar_consultas(session=Depends(pegarSessão)):
    """Lista todas as consultas cadastradas no sistema."""
    consultas = session.query(Consulta).all()
    return [
        {
            "id": c.id,
            "paciente_id": c.paciente_id,
            "especialidade": c.especialidade,
            "unidade_saude": c.unidade_saude,
            "data_consulta": c.data_consulta,
            "horario": c.horario,
            "status": c.status
        }
        for c in consultas
    ]


@consulta_router.post("/agendar")
async def agendar_consulta(
    paciente_id: int,
    especialidade: str,
    unidade_saude: str,
    data_consulta: str,
    horario: str,
    session=Depends(pegarSessão)
):
    """
    Agenda uma nova consulta médica para um paciente.
    Status inicial: pendente (aguardando confirmação do paciente).
    """
    paciente = session.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    nova_consulta = Consulta(
        paciente_id=paciente_id,
        especialidade=especialidade,
        unidade_saude=unidade_saude,
        data_consulta=data_consulta,
        horario=horario,
        status="pendente"
    )
    session.add(nova_consulta)
    session.commit()

    # Simula envio de lembrete (em produção: Amazon SNS / WhatsApp Business API)
    _enviar_lembrete(paciente, nova_consulta)

    return {
        "mensagem": f"Consulta agendada com sucesso! ID: {nova_consulta.id}",
        "status": "pendente"
    }


@consulta_router.patch("/confirmar/{consulta_id}")
async def confirmar_consulta(consulta_id: int, session=Depends(pegarSessão)):
    """
    Confirma a presença do paciente na consulta médica.
    Chamado quando o paciente responde 'SIM' ao lembrete recebido via SMS/WhatsApp.
    """
    consulta = session.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    if consulta.status == "cancelado":
        raise HTTPException(status_code=400, detail="Esta consulta já foi cancelada")

    consulta.status = "confirmado"
    session.commit()

    return {
        "mensagem": "Consulta confirmada com sucesso!",
        "consulta_id": consulta_id,
        "status": "confirmado"
    }


@consulta_router.patch("/cancelar/{consulta_id}")
async def cancelar_consulta(consulta_id: int, session=Depends(pegarSessão)):
    """
    Cancela a consulta médica e repassa a vaga para o próximo da fila.
    Chamado quando o paciente responde 'NÃO' ao lembrete recebido via SMS/WhatsApp.
    O sistema notifica automaticamente o próximo paciente disponível.
    """
    consulta = session.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    if consulta.status == "confirmado":
        raise HTTPException(status_code=400, detail="Não é possível cancelar uma consulta já confirmada")

    consulta.status = "cancelado"
    session.commit()

    # Repassa vaga automaticamente para o próximo da fila
    resultado_repasse = _repassar_vaga_para_fila(consulta, session)

    return {
        "mensagem": "Consulta cancelada. Vaga repassada para o próximo da fila.",
        "consulta_id": consulta_id,
        "status": "cancelado",
        "repasse": resultado_repasse
    }


@consulta_router.get("/fila/{especialidade}")
async def ver_fila(especialidade: str, session=Depends(pegarSessão)):
    """
    Lista as consultas pendentes para uma especialidade médica.
    Representa a fila de espera de pacientes aguardando atendimento.
    """
    fila = session.query(Consulta).filter(
        Consulta.especialidade == especialidade,
        Consulta.status == "pendente"
    ).all()

    return {
        "especialidade": especialidade,
        "total_na_fila": len(fila),
        "fila": [
            {
                "id": c.id,
                "paciente_id": c.paciente_id,
                "data_consulta": c.data_consulta,
                "horario": c.horario
            }
            for c in fila
        ]
    }


def _enviar_lembrete(paciente, consulta):
    """
    Simula o envio de lembrete ao paciente via SMS/WhatsApp.

    Em produção: integrar com Amazon SNS (SMS) ou WhatsApp Business API.

    Exemplo de mensagem enviada 24h antes da consulta (via Amazon EventBridge):
    'Olá {nome}! Você confirma sua consulta de {especialidade} amanhã às {horario}?
     Responda SIM | NÃO. Fila Zero Saúde.'
    """
    contato = paciente.telefone or paciente.email
    print(f"[SIMULAÇÃO - LEMBRETE] Enviado para {paciente.nome} ({contato})")
    print(f"  -> Especialidade : {consulta.especialidade}")
    print(f"  -> Unidade       : {consulta.unidade_saude}")
    print(f"  -> Data/Hora     : {consulta.data_consulta} às {consulta.horario}")
    return True


def _repassar_vaga_para_fila(consulta_cancelada, session):
    """
    Repassa automaticamente a vaga cancelada para o próximo paciente na fila de espera.

    Em produção:
    - Amazon EventBridge dispara o processo de repasse automaticamente.
    - O próximo paciente recebe uma notificação via Amazon SNS (SMS) ou WhatsApp.
    - A vaga nunca fica ociosa, reduzindo desperdício no sistema público de saúde.
    """
    print(f"[SIMULAÇÃO - REPASSE] Repassando vaga de {consulta_cancelada.especialidade} para próximo da fila...")
    # Em produção: buscar fila de espera, notificar próximo paciente e agendar nova consulta
    return {
        "status": "simulado",
        "mensagem": "Em produção: próximo paciente seria notificado automaticamente via SMS/WhatsApp"
    }