from datetime import date
from app_repo_github.gh_api_cliente.conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT
import requests
import logging
import re
import dateutil.parser
from app_repo_github.gh_api_cliente.Sessao import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Cliente")

class ClienteBase():
    def __init__(self, api_url: str, timeout: int = 3) -> None:
        self._api_url = api_url
        self._timeout = timeout
        with Session as session:
            self.session = session
            self._resposta = self.consultar()
            logger.warning("requisições restantes disponíveis: %s", self.requisicoes_restantes)
        

    def parse_dados(self, resposta: str):
        pass
    
    def consultar(self) -> str:
        try:

            res = self.session.get(f'{self._api_url}', timeout=self._timeout)
            self.requisicoes_restantes = int(res.headers['x-ratelimit-remaining'])
            if res.status_code == 200:
                logger.info("Não retornou erro ao buscar objeto, continuando")
                return res.json()
            else:
                if int(res.headers['x-ratelimit-remaining']) <= 1:
                    raise Erros.LimiteAPI("Limite da API do github atingido")
                mensagem = res.json()['message']
                logger.critical(mensagem)
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

    class LimiteAPI(Exception):
        pass
    
class ClienteUsuarios(ClienteBase):
    def __init__(self, api_url: str, usuario_bruto: str, timeout: int = 3) -> None:
        """cliente para consulta de informações de um usuário do github

        Args:
            api_url (str): URL da API Rest do github
            usuario (str): Nome de usuário a ser consultado               
            timeout (int, optional): Limite do tempo de resposta. Padrão é 3.
        """
        
        self._usuario = re.sub(r'[^a-zA-Z]', '', usuario_bruto)
        logger.debug("começando o trabalho com o usuário: %s", self._usuario)
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
        logger.debug("Inicializando cliente repositorios com url: %s", api_url)
        api_url_com_limite = f"{api_url}?per_page={limite}"
        super().__init__(api_url_com_limite, timeout)
        self.lista_repositorios = self.parse_dados(self._resposta)
        self.lista_repositorios_alfabetico = self.ordenar_lista_repositorios()
        self.lista_repositorios_ultimo_commit = self.ordenar_lista_repositorios(alfabetico=False)

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

            # obtém a data do último commit deste repositório

            """
            Abordagem de calcular o commit mais recente pela listagem completa
            é muito custosa no consumo dos limites da API

            #cliente_commits = ClienteCommits(commits_url)
            #data_commit = cliente_commits.data_commit_mais_recente
            """
            data_commit = dateutil.parser.isoparse(x['pushed_at'])
            
            repo = {
                "repo_id": x["id"],
                "nome": x["name"],
                "html_url": x["html_url"],
                "descricao": x["description"],
                "data_ultimo_commit": data_commit,
                "data_ultimo_commit_str": data_commit.strftime("%d/%m/%Y, %H:%M:%S"),
                "arquivado": bool(x["archived"])
            }
            lista_repositorios.append(repo)
        return lista_repositorios

    def ordenar_lista_repositorios(self, alfabetico=True) -> list:
        """Lista de repositórios por ordem alfabética ou de último commit

        Args:
            alfabetico (bool, optional): tipo de ordenação, True para alfabético, False para último commit. Padrão para True.

        Returns:
            list: lista de repositórios ordenada
        """
        if alfabetico:
            return sorted(self.lista_repositorios, key=lambda repo: repo['nome'])
        else:
            return sorted(self.lista_repositorios, key=lambda repo: repo['data_ultimo_commit'], reverse=True)
                

class ClienteCommits(ClienteBase):
    def __init__(self, api_url: str, timeout: int = 3) -> None:
        """consulta na API pela lista de commits de um repositório

        Args:
            api_url (str): URL da API de commits de um repo
            
            timeout (int, optional): Limite do tempo de resposta. Padrão 3.
        """
        logger.debug("Inicializando cliente commits com url: %s", api_url)
        super().__init__(api_url, timeout)
        self.lista_commits = self.parse_dados(self._resposta)
        self.data_commit_mais_recente = self.commits_por_data(ascendente=False)[0]['commit_data']


    def parse_dados(self, resposta: str):
        lista_commits = []
        
        for commit in resposta:
            try:
                autor_login = commit['author']['login']
                autor_id = commit['author']['id']
            except TypeError:
                autor_login = "Sem login"
                autor_id = "Sem autor id"
            except KeyError:
                autor_login = "Sem login"
            _commit = {
            # converte a data no formato ISO para um datetime padrão python
            "commit_data": dateutil.parser.isoparse(commit['commit']['author']['date']),
            "commit_autor_login": autor_login,
            "commit_autor_nome": commit['commit']['author']['name'],
            "commit_autor_id": autor_id,
            "commit_mensagem": commit['commit']['message'],
            "commit_url": commit['url']
            }
            lista_commits.append(_commit)
        return lista_commits

    def commits_por_data(self, ascendente=False) -> list:
        """Ordena a lista de commits baseado na data

        Args:
            ascendente (bool, optional): Ascendente True exibe os commits mais antigos no topo. Padrão False.

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
    for x in cliente_repositorios.lista_repositorios_ultimo_commit:
        print(x['data_ultimo_commit_str'])
    #repo_alfabetico = cliente_repositorios.lista_repositorios_alfabetico[0]
    #repo_ultimo_commit = cliente_repositorios.lista_repositorios_ultimo_commit[0]

    #print("Repositório na ordem alfabética: ", repo_alfabetico)
    #print("Repositório na ordem ultimo commit: ", repo_ultimo_commit)
