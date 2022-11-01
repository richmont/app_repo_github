from conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT
import requests
import logging
import json
import dateutil.parser
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Cliente")



class ClienteBase():
    def __init__(self, api_url: str, timeout: int = 3) -> None:
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
                mensagem = res.json()['message']
                raise Erros.ObjetoNaoExiste(mensagem=mensagem)
        except requests.exceptions.ConnectionError:
            raise Erros.UrlIncorreto("verifique o URL")

class Erros():
    class InformacaoAusente(Exception):
        pass

    class ObjetoNaoExiste(Exception):
        def __init__(self, mensagem=str()):
            self.mensagem = mensagem

    class UrlIncorreto(Exception):
        pass
    
class ClienteUsuarios(ClienteBase):
    def __init__(self, api_url: str, usuario: str, timeout: int = 3) -> None:
        """cliente para consulta de informações de um usuário do github

        Args:
            api_url (str): URL da API Rest do github
            usuario (str): Nome de usuário a ser consultado
            timeout (int, optional): Limite do tempo de resposta. Padrão é 3.
        """
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
        """transforma os dados do json na resposta em variáveis

        Args:
            resposta (dict): objeto que contém os dados recebidos na requisição
        """
        self.login = resposta['login']
        self.id = resposta['id']
        self.avatar_url = resposta['avatar_url']
        self.html_url = resposta['html_url']
        self.repos_url = resposta['repos_url']
        self.nome = resposta['name']

class ClienteRepositorios(ClienteBase):
    def __init__(self, api_url: str, limite: int = 0, timeout: int = 3) -> None:
        """coleta a listagem dos repositórios de um usuário

        Args:
            api_url (str): Neste caso, o URL dos repositórios
            limite (int): Limite de repositórios a serem buscados. Padrão 0
            timeout (int, opcional): Limite do tempo de resposta. Padrão 3.
        """
        api_url_com_limite = f"{api_url}?per_page={limite}"
        super().__init__(api_url_com_limite, timeout)
        self.lista_repositorios = self.parse_dados(self._resposta)

    def parse_dados(self, resposta: str):
        """transforma os dados do json na resposta em variáveis

        Args:
            resposta (dict): objeto que contém os dados recebidos na requisição
        """
        lista_repositorios = []
        # print(json.dumps(resposta[0], indent=4))
        for x in resposta:
            # remove o fim do url que serve para orientar o uso da API apenas
            commits_url = x["commits_url"].split('{')[0]
            repo = {
                "repo_id": x["id"],
                "nome": x["name"],
                "html_url": x["html_url"],
                "descricao": x["description"],
                "commits_url": commits_url,
                "arquivado": bool(x["archived"])
            }
            lista_repositorios.append(repo)
        return lista_repositorios

class ClienteCommits(ClienteBase):
    def __init__(self, api_url: str, limite: int = 5, timeout: int = 3) -> None:
        """consulta na API pela lista de commits de um repositório

        Args:
            api_url (str): URL da API de commits de um repo
            limite (int): Limite de repositórios a serem buscados. Padrão 5
            timeout (int, optional): Limite do tempo de resposta. Padrão 3.
        """
        super().__init__(api_url, timeout)
        self.lista_commits = self.parse_dados(self._resposta)

    def parse_dados(self, resposta: str):
        lista_commits = []
        for commit in resposta:
            _commit = {
            "commit_data": dateutil.parser.isoparse(commit['commit']['author']['date']),
            "commit_autor_login": commit['author']['login'],
            "commit_autor_nome": commit['commit']['author']['name'],
            "commit_autor_id": commit['author']['id'],
            "commit_mensagem": commit['commit']['message'],
            "commit_url": commit['url']
            }
            lista_commits.append(_commit)
        return lista_commits

    def commits_por_data(self, ascendente=True) -> list:
        """Ordena a lista de commits baseado na data

        Args:
            ascendente (bool, optional): Ascendente True exibe os commits mais antigos no topo. Padrão True.

        Returns:
            list: lista de commits
        """
        
        if ascendente:
            return sorted(self.lista_commits, key=lambda commit: commit['commit_data'])
        else:
            # commits já estão ordenados pela data de forma decrescente por padrão
            return self.lista_commits

if __name__ == "__main__":
    cliente_usuario = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", 'richmont')
    cliente_repositorios = ClienteRepositorios(cliente_usuario.repos_url, limite=0)
    commits_url = cliente_repositorios.lista_repositorios[0]['commits_url']
    print(commits_url)
    cliente_commits = ClienteCommits(commits_url)
    #print(json.dumps(cliente_commits._resposta, indent=4))
    commit_recente = cliente_commits.commits_por_data(ascendente=False)[0]
    commit_antigo = cliente_commits.commits_por_data(ascendente=True)[0]
    print(commit_antigo['commit_mensagem'])
    print("=============")
    print(commit_recente['commit_mensagem'])
    #print(sorted(cliente_commits.lista_commits, key=lambda commit: commit['commit_data'])[0])
    

    """
    print("Data do commit: ", commit['commit_data'])
    print("Login do autor: ", commit['commit_autor_login'])
    print("Login do nome: ", commit['commit_autor_nome'])
    print("Mensagem do commit: ", commit['commit_mensagem'])
    """