from conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Cliente")

class ClienteBase():
    def __init__(self, api_url:str, timeout: int = 3) -> None:
        self._api_url = api_url
        self._timeout = timeout
        self._resposta = self.consultar()

    def parse_dados(self, resposta: str):
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
        logger.debug("começando o trabalho com o usuário: %s", usuario)
        self._usuario = usuario
        super().__init__(f"{api_url}{self._usuario}", timeout)
        self.login = None
        self.id = None
        self.avatar_url = None
        self.html_url = None
        self.repos_url = None
        self.nome = None
        self.parse_dados(self._resposta)
    


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

    def parse_dados(self, resposta: str):
        pass



if __name__ == "__main__":
    cliente = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", 'richmont')
    print(cliente.repos_url)