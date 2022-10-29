import datetime
import requests

class Repositorio():
    def __init__(self, nome: str,
                id_repositorio: int, 
                arquivado: bool, 
                commits_url: str) -> None:
        """Possui os principais atributos de um repositório

        Args:
            nome (str): Nome do repositório
            id_repositorio (int): ID que identifica o repo no github
            arquivado (bool): Se o repo está arquivado ou não
            commits_url (str): URL da lista de commits do repositório
        """
        self.nome = nome
        self.id_repositorio = id_repositorio
        self.arquivado = arquivado
        self._commits_url = commits_url

    def obter_ultimo_commit(self) -> datetime.datetime:
        """Ajusta o url de commits e obtém a data do mais recente

        Returns:
            datetime.datetime: Data do último commit
        """
        pass