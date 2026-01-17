from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

# Configuração da criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def criar_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # 1. Criptografa a senha
    senha_hash = pwd_context.hash(usuario.senha)
    
    # 2. Cria o objeto do banco
    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        tipo=usuario.tipo
    )
    
    # 3. Salva
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario