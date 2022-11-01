from requests import Session
from conf.configuracoes import PERSONAL_TOKEN, LOGIN

def _sessao_getter():
    return SESSAO

SESSAO = Session()
Session = _sessao_getter()


if LOGIN is not None or PERSONAL_TOKEN is not None:
    user = str(LOGIN)
    password = str(PERSONAL_TOKEN)
    SESSAO.auth = (user, password)

