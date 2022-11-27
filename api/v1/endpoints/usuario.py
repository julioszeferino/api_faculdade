from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaArtigos, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# GET Logado: busca qual o usuario autenticado
@router.get('/logado', response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    """
    Operacao GET - Retorna o usuario que esta autenticado

    :param usuario_logado: Token do usuario que que fez a requisicao

    :return: Usuario autenticado
    """
    return usuario_logado

# POST / Sign Up: cria um novo usuario
# Para criar vou usar o UsuarioSchemaCreate, que e um JSON que contem a senha
# Contudo, para retornar a resposta, eu nao mostro a senha, usando o UsuarioSchemaBase
@router.post('/signup', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    """
    Operacao POST - Cria um novo usuario

    :param usuario: JSON com os dados do usuario
    :param session: Sessao do banco de dados

    :return: Usuario criado
    """
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin
    )

    async with db as session:
        # Verificando se o email ja existe
        query = select(UsuarioModel).where(UsuarioModel.email == usuario.email)
        result = await session.execute(query)
        usuario_existente: Optional[UsuarioModel] = result.scalars().unique().first()

        if usuario_existente:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Email ja cadastrado')

        # persistindo o usuario no banco de dados
        session.add(novo_usuario)
        await session.commit()

        return novo_usuario


# GET Usuario: busca todos os usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    """
    Operacao GET - Retorna todos os usuarios

    :param db: Sessao do banco de dados

    :return: Lista de usuarios
    """
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()

        return usuarios

# GET Usuario: busca um usuario pelo id
@router.get('/{id}', response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, db: AsyncSession = Depends(get_session)):
    """
    Operacao GET - Retorna um usuario pelo id

    :param id: Id do usuario
    :param db: Sessao do banco de dados

    :return: JSON com os artigos com usuario
    """
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario nao encontrado')

        return usuario


# PUT Usuario: atualiza um usuario pelo id
@router.put('/{id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    """
    Operacao GET - Retorna um usuario pelo id

    :param id: Id do usuario
    :param db: Sessao do banco de dados

    :return: JSON com os artigos com usuario
    """
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        # se o usuario nao existir, retorna 404
        if not usuario_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario nao encontrado')
        
       # se o usuario existir, verifica que campos foram passados e atualiza
        if usuario.nome:
            usuario_up.nome = usuario.nome
        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.eh_admin:
            usuario_up.eh_admin = usuario.eh_admin
        if usuario.senha:
            usuario_up.senha = gerar_hash_senha(usuario.senha)

        await session.commit()

        return usuario_up

# DELETE Usuario: deleta um usuario pelo id
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_session)):
    """
    Operacao DELETE - Deleta um usuario pelo id

    :param id: Id do usuario
    :param db: Sessao do banco de dados

    :return: None
    """
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        # se o usuario nao existir, retorna 404
        if not usuario_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario nao encontrado')
        
        # se o usuario existir, deleta
        await session.delete(usuario_del)
        await session.commit()
        
        # em geral retornariamos None, mas o FastAPI tem um bug por isso temos a linha abaixo
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# Autenticacao do Usuario
#POST login: autentica um usuario
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """
    Operacao POST - Autentica um usuario

    :param form_data: Dados do formulario
    :param db: Sessao do banco de dados

    :return: Token de acesso
    """
    usuario = await autenticar(
        email=form_data.username, 
        senha=form_data.password, 
        bd=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Email ou senha invalidos')

    # se autenticar, devolvemos o token de acesso para o usuario conseguir realizar as requisicoes
    return JSONResponse(
        content={
            'access_token': criar_token_acesso(sub=usuario.id), 
            'token_type': 'bearer'
        }, status_code=status.HTTP_200_OK)