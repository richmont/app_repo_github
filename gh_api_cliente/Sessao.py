from requests import Session
from conf.configuracoes import PERSONAL_TOKEN, LOGIN
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Sessao")
"""
Define uma sessão comum, com login predefinido, para realizar todas as requisições
"""


def _sessao_getter():
    SESSAO = Session()
    if LOGIN is not None or PERSONAL_TOKEN is not None:
        logger.debug("Login e personal token válidos, usando autenticação")
        user = str(LOGIN)
        password = str(PERSONAL_TOKEN)
        SESSAO.auth = (user, password)
    else:
        logger.debug("Login e personal token inválidos, usando API limitada")
    return SESSAO


Session = _sessao_getter()

