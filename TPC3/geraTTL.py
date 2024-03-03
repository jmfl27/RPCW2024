import json

f = open("mapa-virtual.json")
bd = json.load(f)
f.close()

print(f"""@prefix : <http://rpcw.di.uminho.pt/2024/mapa/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/mapa/> .

<http://rpcw.di.uminho.pt/2024/mapa> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa/destino
:destino rdf:type owl:ObjectProperty ;
         rdfs:domain :Ligação ;
         rdfs:range :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa/origem
:origem rdf:type owl:ObjectProperty ;
        rdfs:domain :Ligação ;
        rdfs:range :Cidade .


###  http://rpcw.di.uminho.pt/2024/mapa/pertenceA
:pertenceA rdf:type owl:ObjectProperty ;
           rdfs:domain :Cidade ;
           rdfs:range :Distrito .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa#distancia
:distancia rdf:type owl:DatatypeProperty ;
           rdfs:domain :Ligação ;
           rdfs:range xsd:float .


###  http://rpcw.di.uminho.pt/2024/mapa/descricao
:descricao rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/idCidade
:idCidade rdf:type owl:DatatypeProperty ;
          rdfs:domain :Cidade ;
          rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/idDistrito
:idDistrito rdf:type owl:DatatypeProperty ;
            rdfs:domain :Distrito ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/idLigacao
:idLigacao rdf:type owl:DatatypeProperty ;
           rdfs:domain :Ligação ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/nomeCidade
:nomeCidade rdf:type owl:DatatypeProperty ;
            rdfs:domain :Cidade ;
            rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/nomeDistrito
:nomeDistrito rdf:type owl:DatatypeProperty ;
              rdfs:domain :Distrito ;
              rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/mapa/populacao
:populacao rdf:type owl:DatatypeProperty ;
           rdfs:domain :Cidade ;
           rdfs:range xsd:int .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/mapa/Cidade
:Cidade rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapa/Distrito
:Distrito rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/mapa/Ligação
:Ligação rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

""")

cidadesD = {}
ligacoesD = {}
distritoD = {}
idDistrito = 1
#i=0

for cidade in bd["cidades"]:
    if cidade["distrito"] not in distritoD:
        distritoD[cidade["distrito"]] = "d" + str(idDistrito)
        idDistrito+=1
    cidadesD[cidade["id"]] = {
        "nome" : cidade["nome"],
        "população" : cidade["população"],
        "descrição" : cidade["descrição"],
        "distrito" : distritoD[cidade["distrito"]]
    }
    print(f"""
###  http://rpcw.di.uminho.pt/2024/mapa#{cidade["id"]}
:{cidade["id"]} rdf:type owl:NamedIndividual ,
                  :Cidade  ;
         :idCidade "{cidade["id"]}";
         :descricao "{cidade["descrição"]}";
         :nomeCidade "{cidade["nome"]}";
         :populacao "{cidade["população"]}"^^xsd:int;
         :pertenceA :{distritoD[cidade["distrito"]]}.

""")
    
for ligacao in bd["ligacoes"]:
    ligacoesD[ligacao["id"]] = {
        "origem" : ligacao["origem"],
        "destino" : ligacao["destino"],
        "distância" : ligacao["distância"]
    }
    rev = "l" + str(int(ligacao["id"].replace("l","")) + 3000)
    #print(rev)
    ligacoesD[rev] = {
        "origem" : ligacao["destino"],
        "destino" : ligacao["origem"],
        "distância" : ligacao["distância"]
    }
    print(f"""
###  http://rpcw.di.uminho.pt/2024/mapa#{ligacao["id"]}
:{ligacao["id"]} rdf:type owl:NamedIndividual ,
                  :Ligação ;
         :idLigacao "{ligacao["id"]}";
         :distancia "{ligacao["distância"]}"^^xsd:float;
         :destino :{ligacao["destino"]};
         :origem :{ligacao["origem"]} .

""")
    print(f"""
###  http://rpcw.di.uminho.pt/2024/mapa#{rev}
:{rev} rdf:type owl:NamedIndividual ,
                  :Ligação ;
         :idLigacao "{rev}";
         :distancia "{ligacao["distância"]}"^^xsd:float;
         :destino :{ligacao["origem"]};
         :origem :{ligacao["destino"]} .

""")
    
for distrito in distritoD:
    print(f"""
###  http://rpcw.di.uminho.pt/2024/mapa#{distritoD[distrito]}
:{distritoD[distrito]} rdf:type owl:NamedIndividual ,
                  :Distrito ;
         :idDistrito "{distritoD[distrito]}";
         :nomeDistrito "{distrito}" .

""")