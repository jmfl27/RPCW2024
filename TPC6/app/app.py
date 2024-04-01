from flask import Flask, render_template, url_for
from datetime import datetime
import requests

app = Flask(__name__)

#dat do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB endpoint
graphdb_endpoint = "http://epl.di.uminho.pt:7200/repositories/cinema2024"

def treatGroups(data):

    for value in data:
        if "name" not in value.keys():
            value["name"] = {'type': 'literal', 'value': ''}
        if "number" not in value.keys():
            value["number"] = {'datatype': 'http://www.w3.org/2001/XMLSchema#integer', 'type': 'literal', 'value': ''}

def organize_film_data(sparql_response):
    film_data = {
        "title": None,
        "duration": None,
        "date": None,
        "actors": set(),
        "composers": set(),
        "countries": set(),
        "directors": set(),
        "genres": set(),
        "producers": set(),
        "screenwriters": set(),
        "writers": set()
    }

    for binding in sparql_response:
        if "title" in binding:
            film_data["title"] = binding["title"]["value"]
        if "duration" in binding:
            film_data["duration"] = binding["duration"]["value"]
        if "date" in binding:
            film_data["date"] = binding["date"]["value"]
        if "actorName" in binding:
            film_data["actors"].add(binding["actorName"]["value"])
        if "composerName" in binding:
            film_data["composers"].add(binding["composerName"]["value"])
        if "countryName" in binding:
            film_data["countries"].add(binding["countryName"]["value"])
        if "directorName" in binding:
            film_data["directors"].add(binding["directorName"]["value"])
        if "genreName" in binding:
            film_data["genres"].add(binding["genreName"]["value"])
        if "producerName" in binding:
            film_data["producers"].add(binding["producerName"]["value"])
        if "screenwriterName" in binding:
            film_data["screenwriters"].add(binding["screenwriterName"]["value"])
        if "writerName" in binding:
            film_data["writers"].add(binding["writerName"]["value"])

    return film_data

@app.route('/')
def index():
    return render_template('index.html',data = {"data": data_iso_formatada})

@app.route('/filmes')
def filmes():
    sparql_query= f"""
prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?title ?duration where {{
    ?filme a :Film ;
       :title ?title .
    optional {{
        ?filme :duration ?duration
    }}
}}
order by ?title
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('filmes.html',data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/filmes/<string:titulo>')
def filme(titulo):
    sparql_query=f"""
    prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
    select ?title ?duration ?date ?actorName ?composerName ?countryName ?directorName ?genreName ?producerName ?screenwriterName ?writerName where {{
    ?film a :Film .
    ?film :title "{titulo}" .
    optional {{
        ?film :duration ?duration.
    }}
    optional {{
        ?film :date ?date.
    }}
    optional {{
        ?film :hasActor ?actor.
        ?film :name ?actorName.
    }}
    optional {{
        ?film :hasComposer ?composer.
        ?film :name ?composerName.
    }}
    optional {{
        ?film :hasCountry ?country.
        ?film :name ?countryName.
    }}
    optional {{
        ?film :hasDirector ?director.
        ?film :name ?directorName.
    }}
    optional {{
        ?film :hasGenre ?genre.
        ?film :name ?genreName.
    }}
    optional {{
        ?film :hasProducer ?producer.
        ?film :name ?producerName.
    }}
    optional {{
        ?film :hasScreenwriter ?screenwriter.
        ?film :name ?screenwriterName.
    }}
    optional {{
        ?film :hasWriter ?writer.
        ?film :name ?writerName.
    }}
}}
"""
    payload = {"query": sparql_query}
    response = requests.get (graphdb_endpoint, params=payload,
        headers={'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        dados = response.json()["results"]["bindings"]
        film_data = organize_film_data(dados)
        return render_template('filme.html', film_data=film_data, tempo=data_iso_formatada)
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/atores')
def atores():
    sparql_query= f"""
prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
select * where {{
    ?actor a :Actor.
    ?actor :name ?actorName.
    optional {{
        ?actor :birthDate ?birthDate.
    }}
}}
order by ?actorName
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('atores.html',data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/atores/<string:nome>')
def ator(nome):
    sparql_query= f"""
prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?actorName ?birthDate ?filmTitle where {{
    ?actor a :Actor.
    ?actor :name ?actorName.
    ?actor :name "{nome}".
    optional {{
        ?actor :birthDate ?birthDate.
    }}
    ?film a :Film.
    ?film :hasActor ?actor.
    ?film :title ?filmTitle.
}}
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('ator.html',data = {"data" : dados, "tempo": data_iso_formatada, "actor": dados[0]})
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/realizadores')
def realizadores():
    sparql_query= f"""
prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
select * where {{
    ?director a :Director.
    ?director :name ?directorName.
}}
order by ?directorName
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('realizadores.html',data = {"data" : dados, "tempo": data_iso_formatada})
    else:
        return render_template('empty.html', data = data_iso_formatada)

@app.route('/realizadores/<string:nome>')
def realizador(nome):
    sparql_query= f"""
prefix : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?actorName ?filmTitle where {{
    ?director a :Director.
    ?director :name ?directorName.
    ?director :name "{nome}".
    
    ?film a :Film.
    ?film :hasDirector ?director.
    ?film :title ?filmTitle.
}}
"""
    resposta = requests.get(graphdb_endpoint, 
                            params={"query": sparql_query}, 
                            headers={'Accept':'application/sparql-results+json'})
    if resposta.status_code == 200:
        dados = resposta.json()['results']['bindings']
        return render_template('realizador.html',data = {"data" : dados, "tempo": data_iso_formatada, 'director': dados[0]})
    else:
        return render_template('empty.html', data = data_iso_formatada)    

if __name__ == '__main__':
    app.run(debug=True)