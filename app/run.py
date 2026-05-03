import uvicorn

# O Uvicorn é quem liga o projeto e deixa acessível no navegador
# Alternativa: uvicorn app.main:app --reload (direto no terminal)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)    # uvicorn.run() cria um servidor usando o Uvicorn
    # main  -- nome do arquivo : app -- nome da variável que instanciou o FastAPI no arquivo main
    # reload=True -- recarrega automaticamente as alterações sem precisar reiniciar o servidor