console.log('hello world');
//var lista_repositorios = document.getElementById('lista-repositorios')
const obterListaRepositorios = (id_lista) => {
    var listaRepositorios = document.getElementById(id_lista).children
  
    return listaRepositorios
  }

  listaRepositorios = obterListaRepositorios('lista-repositorios');
  
 
  const barraBusca = document.getElementById('barraBusca');
  barraBusca.addEventListener('input', (e)=> {
      const stringBusca = e.target.value.toLowerCase();
      console.log(stringBusca);
      for (let repo of listaRepositorios){ 
        if(repo.querySelector('.repo-nome').innerText.toLowerCase().includes(stringBusca)){
          repo.style.display = ''
        } else{
          repo.style.display = 'none'
        }
    }
      
  });

  var checkbox_arquivados = document.querySelector("#checkbox-exibir-arquivados");
  checkbox_arquivados.addEventListener('change', function() {
    
    if (this.checked) {
      for (let repo of listaRepositorios){ 
        if(repo.querySelector('.repo-arquivado').innerText == 'Arquivado: Sim'){
          repo.style.display = ''}
        
        
       }
      } else {
      for (let repo of listaRepositorios){ 
        if(repo.querySelector('.repo-arquivado').innerText == 'Arquivado: Sim'){
          repo.style.display = 'none'
        } 
    }
  }
}
);
var listaRadioOrdenar = document.querySelectorAll('.radio-ordenar')


const ordenarRepo = (listaRadioOrdenar) => {
  
  for(let radio of listaRadioOrdenar){
    radio.addEventListener('change', function() {
      reposAlfabetico = document.querySelectorAll('.alfabetico')
      reposUltimoCommit = document.querySelectorAll('.ultimo-commit')
    if(radio.id == 'radio-ultimo-commit' && radio.checked){
      
        for(let repo of reposAlfabetico){
          repo.style.display = 'none'
        }
      } else{
        for(let repo of reposAlfabetico){
          repo.style.display = ''
        
      }

    }
    if(radio.id == 'radio-alfabetica' && radio.checked){
          for(let repo of reposUltimoCommit){
            repo.style.display = 'none'
          }
    } else{
          for(let repo of reposUltimoCommit){
            repo.style.display = ''
          }
    }
    console.log(radio.checked)
    console.log(radio.id)
    }
  
)
  }}
ordenarRepo(listaRadioOrdenar);

