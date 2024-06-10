import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD
import datetime

# Carregar o grafo RDF existente
g = Graph()
g.parse("diario_da_republica.ttl")

# Definir o namespace do seu grafo RDF
diario = Namespace("http://rpcw.di.uminho.pt/2024/diario-republica/")

# Função para formatar URIs
def format_uri(id):
    if not isinstance(id, str):
         id = str(id)
    return URIRef(diario + id.replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_'))

# Abrir o arquivo JSON e ler os dados
with open("data/new_data.json", "r") as json_file:
    data = json.load(json_file)

def giveDate(data_str):
    # Converter a string de data para um objeto datetime
    data = datetime.datetime.strptime(data_str, "%Y-%m-%d")
    
    # Obter o dia
    dia = data.strftime("%d")
    
    # Obter o mês por extenso em português
    meses_por_extenso = {
        1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
        5: "maio", 6: "junho", 7: "julho", 8: "agosto",
        9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
    }
    mes = meses_por_extenso[data.month]

    ano = data.strftime("%Y")
    
    return dia, mes, ano

entidades_emissoras = set()
diarios_rep = set()
file = 0
id = 0
leng = 0

# Iterar sobre cada entrada no arquivo JSON e adicionar as informações ao grafo RDF
for diploma in data:
    leng += 1
    doc_class = diploma["doc_class"]
    doc_class_uri = format_uri(doc_class)

    # Adicionar informações específicas de cada diploma
    diploma_uri = format_uri(id)
    g.add((diploma_uri, RDF.type, OWL.NamedIndividual))
    g.add((diploma_uri, RDF.type, doc_class_uri))
    g.add((diploma_uri, diario.numero_publicacao, Literal(diploma["number"].split("/")[0])))
    g.add((diploma_uri, diario.local_publicacao, Literal(str(diploma["series"]) + ".ª Série")))
    g.add((diploma_uri, diario.data_publicacao, Literal(diploma["date"])))
    g.add((diploma_uri, diario.articulado, Literal(diploma["dre_pdf"])))
    dia, mes, _ = giveDate(diploma["date"]) 
    g.add((diploma_uri, diario.identificacao_diploma, Literal(f'{diploma["doc_class"]} n.º {diploma["number"]}, de {dia} de {mes}')))
    g.add((diploma_uri, diario.number, Literal(diploma["number"])))
    g.add((diploma_uri, diario.doc_type, Literal(diploma["doc_type"])))
    if "o seguinte:" not in diploma["notes"]:
        g.add((diploma_uri, diario.sumario, Literal(diploma["notes"])))
        g.add((diploma_uri, diario.preambulo, Literal("N/E")))
    else: 
        g.add((diploma_uri, diario.sumario, Literal("N/E")))
        g.add((diploma_uri, diario.preambulo, Literal(diploma["notes"].split("o seguinte:")[0] + "o seguinte:")))

    #Adicionar Entidades Emissoras
    for entidade in diploma["emiting_body"]:

        if "<li>" in entidade:
            entidade = "Universidade Nova de Lisboa - Instituto de Higiene e Medicina Tropical"
        entidade_uri = format_uri(entidade)
                                  
        if entidade not in entidades_emissoras:
            g.add((entidade_uri, RDF.type, OWL.NamedIndividual))
            g.add((entidade_uri, RDF.type, diario.Entidade_Emissora))
            g.add((entidade_uri, diario.entidade_emissora, Literal(entidade)))
            entidades_emissoras.add(entidade)

        g.add((entidade_uri, diario.emite, diploma_uri))
        g.add((diploma_uri, diario.emitido, entidade_uri))

    #Adicionar Diários
    dn = diploma["dr_number"]
    diario_uri = format_uri(dn.replace("/","-"))

    if dn not in diarios_rep:
        g.add((diploma_uri, RDF.type, OWL.NamedIndividual))
        g.add((diario_uri, RDF.type, diario.Diario_da_Republica))
        g.add((diario_uri, diario.dr_number, Literal(dn)))
        diarios_rep.add(dn)

    g.add((diario_uri, diario.publica, diploma_uri))
    g.add((diploma_uri, diario.publicado, diario_uri))

    id += 1

    # Salvar o grafo RDF periodicamente
    if leng > 100000:
        file += 1
        g.serialize(destination=f"ontologias/diario_da_republica_populated{file}.ttl", format="turtle", append=True)
        # Limpar o grafo para evitar consumo excessivo de memória
        g = Graph()
        leng = 0

# Salvar o grafo RDF atualizado
file += 1
g.serialize(destination=f"ontologias/diario_da_republica_populated{file}.ttl", format="turtle")
