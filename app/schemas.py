from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models import TipoUsuario
 
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