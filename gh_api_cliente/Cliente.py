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
    
    def consultar(self) -> str:
        try:
            res = requests.get(f'{self._api_url}', timeout=self._timeout)
            if res.status_code == 200:
                logger.info("Não retornou erro ao buscar objeto, continuando")
                return res.json()
            else:
                raise Erros.ObjetoNaoExiste("verifique o elemento consultado na API: %s", self._api_url)
        except requests.exceptions.ConnectionError:
            raise Erros.UrlIncorreto("verifique o URL")

class Erros():
    class InformacaoAusente(Exception):
        pass

    class ObjetoNaoExiste(Exception):
        pass

    class UrlIncorreto(Exception):
        pass
    

class ClienteUsuarios(ClienteBase):
    def __init__(self, api_url: str, usuario: str, timeout: int = 3) -> None:
        super().__init__(api_url, timeout)
        self._usuario = usuario
        self._api_url = f"{self._api_url}{self._usuario}"
        self.login = None
        self.id = None
        self.avatar_url = None
        self.html_url = None
        self.repos_url = None
        self.nome = None

        
        _res_usuario = self.consultar()
        self.parse_dados(_res_usuario)
    


    def parse_dados(self, resposta: dict) -> None:
        self.login = resposta['login']
        self.id = resposta['id']
        self.avatar_url = resposta['avatar_url']
        self.html_url = resposta['html_url']
        self.repos_url = resposta['repos_url']
        self.nome = resposta['name']

class ClienteRepositorios(ClienteBase):
    def __init__(self, api_url: str, timeout: int = 3) -> None:
        """coleta a listagem dos repositórios de um usuário

        Args:
            api_url (str): Neste caso, o URL dos repositórios
            timeout (int, opcional): Limite do tempo de resposta. Padrão 3.
        """
        super().__init__(api_url, timeout)

    def consultar(self):
        try:
            res = requests.get(f'{self._api_url}', timeout=self._timeout)
            if res.status_code == 200:
                logger.info("Não retornou erro ao buscar usuario, continuando")
                return res.json()
            else:
                raise Erros.UsuarioNaoExiste("verifique o nome de usuário: %s", self._usuario)
        except requests.exceptions.ConnectionError:
            raise Erros.UrlIncorreto("verifique o URL")

if __name__ == "__main__":
    cliente = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", 'aiushdiausduasd')
    print(cliente.nome)