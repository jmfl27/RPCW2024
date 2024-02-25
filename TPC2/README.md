# RPCW2024: TPC 2 - Script de Criação de Ontologias sobre Cursos de Música

## Autor
João Miguel Ferreira Loureiro

## Data
25/02/2024

## Resumo
Este trabalho teve como objetivo criar uma Ontologia a partir de um dataset `db.json` que contem a informação de vários cursos de Música, os instrumentos neles lecionados bem como os alunos que os frequentam. Ao observar o dataset, consegui identificar três classes que formarão a ontologia:

- `Aluno`, que identifica um aluno de um curso, possuíndo 4 DPs relacionadas com o seu id, data de nascimento, nome e ano do curso em que se encontram, e 2 OPs: "frequenta" que o relaciona com o seu curso e "toca" que o relaciona com o instrumento que toca.
- `Cursos`, que identifica um curso a ser lecionado, possuíndo 3 DPs relacionadas com a sua designação/nome, id e duração, e uma OP: "leciona" que o relaciona com o instrumento que leciona. Ao observar o dataset, pode-se observar que os cursos estão divididos em Cursos Basicos e Supeletivos, tendo se criado para eles duas subclasses: `CursoBasico` e `CursoSupeletivo`,
- `Instrumentos`, que identifica um instrumento lecionado por um curso, possuíndo 2 DPs relacionadas com o seu id e nome.

A script construida faz primeiro a inserção dos cursos e dos instrumentos de forma a poder resolver os erros existentes nos registos dos alunos. Sobre as subclasses dos cursos, a script verifica se o id de um curso começa por "CB" ou "CS" de forma a inserir-los na subclasse respetiva. Já sobre os erros previamente mencionados nos registos, existem muitos alunos com ids de cursos não existentes. Como tal, para resolver estes casos, a script verifica se o id começa por "CB" ou "CS" e o instrumento que o aluno toca e observa qual dos cursos existentes corresponde à subclasse e ao instrumento nele identificados.

Para correr a script e obter o output desejado, deve ser corrido o seguinte comando: `python3 geraTTL.py > musica.ttl`


## Ficheiros

- [`db.json`](db.json): ficheiro .json com os registos de dados sobre os cursos de música.
- [`musicaBase.ttl`](`musicaBase.ttl`): ficheiro Turtle criado através do Protege, com a estrutura base da ontologia a utilizar como base para a popular, bem como alguns exemplos de possíveis indivíduos.
- [`geraTTL.py`](geraTTL.py): script em Python usado para popular a ontologia com indivíduos através dos dados contidos no `db.json`.
- [`musica.ttl`](musica.ttl): ficheiro output resultante da execução da script e o resultado final da ontologia.
