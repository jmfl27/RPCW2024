# RPCW2024: TPC 5 - Geração de um dataset sobre cinema

## Autor
João Miguel Ferreira Loureiro

## Data
17/03/2024

## Resumo
O objetivo deste TPC era gerar um dataset sobre cinema constituido pela a informação de vários filmes incluindo os atores que nele participaram, os seus realizadores, escritores, músicos, argumentisas e duração.

Para esse efeito, utilizei a `DBPedia` e, após analizar algumas entradas relacionadas com filmes, observei os atributos e propriedades relevantes e contruí a seguinte query SPARQL que obtém todos os registos relevantes:

```
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?filmName ?actorName ?directorName ?writerName ?musicName ?screenName ?duration
WHERE {
    ?filme a dbo:Film;
              rdfs:label ?filmName.
   Optional {
             ?filme dbo:starring ?actor.
              ?actor rdfs:label ?actorName.
              FILTER (LANG(?actorName) = 'en')
   }
   Optional {
             ?filme dbo:director ?director.
              ?director rdfs:label ?directorName.
              FILTER (LANG(?directorName) = 'en')
   }
   Optional {
             ?filme dbo:writer ?writer.
              ?writer rdfs:label ?writerName.
              FILTER (LANG(?writerName) = 'en')
   }
   Optional {
             ?filme dbo:musicComposer ?music.
              ?music rdfs:label ?musicName.
              FILTER (LANG(?musicName) = 'en')
   }
   Optional {
             ?filme dbp:screenplay ?screen.
              ?screen rdfs:label ?screenName.
              FILTER (LANG(?screenName) = 'en')
   }
  Optional {
             ?filme dbo:runtime ?duration.
   }
  FILTER (LANG(?filmName) = 'en')
}
```
Fez-se então uma script `geraCinema.py` que faz um pedido com a query à DBPedia e usa os dados fornecidos para cirar um ficheiro .json `cinema.json` que contem todas as informações relevantes organizadas por filmes.

## Ficheiro

- [`geraCinema.py`](geraCinema.py): script em Python que realiza consultas à DBPedia e que armazena os dados obtidos num ficheiro .json.

- [`cinema.json`](cinema.json): ficheiro resultante da execução da script.
