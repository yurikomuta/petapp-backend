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


# --- FUNÇÕES DE CONTRATO ---
def criar_contrato(db: Session, contrato: schemas.ContratoCreate, prof_id: int):
    db_contrato = models.Contrato(
        tutor_id=contrato.tutor_id,
        profissional_id=prof_id, # Pega o ID de quem está logado (Adestrador)
        total_aulas=contrato.total_aulas,
        saldo_aulas=contrato.total_aulas
    )
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

def listar_contratos_do_profissional(db: Session, prof_id: int):
    return db.query(models.Contrato).filter(models.Contrato.profissional_id == prof_id).all()

# --- FUNÇÕES DE AULA ---
def criar_aula(db: Session, aula: schemas.AulaCreate):
    db_aula = models.Aula(
        contrato_id=aula.contrato_id,
        pet_id=aula.pet_id,
        data_agendada=aula.data_agendada
    )
    db.add(db_aula)
    db.commit()
    db.refresh(db_aula)
    return db_aula

def listar_aulas_por_usuario(db: Session, user_id: int, tipo_usuario: models.TipoUsuario):
    # Se for Profissional, busca aulas dos contratos onde ele é o profissional
    if tipo_usuario == models.TipoUsuario.PROFISSIONAL:
        return db.query(models.Aula).join(models.Contrato).filter(models.Contrato.profissional_id == user_id).all()
    
    # Se for Tutor, busca aulas dos contratos onde ele é o tutor
    else:
        return db.query(models.Aula).join(models.Contrato).filter(models.Contrato.tutor_id == user_id).all()