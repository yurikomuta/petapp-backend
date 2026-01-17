from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models import TipoUsuario
from datetime import datetime
from app.models import StatusAula
 

# O que precisamos receber para criar um usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: TipoUsuario = TipoUsuario.TUTOR  # Padrão é Tutor

# O que vamos devolver para o app (NUNCA devolvemos a senha)
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: TipoUsuario
    
    class Config:
        from_attributes = True

# --- SCHEMAS DE PET ---
class PetBase(BaseModel):
    nome: str
    raca: Optional[str] = None
    peso: Optional[str] = None
    alergias: Optional[str] = None
    observacoes: Optional[str] = None
    # Foto deixaremos para depois

class PetCreate(PetBase):
    pass

class PetResponse(PetBase):
    id: int
    dono_id: int
    
    class Config:
        from_attributes = True

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