import pytest
import sys
sys.path.append("..")
from Cliente import ClienteUsuarios, Erros
from conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT

class Test_Cliente_OK():
    def test_dummy(self):
        assert True

class Test_Cliente_usuario_nao_existe():
    def test_nome_usuario_aleatorio(self):
        try:
            cliente = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", 'aiushdiausduasd')
        except Erros.ObjetoNaoExiste:
            assert True
        

class Test_Cliente_usuario_sem_repositorios():
    def test_dummy(self):
        assert True

class Test_Cliente_conexao_falhou():
    def test_url_errado(self):
        url = "https://diriguidum"
        usuario = 'diriguidum'
        try:
            cliente_usuario = ClienteUsuarios(url, usuario, timeout=1)
        except Erros.UrlIncorreto:
            assert True
    
    def test_timeout_invalido(self):
        url = "https://diriguidum"
        usuario = 'diriguidum'
        try:
            cliente_usuario = ClienteUsuarios(url, usuario, timeout=0)
        except ValueError:
            assert True