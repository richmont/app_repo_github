console.log('hello world');
//var lista_repositorios = document.getElementById('lista-repositorios')
const obterListaRepositorios = (id_lista) => {
    var listaRepositorios = document.getElementById(id_lista).children
  
    return listaRepositorios
  }

  listaRepositorios = obterListaRepositorios('lista-repositorios');
  
  for (let repo of listaRepositorios)
  { 
    console.log(repo.querySelector('.repo-nome').innerText)
    }
  
  const barraBusca = document.getElementById('barraBusca');
  barraBusca.addEventListener('input', (e)=> {
      const stringBusca = e.target.value.toLowerCase();
      console.log(stringBusca);
      for (let repo of listaRepositorios){ 
        if(repo.querySelector('.repo-nome').innerText.toLowerCase().includes(stringBusca)){
          continue
        } else{
          repo.style.display = 'none'
        }
    }
      
  });
  