from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.database import engine, get_db
from app import models, schemas, crud, auth

# Cria as tabelas no banco ao iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PetApp MVP")

# --- ROTA DE SAÚDE (Teste) ---
@app.get("/")
def read_root():
    return {"mensagem": "API PetApp está online!"}

# --- ROTA DE LOGIN (Gera o Token) ---
@app.post("/token")
def login_para_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # O Swagger envia o email no campo 'username'
    usuario = crud.get_usuario_por_email(db, email=form_data.username)
    
    if not usuario or not crud.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.criar_token_acesso(
        data={"sub": usuario.email, "id": usuario.id, "tipo": usuario.tipo.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTAS DE USUÁRIOS (Públicas) ---
@app.post("/usuarios/", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = crud.get_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.criar_usuario(db=db, usuario=usuario)

# --- ROTAS DE PETS (Protegidas pelo Cadeado) ---
@app.post("/pets/", response_model=schemas.PetResponse)
def criar_pet(
    pet: schemas.PetCreate, 
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user) # <--- O CADEADO VEM DAQUI
):
    return crud.criar_pet(db=db, pet=pet, user_id=current_user.id)

@app.get("/pets/", response_model=List[schemas.PetResponse])
def listar_meus_pets(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    return crud.listar_pets_do_usuario(db=db, user_id=current_user.id)

# --- ROTAS DE CONTRATO (Só Profissional cria) ---
@app.post("/contratos/", response_model=schemas.ContratoResponse)
def criar_contrato(
    contrato: schemas.ContratoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo != models.TipoUsuario.PROFISSIONAL:
        raise HTTPException(status_code=403, detail="Apenas profissionais podem criar contratos")
    
    return crud.criar_contrato(db=db, contrato=contrato, prof_id=current_user.id)

@app.get("/contratos/", response_model=List[schemas.ContratoResponse])
def listar_meus_contratos(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    return crud.listar_contratos_do_profissional(db=db, prof_id=current_user.id)

# --- ROTAS DE AULA ---
@app.post("/aulas/", response_model=schemas.AulaResponse)
def agendar_aula(
    aula: schemas.AulaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # (Idealmente checaríamos se o contrato pertence ao profissional, mas pro MVP simplificamos)
    return crud.criar_aula(db=db, aula=aula)

@app.get("/aulas/", response_model=List[schemas.AulaResponse])
def listar_minhas_aulas(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    return crud.listar_aulas_por_usuario(db=db, user_id=current_user.id, tipo_usuario=current_user.tipo)


# --- ROTAS DE EXECUÇÃO (Check-in / Check-out) ---

@app.patch("/aulas/{aula_id}/checkin", response_model=schemas.AulaResponse)
def checkin_aula(
    aula_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    # Apenas Profissionais podem dar check-in
    if current_user.tipo != models.TipoUsuario.PROFISSIONAL:
        raise HTTPException(status_code=403, detail="Apenas profissionais iniciam aulas")
        
    aula = crud.realizar_checkin(db, aula_id)
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    return aula

@app.post("/aulas/{aula_id}/checkout", response_model=schemas.AulaResponse)
def checkout_aula(
    aula_id: int,
    dados: schemas.AulaCheckout,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    if current_user.tipo != models.TipoUsuario.PROFISSIONAL:
        raise HTTPException(status_code=403, detail="Apenas profissionais finalizam aulas")
        
    aula = crud.realizar_checkout(db, aula_id, dados)
    if not aula:
        raise HTTPException(status_code=404, detail="Aula não encontrada")
    return aula