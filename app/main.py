from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session   
from app.database import engine, get_db
from app import models, schemas, crud

# Cria tabelas se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PetApp MVP")

@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    usuario_existente = crud.get_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Cria novo usuário
    return crud.criar_usuario(db=db, usuario=usuario)

@app.get("/")
def read_root():
    return {"mensagem": "API PetApp pronta para cadastros!"}