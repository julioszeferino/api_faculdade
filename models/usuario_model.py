from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class UsuarioModel(settings.DB_BASE_MODEL):
    
    __tablename__ = "usuarios"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=True)
    sobrenome: str = Column(String(256), nullable=True)
    email: str = Column(String(256), nullable=False, index=True, unique=True)
    senha: str = Column(String(256), nullable=False)
    eh_admin: bool = Column(Boolean, default=False)

    artigos = relationship(
        "ArtigoModel", 
        back_populates="criador", 
        lazy='joined', 
        cascade="all,delete-orphan",
        uselist=True)