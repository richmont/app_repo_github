from conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT
import requests

class ClienteBase():
    def __init__(self, api_url) -> None:
        self.api_url = api_url

    def consultar_api(self) -> str:
        """Realiza a requisição para a API a partir do url recebido

        Retorna:
            str: conteúdo da resposta da requisição
        """
        return str()

    def parse_resposta(self) -> dict:
        return dict()

class ClienteUsuarios(ClienteBase):
    def __init__(self, api_url) -> None:
        super().__init__(api_url)
        pass

