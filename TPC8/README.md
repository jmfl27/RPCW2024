# RPCW2024: TPC 8 - Converter XML em Ontologias TTL

## Autor
João Miguel Ferreira Loureiro

## Data
14/04/2024

## Resumo
Este TPC constituiu na criação de um ficheiro TTL que contem uma ontologia com informações sobre famílias a partir de um ficheiros XML. Observando o ficheiro base fornecido pelo o docente pode-se observar que existe uma classe, Pessoa, com um data property, o nome, e duas object properties, temPai e temMae.
Ambos os ficheiros XML seguem a mesma estrtura para identificar pessoas, utilizando a tag `<person>`, que por sua vez possui várias tags que contêm a informação pessoal dessa pessoa, sendo as mais relevantes a este TPC: `<id>`, `<name>`, `<sex>` e `<parent>`.
Utilizando a bilioteca xml e a ElementTree pertnecente a esta, a script percorre cada entrada com a tag `<person>`, utilizando as tags `<id>` e `<name>` para acrescentar esse indivíduo à ontologia. De seguida, percorre todas as linhas com a tag `<parent>`, que possui um `ref` com o `<id>` associado ao pai da pessoa. Utilizando esse id, vai até à entrada correspondente e verifica a tag `<sex>` para saber qual das object properties tem que criar para esse indivíduo ('M' para temPai e 'F' para temMae).

## Ficheiro

- [`biblia.xml`](biblia.xml) e [`royal.xml`](royal.xml): ficheiros .xml que contêm a informação a converter para .ttl.

- [`familia-base.ttl`](familia-base.ttl): ficheiro Turtle criado através do Protege, com a estrutura base da ontologia a utilizar como base para a popular.

- [`addBiblia.py`](addBiblia.py) e [`addRoyal.py`](addRoyal.py): scripts em Python usados para popular a ontologia `baseCinema.ttl` com indivíduos através dos dados contidos no `biblia.xml` ou `royal.xml`.

- [`biblia.ttl`](biblia.ttl) e [`royal.ttl`](royal.ttl): ficheiros output resultantes da execução das scripts e os resultados finais das ontologias.