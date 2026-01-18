from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime
from app.models import StatusAula


# Configuração de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- USUARIO ---
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

# --- PET ---
def criar_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    # Usa model_dump() (Pydantic v2) ou dict() se der erro
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

# --- CONTRATO ---
def criar_contrato(db: Session, contrato: schemas.ContratoCreate, prof_id: int):
    db_contrato = models.Contrato(
        tutor_id=contrato.tutor_id,
        profissional_id=prof_id,
        total_aulas=contrato.total_aulas,
        saldo_aulas=contrato.total_aulas
    )
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

def listar_contratos_do_profissional(db: Session, prof_id: int):
    return db.query(models.Contrato).filter(models.Contrato.profissional_id == prof_id).all()

# --- AULA ---
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
    if tipo_usuario == models.TipoUsuario.PROFISSIONAL:
        return db.query(models.Aula).join(models.Contrato).filter(models.Contrato.profissional_id == user_id).all()
    else:
        return db.query(models.Aula).join(models.Contrato).filter(models.Contrato.tutor_id == user_id).all()


# --- EXECUÇÃO DA AULA ---

def realizar_checkin(db: Session, aula_id: int):
    # Busca a aula
    db_aula = db.query(models.Aula).filter(models.Aula.id == aula_id).first()
    if not db_aula:
        return None
    
    # Atualiza horário e status
    db_aula.checkin_hora = datetime.now()
    db.commit()
    db.refresh(db_aula)
    return db_aula

def realizar_checkout(db: Session, aula_id: int, dados: schemas.AulaCheckout):
    db_aula = db.query(models.Aula).filter(models.Aula.id == aula_id).first()
    if not db_aula:
        return None

    # 1. Atualiza dados da aula
    db_aula.checkout_hora = datetime.now()
    db_aula.resumo_texto = dados.resumo_texto
    db_aula.nota_comportamento = dados.nota_comportamento
    db_aula.status = StatusAula.REALIZADA
    
    # 2. Busca o contrato vinculado para descontar o saldo
    db_contrato = db.query(models.Contrato).filter(models.Contrato.id == db_aula.contrato_id).first()
    if db_contrato and db_contrato.saldo_aulas > 0:
        db_contrato.saldo_aulas -= 1 # Desconta uma aula
    
    db.commit()
    db.refresh(db_aula)
    return db_aula