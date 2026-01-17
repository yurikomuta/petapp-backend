from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

# --- ENUMS (Opções fixas) ---
class TipoUsuario(str, enum.Enum):
    TUTOR = "tutor"
    PROFISSIONAL = "profissional"

class StatusAula(str, enum.Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"

# --- TABELAS ---

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    tipo = Column(Enum(TipoUsuario), default=TipoUsuario.TUTOR)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    pets = relationship("Pet", back_populates="dono")
    
    # Contratos onde ele é o tutor
    contratos_como_tutor = relationship("Contrato", foreign_keys="[Contrato.tutor_id]", back_populates="tutor")
    # Contratos onde ele é o profissional
    contratos_como_prof = relationship("Contrato", foreign_keys="[Contrato.profissional_id]", back_populates="profissional")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    dono_id = Column(Integer, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)
    raca = Column(String, nullable=True)
    peso = Column(String, nullable=True) # String para facilitar "10kg"
    alergias = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    foto_url = Column(String, nullable=True)

    dono = relationship("Usuario", back_populates="pets")
    aulas = relationship("Aula", back_populates="pet")


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(Integer, ForeignKey("usuarios.id"))
    profissional_id = Column(Integer, ForeignKey("usuarios.id"))
    total_aulas = Column(Integer, default=10)
    saldo_aulas = Column(Integer, default=10)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    tutor = relationship("Usuario", foreign_keys=[tutor_id], back_populates="contratos_como_tutor")
    profissional = relationship("Usuario", foreign_keys=[profissional_id], back_populates="contratos_como_prof")
    aulas = relationship("Aula", back_populates="contrato")


class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"))
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=True)
    
    data_agendada = Column(DateTime, nullable=False)
    status = Column(Enum(StatusAula), default=StatusAula.AGENDADA)
    
    # Dados do Relatório (Check-out)
    checkin_hora = Column(DateTime, nullable=True)
    checkout_hora = Column(DateTime, nullable=True)
    resumo_texto = Column(Text, nullable=True)
    nota_comportamento = Column(Integer, nullable=True) # 1 a 5
    midia_url = Column(String, nullable=True) # Link da foto/video

    contrato = relationship("Contrato", back_populates="aulas")
    pet = relationship("Pet", back_populates="aulas")