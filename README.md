# 🏥 Fila Zero Saúde

Sistema serverless na AWS para gerenciamento inteligente de consultas médicas no SUS.


## 📌 O Problema

No SUS, milhares de consultas são desperdiçadas diariamente porque:
• Pacientes esquecem a consulta agendada
• Não conseguem confirmar ou cancelar com facilidade
• A vaga fica ociosa enquanto outros esperam meses na fila

**Efeito:** desperdício de dinheiro público, filas enormes e pessoas doentes sem atendimento.



## 💡 A Solução

Uma plataforma simples e gratuita que:
• Envia **lembretes automáticos** de consultas via SMS
• Permite ao paciente **confirmar ou cancelar com 1 clique**
• **Repassa automaticamente** a vaga cancelada para o próximo da fila



## ☁️ Arquitetura AWS

• colocar o arquivo 

### Serviços utilizados

### Armazenamento e Hospedagem
Amazon S3 — Hospedagem de site estático
### Backend e APIs
API Gateway — Exposição dos endpoints REST
AWS Lambda — Lógica de confirmação e cancelamento
### Banco de Dados
Amazon DynamoDB — Armazenamento de consultas e pacientes
### Comunicação e Eventos
Amazon SNS — Envio de SMS
Amazon EventBridge — Disparo automático de lembretes
### Segurança
AWS WAF — Proteção da API contra ataques
Amazon VPC — Isolamento e segurança da infraestrutura


## 👥 Time

 Nome 
| Guilherme Castro | Gustavo Neves | Henry Aguiar | Mateus Mecula | Saulo Vehuel | Suelen V. |
