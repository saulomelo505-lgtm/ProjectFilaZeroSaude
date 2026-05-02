# Fila Zero Saúde

Sistema de redução de faltas em consultas médicas públicas do SUS.

## O Problema

No SUS, milhares de consultas e exames são perdidos diariamente porque:
- Pacientes esquecem a consulta
- Não conseguem confirmar ou cancelar a tempo
- A vaga fica ociosa enquanto outras pessoas esperam meses na fila

**Resultado:** desperdício de dinheiro público, filas enormes e pessoas doentes sem atendimento.

## A Solução

Plataforma simples e gratuita que:
- Envia **lembretes automáticos** de consultas (WhatsApp/SMS)
- Permite ao paciente **confirmar ou cancelar com 1 clique**
- **Repassa automaticamente** a vaga cancelada para o próximo da fila

## Fluxo Principal

1. Paciente agenda consulta → sistema registra com status `pendente`
2. 24h antes, paciente recebe SMS/WhatsApp:  
   _"Você confirma sua consulta de Cardiologia amanhã às 10h? SIM | NÃO"_
3. Se **confirmar** → status muda para `confirmado`, consulta mantida
4. Se **cancelar** → status muda para `cancelado`, vaga repassada automaticamente ao próximo da fila

## Rotas da API

| Método | Rota                              | Descrição                                    |
|--------|-----------------------------------|----------------------------------------------|
| POST   | /auth/criarConta                  | Cadastrar novo paciente                      |
| GET    | /consultas/                       | Listar todas as consultas                    |
| POST   | /consultas/agendar                | Agendar nova consulta médica                 |
| PATCH  | /consultas/confirmar/{id}         | Confirmar presença na consulta               |
| PATCH  | /consultas/cancelar/{id}          | Cancelar e repassar vaga para fila           |
| GET    | /consultas/fila/{especialidade}   | Ver fila de espera por especialidade         |

## Tecnologias

- **FastAPI** — Framework web assíncrono
- **SQLAlchemy** — ORM / Banco de dados (SQLite para desenvolvimento)
- **Alembic** — Migrações de banco de dados
- **Uvicorn** — Servidor ASGI
- **Passlib (bcrypt)** — Criptografia de senhas

## Como Executar

```bash
cd app
pip install -r requirements.txt
python run.py
```

Acesse a documentação interativa: `http://localhost:8000/docs`

## Migrações do Banco de Dados

```bash
alembic revision --autogenerate -m "descrição da migração"
alembic upgrade head
```

## Arquitetura AWS (Produção)

| Serviço              | Função                                              |
|----------------------|-----------------------------------------------------|
| **S3**               | Frontend estático para confirmação/cancelamento     |
| **API Gateway**      | Exposição das rotas da API                          |
| **AWS Lambda**       | Lógica de confirmação e cancelamento                |
| **DynamoDB**         | Armazenamento de consultas, pacientes e status      |
| **Amazon SNS**       | Envio de SMS de lembrete                            |
| **Amazon EventBridge** | Disparo automático de lembretes 24h antes         |

---

*Fila Zero Saúde — Reduzindo desperdício e salvando vidas na saúde pública.*

### Comandos úteis do Alembic
```
alembic revision --autogenerate -m "descrição"  # gera nova migração baseada nos modelos
alembic upgrade head                              # aplica todas as migrações pendentes
```
