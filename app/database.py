import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração da URL do Banco
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://petadmin:petsecret@localhost/petapp_db")

# Motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os Models
Base = declarative_base()

# Função para pegar a sessão do banco (Dependência)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()