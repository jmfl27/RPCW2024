from flask import Flask, render_template, url_for
from datetime import datetime
import requests

app = Flask(__name__)

#dat do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/tabelaPeriodica"

def treatGroups(data):

    for value in data:
        if "name" not in value.keys():
            value["name"] = {'type': 'literal', 'value': ''}
        if "number" not in value.keys():
            value["number"] = {'datatype': 'http://www.w3.org/2001/XMLSchema#integer', 'type': 'literal', 'value': ''}

@app.route('/')
def index():
    return render_template('index.html',data = {"data": data_iso_formatada})

@app.route('/elementos/<int:na>')
def element(na):
    sparql_query=f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select * where {{
    ?s a tp:Element.
    ?s tp:name ?nome.
    ?s tp:symbol ?simb.
    ?s tp:group ?group_uri.
    ?s tp:atomicWeight ?peso.
    ?s tp:block ?bloco.
    ?s tp:casRegistryID ?cas.
    ?s tp:classification ?class.
    ?s tp:color ?cor.
    ?s tp:period ?periodo.
    ?s tp:standardState ?state.
    ?s tp:atomicNumber ?na.
    ?s tp:atomicNumber {na}.

    BIND(REPLACE(STR(?group_uri), STR(tp:), "") AS ?groupFragment)
    BIND(STRAFTER(?groupFragment, "_") AS ?groupNumeric)
}}
order by ?n
"""
    payload = {"query": sparql_query}
    response = requests.get (graphdb_endpoint, params=payload,
        headers={'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        dados = response.json()["results"]["bindings"]
        return render_template('elemento.html', entry = dados[0], tempo = data_iso_formatada)
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/elementos')
def elementos():
    sparql_query= """
prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
select * where{
    ?s a tp:Element ;
       tp:name ?nome ;
       tp:symbol ?simb ;
       tp:atomicNumber ?n ;
       tp:group ?group_uri .

       BIND(REPLACE(STR(?group_uri), STR(tp:), "") AS ?groupFragment)
       BIND(STRAFTER(?groupFragment, "_") AS ?groupNumeric)
}
order by ?n
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('elementos.html',data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/grupos/<string:grupo>')
def grupo(grupo):
    sparql_query = f"""
    PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?n ?gname ?simb ?name ?na WHERE {{
        :{grupo} rdf:type :Group ;
        optional{{:{grupo} :number ?n.}}
        optional{{:{grupo} :name ?gname.}}

        ?el :group :{grupo} ;
		    :symbol ?simb ;
            :name ?name ;
            :atomicNumber ?na .
    
    }}
    Order by ?na
    """

    resposta = requests.get(graphdb_endpoint, 
                            params = {"query": sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        print(dados)
        return render_template('grupo.html', data = dados, tempo = data_iso_formatada)
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/grupos')
def grupos():
    sparql_query = """
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?number ?name WHERE {
    ?s rdf:type :Group .
    Optional{ ?s :number ?number .}
    Optional{ ?s :name ?name .}
}
Order by ?number
"""

    resposta = requests.get(graphdb_endpoint, 
                            params = {"query": sparql_query}, 
                            headers = {'Accept': 'application/sparql-results+json'})
    
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        treatGroups(dados)
        return render_template('grupos.html', data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = {"data": data_iso_formatada})

if __name__ == '__main__':
    app.run(debug=True)