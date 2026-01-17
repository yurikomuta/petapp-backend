from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from typing import List

# Configuração da senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- FUNÇÕES DE USUÁRIO ---

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    senha_hash = pwd_context.hash(usuario.senha)
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        tipo=usuario.tipo
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def verificar_senha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)

# --- FUNÇÕES DE PETS (PROTEGIDAS) ---

def criar_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    # O **pet.model_dump() converte o objeto em um dicionário
    # Se der erro de versão do Pydantic antigo, use pet.dict()
    db_pet = models.Pet(
        **pet.model_dump(), 
        dono_id=user_id
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def listar_pets_do_usuario(db: Session, user_id: int):
    return db.query(models.Pet).filter(models.Pet.dono_id == user_id).all()