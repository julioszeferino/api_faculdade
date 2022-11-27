from passlib.context import CryptContext

CRIPTO = CryptContext(
    schemes=["bcrypt"], # schema para criacao de hashs e senhas 
    deprecated="auto" # se algo for desativado, o tratamento sera automatico
    )

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    Funcao para verificar se a senha esta correta, comparando a senha
    em texto puro, informada pelo usuario, e o hash da senha que estara
    salvo no banco de dados durante a criacao da conta.
    """
    return CRIPTO.verify(senha, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    """
    Funcao para gerar e retornar hash da senha, que sera salvo no banco de dados
    durante a criacao da conta.
    """
    return CRIPTO.hash(senha)