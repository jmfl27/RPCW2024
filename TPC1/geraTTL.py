import json

f = open("plantas.json")
bd = json.load(f)
f.close()

ttl = """
@prefix : <http://rpcw.di.uminho.pt/2024/plantas/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/plantas/> .

<http://rpcw.di.uminho.pt/2024/plantas> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#pertenceA
:pertenceA rdf:type owl:ObjectProperty ;
           rdfs:domain :Planta ;
           rdfs:range :Espécie .


###  http://rpcw.di.uminho.pt/2024/plantas#resideEm
:resideEm rdf:type owl:ObjectProperty ;
          rdfs:domain :Planta ;
          rdfs:range :Rua .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#NomeRua
:NomeRua rdf:type owl:DatatypeProperty ;
         rdfs:domain :Rua ;
         rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Caldeira
:Caldeira rdf:type owl:DatatypeProperty ;
          rdfs:domain :Planta ;
          rdfs:range xsd:boolean .


###  http://rpcw.di.uminho.pt/2024/plantas#Codigo
:Codigo rdf:type owl:DatatypeProperty ;
        rdfs:domain :Rua ;
        rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/plantas#DataAtualizacao
:DataAtualizacao rdf:type owl:DatatypeProperty ;
                 rdfs:domain :Planta ;
                 rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#DataPlantacao
:DataPlantacao rdf:type owl:DatatypeProperty ;
               rdfs:domain :Planta ;
               rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Estado
:Estado rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Freguesia
:Freguesia rdf:type owl:DatatypeProperty ;
           rdfs:domain :Rua ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Gestor
:Gestor rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Id
:Id rdf:type owl:DatatypeProperty ;
    rdfs:domain :Planta ;
    rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/plantas#Implantacao
:Implantacao rdf:type owl:DatatypeProperty ;
             rdfs:domain :Planta ;
             rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Local
:Local rdf:type owl:DatatypeProperty ;
       rdfs:domain :Rua ;
       rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#NomeCient
:NomeCient rdf:type owl:DatatypeProperty ;
           rdfs:domain :Planta ;
           rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#NumInterven
:NumInterven rdf:type owl:DatatypeProperty ;
             rdfs:domain :Planta ;
             rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/plantas#Origem
:Origem rdf:type owl:DatatypeProperty ;
        rdfs:domain :Planta ;
        rdfs:range xsd:string .


###  http://rpcw.di.uminho.pt/2024/plantas#Registo
:Registo rdf:type owl:DatatypeProperty ;
         rdfs:domain :Planta ;
         rdfs:range xsd:int .


###  http://rpcw.di.uminho.pt/2024/plantas#Tutor
:Tutor rdf:type owl:DatatypeProperty ;
       rdfs:domain :Planta ;
       rdfs:range xsd:boolean .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/plantas#Espécie
:Espécie rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Planta
:Planta rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/plantas#Rua
:Rua rdf:type owl:Class .

#################################################################
#    Individuals
#################################################################

"""

ruas = {}
especies = []
#i=0

for planta in bd:
    #print(i)
    #i+=1
    if planta['Rua'] != "" and planta['Código de rua'] != "":

        if planta['Código de rua'] not in ruas.keys():
            ruas[planta['Código de rua']] = planta['Rua']

        registo = f"""
        ###  http://rpcw.di.uminho.pt/2024/plantas#{planta['Id']}
        <http://rpcw.di.uminho.pt/2024/plantas#{planta['Id']}> rdf:type owl:NamedIndividual ,
                                                            :Planta ;
                                                    :Caldeira "{True if planta['Caldeira'] == "Sim" else False}"^^xsd:bool ;
                                                    :DataAtualizacao "{planta['Data de actualização'].replace(" ","_")}" ;
                                                    :DataPlantacao "{planta['Data de Plantação'].replace(" ","_")}" ;
                                                    :Estado "{planta['Estado'].replace(" ","_")}" ;
                                                    :Gestor "{planta['Gestor'].replace(" ","_")}" ;
                                                    :Implantacao "{planta['Implantação'].replace(" ","_")}" ;
                                                    :NomeCient "{planta['Nome Científico'].replace(" ","_")}" ;
                                                    :NumInterven "{planta['Número de intervenções'] if planta['Número de intervenções'] != "" else 0}"^^xsd:int  ;
                                                    :Origem "{planta['Origem'].replace(" ","_")}" ;
                                                    :Registo "{planta['Número de Registo']}"^^xsd:int  ;
                                                    :Tutor "{True if planta['Tutor'] == "Sim" else False}"^^xsd:bool ;
                                                    :pertenceA :{planta['Espécie'].replace(" ","_")} ;
                                                    :resideEm :{planta['Código de rua'] if planta['Código de rua'] != "" else list(ruas.keys())[list(ruas.values()).index(planta['Rua'])] } ;
                                                    :Id "{planta['Id']}"^^xsd:int  .
        """

        if planta['Código de rua'] != "":
            registo += f"""    
            ###  http://rpcw.di.uminho.pt/2024/plantas#{planta['Código de rua']}
            :{planta['Código de rua']} rdf:type owl:NamedIndividual ,
                            :Rua ;
                            :NomeRua "{planta['Rua'].replace('"',"").replace(" ","_")}" ;
                            :Freguesia "{planta['Freguesia'].replace('"',"").replace(" ","_")}"  ;
                            :Local "{planta['Local'].replace('"',"").replace(" ","_")}" ;
                            :Codigo "{planta['Código de rua']}"^^xsd:int .
            """
        else:
            registo += f"""    
            ###  http://rpcw.di.uminho.pt/2024/plantas#{list(ruas.keys())[list(ruas.values()).index(planta['Rua'])]}
            :{list(ruas.keys())[list(ruas.values()).index(planta['Rua'])]} rdf:type owl:NamedIndividual ,
                            :Rua ;
                            :NomeRua "{planta['Rua'].replace('"',"").replace(" ","_")}" ;
                            :Freguesia "{planta['Freguesia'].replace('"',"").replace(" ","_")}"  ;
                            :Local "{planta['Local'].replace('"',"").replace(" ","_")}" ;
                            :Codigo "{list(ruas.keys())[list(ruas.values()).index(planta['Rua'])]}"^^xsd:int .
            """
        
        if planta['Espécie'].replace(" ","_") not in especies:
            especies.append(planta['Espécie'].replace(" ","_"))

            registo += f"""
            ###  http://rpcw.di.uminho.pt/2024/plantas#:{planta['Espécie'].replace(" ","_")}
            :{planta['Espécie'].replace(" ","_")} rdf:type owl:NamedIndividual ,
                                :Espécie .
            """
        
        ttl += registo

f = open("plantas.ttl", "w")
f.write(ttl)
f.close()