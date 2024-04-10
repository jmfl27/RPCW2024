import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("alunosBase.ttl")

# Definir o namespace do seu grafo RDF
alunos = Namespace("http://rpcw.di.uminho.pt/2024/Alunos/")

# Função para formatar URIs
def format_uri(idAluno):
    return URIRef(alunos + idAluno)

# Abrir o arquivo JSON e ler os dados
with open("aval-alunos.json", "r") as json_file:
    data = json.load(json_file)

# Iterar sobre cada entrada no arquivo JSON e adicionar as informações ao grafo RDF
for aluno in data["alunos"]:
    aluno_uri = format_uri(aluno['idAluno'])
    g.add((aluno_uri, RDF.type, OWL.NamedIndividual))
    g.add((aluno_uri, RDF.type, alunos.Aluno))
    g.add((aluno_uri, alunos.idAluno, Literal(aluno["idAluno"])))
    g.add((aluno_uri, alunos.nome, Literal(aluno["nome"])))
    g.add((aluno_uri, alunos.curso, Literal(aluno["curso"])))
    g.add((aluno_uri, alunos.notaProjeto, Literal(aluno["projeto"], datatype=XSD.int)))

    # Adicionar notas de TPC
    for tpc in aluno["tpc"]:
        tpc_uri = format_uri(aluno["idAluno"] + "_" + tpc["tp"])
        g.add((tpc_uri, RDF.type, alunos.TPC))
        g.add((tpc_uri, alunos.notaTPC, Literal(tpc["nota"], datatype=XSD.float)))
        g.add((tpc_uri, alunos.tp, Literal(tpc["tp"])))
        g.add((aluno_uri, alunos.fezTPC, tpc_uri))

    # Adicionar notas de exames
    for tipo, nota in aluno["exames"].items():
        exame_uri = format_uri(aluno["idAluno"] + "_" + tipo[0].upper())
        g.add((exame_uri, RDF.type, alunos[tipo.capitalize()]))
        g.add((exame_uri, alunos.notaExame, Literal(nota, datatype=XSD.int)))
        g.add((aluno_uri, alunos.fezExame, exame_uri))

# Salvar o grafo RDF atualizado
g.serialize(destination="aluno_populated.ttl", format="turtle")