from fastapi import APIRouter, Depends, HTTPException
from app.models import Paciente
from app.dependence import pegarSessão
from app.Security.security import bcrypt_context
from app.schemas import PacienteCreate

user_router = APIRouter(prefix="/auth", tags=["auth"])
"""
    Rotas de autenticação e cadastro de pacientes do sistema Fila Zero Saúde.
"""
# prefix="/auth" --> dominio/auth/...
# tags=["auth"]  --> agrupa as rotas na documentação automática do FastAPI


@user_router.post('/criarConta')  # POST pois envia dados para criar um recurso no servidor
async def criarConta(Dados: PacienteCreate, session=Depends(pegarSessão)):
    """
    Cadastra um novo paciente no sistema Fila Zero Saúde.
    O telefone é utilizado para envio de lembretes de consulta via SMS/WhatsApp.
    """
    
    paciente = session.query(Paciente).filter(Paciente.email == Dados.email).first()  # pega a tabela Paciente no banco e filtra o email == com o que ntrou agr e pega o ultimo 

    if paciente:  # se já existe um paciente com esse e-mail
        raise HTTPException(status_code=400, detail="E-mail do paciente já cadastrado")
        # HTTPException -> retorna código HTTP com mensagem de erro
        # status_code   -> código do erro ou sucessos
        # detail        -> mensagem descritiva

    else:  # se não existe, cria o novo paciente  
        if len(Dados.senha.encode("utf-8")) > 72: #encode transforma em byte("utf-8" é a forma como o computador transforma texto (letras) em bytes (números))
           raise HTTPException(status_code=400, detail="Senha muito longa") # raise serve para forçar a interrupção do código e avisar que algo deu errado.
        
        senha_criptografada = bcrypt_context.hash(Dados.senha) #transforma uma senha comum em uma sequência longa, irreversível que é o hash 
        
        novoPaciente = Paciente(nome=Dados.nome, email=Dados.email, senha=senha_criptografada, telefone= Dados.telefone)
        session.add(novoPaciente)
        session.commit()  # salva as alterações no banco de dados
        return {"mensagem": f"Paciente {Dados.nome} cadastrado com sucesso no Fila Zero Saúde!"}