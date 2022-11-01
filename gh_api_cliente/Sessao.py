from requests import Session
from conf.configuracoes import PERSONAL_TOKEN, LOGIN

"""
Define uma sessão comum, com login predefinido, para realizar todas as requisições
"""

SESSAO = Session()
def _sessao_getter():
    return SESSAO

if LOGIN is not None or PERSONAL_TOKEN is not None:
    user = str(LOGIN)
    password = str(PERSONAL_TOKEN)
    SESSAO.auth = (user, password)
Session = _sessao_getter()

