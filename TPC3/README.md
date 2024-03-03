# RPCW2024: TPC 3 - Criação e Execução de Queiries sob uma Ontologia de um Mapa Virtual

## Autor
João Miguel Ferreira Loureiro

## Data
03/03/2024

## Resumo
Antes de criar a ontologia, observei o dataset fornecido e indentifiquei 3 classes que formarão a ontologia:

- `Cidade`, que identifica uma cidade, possuindo 4 DPs relacionadas com a sua descrição, cidade, nome e população, bem como uma OP: 'pertenceA' que identifica a qual Distrito pertence.
- `Distrito`, que identifica um Distrito, possuindo 2 DPs relacionadas com o seu nome e o seu id, que não existe no dataset original mas é criado conforme são identificados novos distritos.
- `Ligação`, que identifica uma Ligação, possuindo 2 DPs relacionadas com o seu id e a sua distancia, bem como 2 OPs 'destino' que identifica a cidade destinatária e 'origem' que identifica a cidade de origem.

A script cria, para cada ligação, uma ligação inversa onde o destino original passa à origem do novo, e vice versa.

As respostas às queries encontram se no ficheiro [`queries.txt`](queries.txt), e foram respondidas com recurso ao GraphDB.

Para correr a script e obter o output desejado, deve ser corrido o seguinte comando: `python3 geraTTL.py > mapaVirtual.ttl`

## Ficheiros

- [`mapa-virtual.json`](mapa-virtual.json): ficheiro .json com os registos de dados sobre o mapa virtual.
- [`mapaBase.ttl`](`mapaBase.ttl): ficheiro Turtle criado através do Protege, com a estrutura base da ontologia a utilizar como base para a popular, bem como alguns exemplos de possíveis indivíduos.
- [`geraTTL.py`](geraTTL.py): script em Python usado para popular a ontologia com indivíduos através dos dados contidos no `mapa-virtual.json`.
- [`mapaVirtual.ttl`](mapaVirtual.ttl): ficheiro output resultante da execução da script e o resultado final da ontologia.
- [`queries.txt`](queries.txt): ficheiro que contem as respostas às queries pedidas.