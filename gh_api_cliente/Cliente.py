from conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Cliente")

class ClienteBase():
    def __init__(self, api_url:str, timeout: int = 3) -> None:
        self._api_url = api_url
        self._timeout = timeout
    def parse_dados(self, resposta: str) -> dict:
        pass


class Erros():
    class InformacaoAusente(Exception):
        pass

    class UsuarioNaoExiste(Exception):
        pass

    class UrlIncorreto(Exception):
        pass
    

class ClienteUsuarios(ClienteBase):
    def __init__(self, api_url: str, usuario: str, timeout: int = 3) -> None:
        super().__init__(api_url, timeout)
        self.login = None
        self.id = None
        self.avatar_url = None
        self.html_url = None
        self.repos_url = None
        self.nome = None

        self._usuario = usuario
        _res_usuario = self.consultar_usuario()
        self.parse_dados(_res_usuario)
    
    def consultar_usuario(self) -> str:
        try:
            res = requests.get(f'{self._api_url}{self._usuario}', timeout=self._timeout)
            if res.status_code == 200:
                logger.info("Não retornou erro ao buscar usuario, continuando")
                return res.json()
            else:
                raise Erros.UsuarioNaoExiste("verifique o nome de usuário: %s", self._usuario)
        except requests.exceptions.ConnectionError:
            raise Erros.UrlIncorreto("verifique o URL")
    def parse_dados(self, resposta: dict) -> None:
        self.login = resposta['login']
        self.id = resposta['id']
        self.avatar_url = resposta['avatar_url']
        self.html_url = resposta['html_url']
        self.repos_url = resposta['repos_url']
        self.nome = resposta['name']
    #except IndexError:
        #raise Erros.InformacaoAusente("Falta uma informação essencial deste usuário")


if __name__ == "__main__":
    cliente = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", 'aiushdiausduasd')
    print(cliente.nome)