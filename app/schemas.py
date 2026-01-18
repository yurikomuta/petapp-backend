from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import TipoUsuario, StatusAula

# --- USUARIO ---
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: TipoUsuario = TipoUsuario.TUTOR

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: TipoUsuario
    
    class Config:
        from_attributes = True

# --- PET ---
class PetBase(BaseModel):
    nome: str
    raca: Optional[str] = None
    peso: Optional[str] = None
    alergias: Optional[str] = None
    observacoes: Optional[str] = None

class PetCreate(PetBase):
    pass

class PetResponse(PetBase):
    id: int
    dono_id: int
    class Config:
        from_attributes = True

# --- CONTRATO ---
class ContratoCreate(BaseModel):
    tutor_id: int
    total_aulas: int = 10

class ContratoResponse(BaseModel):
    id: int
    tutor_id: int
    profissional_id: int
    saldo_aulas: int
    ativo: bool
    class Config:
        from_attributes = True

# --- AULA ---
class AulaCreate(BaseModel):
    contrato_id: int
    pet_id: Optional[int] = None
    data_agendada: datetime

class AulaResponse(BaseModel):
    id: int
    data_agendada: datetime
    status: StatusAula
    pet_id: Optional[int]
    class Config:
        from_attributes = True

# --- CHECK-OUT ---
class AulaCheckout(BaseModel):
    resumo_texto: str
    nota_comportamento: int # 1 a 5
    # Futuramente aqui entrará a foto (Upload)

