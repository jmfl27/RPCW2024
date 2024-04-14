import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("familia-base.ttl")

# Definir o namespace do seu grafo RDF
familia = Namespace("http://rpcw.di.uminho.pt/2024/familia/")

# Função para formatar URIs
def format_uri(idAluno):
    return URIRef(familia + idAluno)

# Parse the XML file
tree = ET.parse('royal.xml')

# Get the root element
root = tree.getroot()

# Print the name of the root element
#print(root.tag)

persons = []

# Loop through the child elements of the root element
for entrada in root.iter('person'):
    #print(entrada.tag, entrada.text)
    id = entrada.find('id').text
    person_uri = format_uri(id)
    persons.append(id)

    g.add((person_uri, RDF.type, OWL.NamedIndividual))
    g.add((person_uri, RDF.type, familia.Pessoa))
    g.add((person_uri, familia.nome, Literal(entrada.find('name').text)))

    for pai in entrada.iter('parent'):
        parent_id = pai.get('ref')
        parent_uri = format_uri(parent_id)
        parent = root.find(f'.//person[id="{parent_id}"]')
        parent_sex = parent.find('sex').text

        if parent_sex == 'F':
            g.add((person_uri, familia.temMae, parent_uri))
        elif parent_sex == 'M':
            g.add((person_uri, familia.temPai, parent_uri))
        else:
            print('OUTLIER')
            exit()

# Salvar o grafo RDF atualizado
g.serialize(destination="royal.ttl", format="turtle")