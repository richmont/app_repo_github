from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# https://stackoverflow.com/questions/10388033/csrf-verification-failed-request-aborted
import sys, os
try:
    sys.path.append(os.environ['VIRTUAL_ENV'])
except KeyError:
    sys.path.append('../..')
    sys.path.append('..')
from app_repo_github.gh_api_cliente.Cliente import ClienteRepositorios, ClienteUsuarios, Erros
from app_repo_github.gh_api_cliente.conf.configuracoes import GH_API_BASE_URL, GH_USUARIOS_ENDPOINT

@csrf_exempt
def index(request):
    if request.method == 'POST' and request.POST['input-usuario-github'] != '':
        usuario = request.POST['input-usuario-github']
        alfabetico = True
        try:
            
            cliente_usuario = ClienteUsuarios(f"{GH_API_BASE_URL}{GH_USUARIOS_ENDPOINT}", usuario)
            dict_usuario = {
                'id': cliente_usuario.id,
                'nome': cliente_usuario.nome,
                'login': cliente_usuario.login,
                'avatar_url': cliente_usuario.avatar_url,
                'html_url': cliente_usuario.html_url
            }

            cliente_repositorios = ClienteRepositorios(cliente_usuario.repos_url, limite=0)
            repo_alfabetico = cliente_repositorios.lista_repositorios_alfabetico
            repo_ultimo_commit = cliente_repositorios.lista_repositorios_ultimo_commit

            return render(request, 'index.html', {"usuario": dict_usuario, "repo_alfabetico": repo_alfabetico, "repo_ultimo_commit": repo_ultimo_commit})
        except Erros.ObjetoNaoExiste:
            messages.add_message(request, messages.ERROR, f"Usuário não encontrado: {usuario}")

    #cliente_repositorios = ClienteRepositorios(cliente_usuario.repos_url, limite=0)

    return render(request, 'index.html', {})
