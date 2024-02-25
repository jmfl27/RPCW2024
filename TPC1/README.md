# RPCW2024: TPC 1 - Script de Criação de Ontologias sobre Plantas

## Autor
João Miguel Ferreira Loureiro

## Data
17/02/2024

## Resumo
Este trabalho teve como objetivo criar uma Ontologia a partir de um dataset `plantas.json`. Comecei por observar este dataset e identificar as classes que constituirão a ontologia, bem como os atributos que constituem cada um deles. Foram criadas as classes `Planta` (a classe principal da ontologia que contem Object Properties (OPs) com as outras classes e todas as Data Properties (DPs) relacionadas com as caraterísticas das plantas), `Rua` (contem as DPs relacionadas com todas as informações das localizações das plantas) e `Espécie` (contém as Espécies das plantas). Ao analisar o dataset, reparei que existiam algumas entradas sem o atributo "Rua" ou "Código de Rua". No caso de só possuir um deles, a script tenta fazer cross-reference com entradas previamente inseridas. Caso não possua nenhum, a entrada é ignorada.

## Ficheiro

- [`plantas.json`](plantas.json): ficheiro .json com os registos de dados sobre as plantas.
- [`plantasBase.ttl`](plantasBase.ttl): ficheiro Turtle criado através do Protege, com a estrutura base da ontologia a utilizar como base para a popular.
- [`geraTTL.py`](geraTTL.py): script em Python usado para popular a ontologia com indivíduos através dos dados contidos no `plantas.json`.
- [`plantas.ttl`](plantas.tty): ficheiro output resultante da execução da script e o resultado final da ontologia.
