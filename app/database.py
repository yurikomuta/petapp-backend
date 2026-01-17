import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pega a URL do docker-compose ou usa um padrão local se falhar
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://petadmin:petsecret@localhost/petapp_db")

# Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria a sessão (o que usamos para mandar queries)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para nossos modelos (tabelas) herdarem
Base = declarative_base()

# Função utilitária para pegar o banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        