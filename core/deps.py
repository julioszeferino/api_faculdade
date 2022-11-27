from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel

class TokenData(BaseModel):
    username: Optional[str] = None


async def get_session() -> Generator:
    """
    Funcao responsavel por criar uma sessao com o banco de dados.
    """
    session: AsyncSession = Session()

    try: 
        yield session
    finally:
        await session.close()


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    """
    Funcao responsavel por retornar o usuario autenticado.
    """
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nao foi possivel autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # tentando decodificar o token do usuario tentando logar
        payload: dict = jwt.decode(
            token, 
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        # em cima do payload decodificado, vamos validar as informacoes:

        # recuperando o usuario
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        # recuperando o token
        token_data: TokenData = TokenData(username=username)

    except JWTError:
        # Nao foi possivel decodificar o token
        raise credentials_exception

    async with db as session:
        # validando se existe cadastro do usuario no bd
        query = select(UsuarioModel).where(UsuarioModel.id == int(token_data.username))
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credentials_exception

        return usuario