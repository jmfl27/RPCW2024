# RPCW2024: TPC 5 - Construção de uma ontologia a partir de um dataset sobre cinema e de uma aplicação para a explorar

## Autor
João Miguel Ferreira Loureiro

## Data
31/03/2024

## Resumo
Como continuação do TPC anterior, neste TPC foi pedido que pegássemos no `.json` nele gerado e que o transformasse numa ontologia `.ttl`, conforme o formato especificado na aula, fazer uma aplicação web em `Flask` para navegar os dados encontrados no endpoint especificado e para responder a algumas queries sobre estes mesmo.

Primeiro, atualizei a geração do dataset do TPC 5 para incluir novos campos que enventualmente se revelaram necessários para este TPC, o que resultou num dataset mais robusto.

Para fazer a criação do `.ttl`, criei uma script `geraCinema.py` que utiliza a biblioteca `rdflib` para acrescentar as entradas presentes no `cinema.json` ao `baseCinema.ttl`, criado na aula a ser usado como base para a ontologia, bem como as suas data e object properties, quando aplicável. Todos os dados são tratados para substituir nomes inválidos nos ficheiros `.ttl` (ex: Burt Reynolds -> Burt_Reynolds).

Quanto à aplicção web, decidi por criar 7 rotas, no entanto não as consegui testar devidamente devido a problemas em aceder ao endpoint fornecido:

- `/` - indíce com as opções disponíveis (filmes, atores e realizadores)

- `/filmes` - mostra uma tabela com todos os filmes, identificados pelo o seu título, que contem um link para a página a ele correspondente, e a sua duração.

- `/filmes/:titulo` - mostra uma página com os detalhes do filme do título associado: título, duração, data de lançamento, elenco, compositores, países, diretores, gêneros, produtores, argumentistas e escritores, tendo cada ator e realizador um link para a página associada a esse respetivo nome.

- `/atores` - mostra uma tabela com todos os atores, identificados pelo o seu nome, que contem um link para a página a ele correspondente, e a sua data de nascimento.

- `/atores/:nome` - mostra uma página com os detalhes do ator com o nome associado: nome, data de nascimento e os filmes em qual atuaram, tendo cada filme um link para a página associada a esse respetivo filme.

- `/realizadores` - mostra uma tabela com todos os realizadores, identificados pelo o seu nome, que contem um link para a página a ele correspondente.

- `/realizadores/:nome` - mostra uma página com os detalhes do realizador com o nome associado: nome e os filmes que realizaram, tendo cada filme um link para a página associada a esse respetivo filme.

Por fim, as respostas às queries encontram-se no `queries.txt`.

## Ficheiros

- [`geraCinema.py`](geraCinema.py): script atualizada em Python que realiza consultas à DBPedia e que armazena os dados obtidos num ficheiro .json. Previamente desenvolvida para o TPC 5.

- [`cinema.json`](cinema.json): ficheiro resultante da execução da script atualizada do TPC 5.

- [`addTTL.py`](addTTL.py): script em Python usado para popular a ontologia `baseCinema.ttl` com indivíduos através dos dados contidos no `cinema.json`.

- [`baseCinema.ttl`](baseCinema.ttl): ficheiro Turtle criado através do Protege, com a estrutura base da ontologia a utilizar como base para a popular, bem como alguns exemplos de possíveis indivíduos.

- [`cinema.ttl`](cinema.ttl): ficheiro output resultante da execução da script e o resultado final da ontologia.

- [`queries.txt`](queries.txt): ficheiro que contem as respostas às queries pedidas.

- [`app.py`](app/app.py): ficheiro principal da aplicação web Flask, que controla as rotas, os pedidos a fazer, bem como a renderização da página web em si.

- [`templates`](app/templates): contem os templates em `.html` das páginas web a apresentar.