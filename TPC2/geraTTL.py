import json

def correctCurso(cid,inst,cursosD):
    if cid.startswith("CB"):
        for c in cursosD:
            if c.startswith("CB") and cursosD[c]["instrumento"] == inst:
                return c
    else:
        for c in cursosD:
            if c.startswith("CS") and cursosD[c]["instrumento"] == inst:
                return c           


f = open("db.json")
bd = json.load(f)
f.close()

print(f"""
@prefix : <http://rpcw.di.uminho.pt/2024/musica/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/musica/> .

<http://rpcw.di.uminho.pt/2024/musica> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#frequenta
:frequenta rdf:type owl:ObjectProperty ;
           rdfs:domain :Aluno ;
           rdfs:range :Cursos .


###  http://rpcw.di.uminho.pt/2024/musica#leciona
:leciona rdf:type owl:ObjectProperty ;
         rdfs:domain :Cursos ;
         rdfs:range :Instrumentos .


###  http://rpcw.di.uminho.pt/2024/musica#toca
:toca rdf:type owl:ObjectProperty ;
      rdfs:domain :Aluno ;
      rdfs:range :Instrumentos .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#anoCurso
:anoCurso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/musica#dataNasc
:dataNasc rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/musica#designacao
:designacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Cursos ;
            rdfs:range xsd:string .

###  http://rpcw.di.uminho.pt/2024/musica#duracao
:duracao rdf:type owl:DatatypeProperty ;
         rdfs:domain :Cursos ;
         rdfs:range xsd:int .

###  http://rpcw.di.uminho.pt/2024/musica#id_aluno
:id_aluno rdf:type owl:DatatypeProperty ;
          rdfs:domain :Aluno ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/musica#id_curso
:id_curso rdf:type owl:DatatypeProperty ;
          rdfs:domain :Cursos ;
          rdfs:range xsd:string .        


###  http://rpcw.di.uminho.pt/2024/musica#id_instrumento
:id_instrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumentos ;
                rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/musica#nome_aluno
:nome_aluno rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/musica#nome_instrumento
:nome_instrumento rdf:type owl:DatatypeProperty ;
                  rdfs:domain :Instrumentos ;
                  rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#CursoBasico
:CursoBasico rdf:type owl:Class ;
             rdfs:subClassOf :Cursos .


###  http://rpcw.di.uminho.pt/2024/musica#CursoSupeletivo
:CursoSupeletivo rdf:type owl:Class ;
                 rdfs:subClassOf :Cursos .


###  http://rpcw.di.uminho.pt/2024/musica#Cursos
:Cursos rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Instrumentos
:Instrumentos rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

""")

cursosD = {}
instrumentosD = {}
#i=0

for curso in bd["cursos"]:
    cursosD[curso["id"]] = {
        "designacao" : curso["designacao"],
        "duracao" : curso["duracao"],
        "instrumento" : curso["instrumento"]["#text"]
    }
    print(f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ,
                  :{"CursoBasico" if curso["id"].startswith("CB") else "CursoSupeletivo"} ;
         :id_curso "{curso["id"]}";
         :designacao "{curso["designacao"].replace(" ","_")}";
         :duracao "{curso["duracao"]}"^^xsd:int;
         :leciona :{curso["instrumento"]["id"]};
         :id_curso "{curso["id"]}".

""")
    
for inst in bd["instrumentos"]:
    instrumentosD[inst["#text"]] = {
        "nome" : inst["id"]
    }
    print(f"""
###  http://rpcw.di.uminho.pt/2024/musica#{inst["id"]}
:{inst["id"]} rdf:type owl:NamedIndividual ,
                  :Instrumentos ;
         :id_instrumento "{inst["id"]}";
         :nome_instrumento "{inst["#text"].replace(" ","_")}".

""")

#list(ruas.keys())[list(ruas.values()).index(planta['Rua'])]
#list(instrumentosD.keys())[list(instrumentosD.values()).index(aluno["instrumento"])]

for aluno in bd["alunos"]:

    print(f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ,
                  :Aluno ;
         :nome_aluno "{aluno["nome"].replace(" ","_")}";
         :dataNasc "{aluno["dataNasc"]}";
         :anoCurso "{aluno["anoCurso"]}"^^xsd:int;
         :toca :{instrumentosD[aluno["instrumento"]]["nome"].replace(" ","_")};
         :frequenta :{aluno["curso"] if aluno["curso"] in cursosD.keys() else correctCurso(aluno["curso"],aluno["instrumento"],cursosD)};
         :id_aluno "{aluno["id"]}".

""")