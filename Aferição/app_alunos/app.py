from flask import Flask, render_template, url_for, jsonify, request
from datetime import datetime
import requests
import json

app = Flask(__name__)

#dat do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')

#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/Alunos"

@app.route('/api/alunos', methods=['GET'])
def alunos():
    curso = request.args.get('curso')
    group = request.args.get('groupBy')

    if curso:
        print(curso)
        sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT ?idAluno ?nome WHERE {{
            ?s :idAluno ?idAluno;
                :nome ?nome;
                :curso "{curso}".
        }}
        ORDER BY asc(?nome)
        """
        payload = {"query": sparql_query}
        response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            data = response.json()["results"]["bindings"]
            alunos = []
            for row in data:
                aluno = {
                    "idAluno": row["idAluno"]["value"],
                    "nome": row["nome"]["value"]
                }
                alunos.append(aluno)
            return jsonify(alunos)
        else:
            return jsonify({"error": "No data found"}), 404
    elif group == 'curso':
        print(group)
        sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT ?curso (COUNT(?aluno) AS ?numAlunos)
        WHERE {{
                ?aluno rdf:type :Aluno.
                ?aluno :curso ?curso.
        }}
        GROUP BY ?curso
        ORDER BY asc(?curso)
        """
        payload = {"query": sparql_query}
        response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            data = response.json()["results"]["bindings"]
            alunos = []
            for row in data:
                aluno = {
                    "curso": row["curso"]["value"],
                    "numero": row["numAlunos"]["value"]
                }
                alunos.append(aluno)
            return jsonify(alunos)
        else:
            return jsonify({"error": "No data found"}), 404
    elif group == 'projeto':
        print(group)
        sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT ?notaProjeto (COUNT(?aluno) AS ?numAlunos)
        WHERE {{
                ?aluno rdf:type :Aluno.
                ?aluno :notaProjeto ?notaProjeto.
        }}
        GROUP BY ?notaProjeto
        ORDER BY asc(?notaProjeto)
        """
        payload = {"query": sparql_query}
        response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            data = response.json()["results"]["bindings"]
            alunos = []
            for row in data:
                aluno = {
                    "notaProjeto": row["notaProjeto"]["value"],
                    "numero": row["numAlunos"]["value"]
                }
                alunos.append(aluno)
            return jsonify(alunos)
        else:
            return jsonify({"error": "No data found"}), 404
    elif group == 'recurso':
        print(group)
        sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT ?idAluno ?nome ?curso ?recurso
        WHERE {{
            ?s :idAluno ?idAluno;
            :nome ?nome;
            :curso ?curso;
            :fezExame ?exame.
            ?exame :notaExame ?recurso.
            FILTER(contains(str(?exame), "_R"))
        }}
        ORDER BY asc(?nome)
        """
        payload = {"query": sparql_query}
        response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            data = response.json()["results"]["bindings"]
            alunos = []
            for row in data:
                aluno = {
                    "idAluno": row["idAluno"]["value"],
                    "nome": row["nome"]["value"],
                    "curso": row["curso"]["value"],
                    "recurso": row["recurso"]["value"]
                }
                alunos.append(aluno)
            return jsonify(alunos)
        else:
            return jsonify({"error": "No data found"}), 404
    else:
        sparql_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT DISTINCT ?idAluno ?nome ?curso WHERE {{
            ?s :idAluno ?idAluno;
                :nome ?nome;
                :curso ?curso.
        }}
        ORDER BY asc(?nome)
        """
        payload = {"query": sparql_query}
        response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

        if response.status_code == 200:
            data = response.json()["results"]["bindings"]
            alunos = []
            for row in data:
                aluno = {
                    "idAluno": row["idAluno"]["value"],
                    "nome": row["nome"]["value"],
                    "curso": row["curso"]["value"]
                }
                alunos.append(aluno)
            return jsonify(alunos)
        else:
            return jsonify({"error": "No data found"}), 404
    
@app.route('/api/alunos/<string:id>', methods=['GET'])
def aluno(id):
    sparql_query = f"""
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

    SELECT ?idAluno ?nome ?curso ?exame ?notaExame ?notaProjeto ?tp ?notaTPC WHERE {{
        ?aluno rdf:type :Aluno.
        ?aluno :idAluno "{id}";
               :idAluno ?idAluno;
                :nome ?nome;
                :curso ?curso;
                :notaProjeto ?notaProjeto;
                :fezExame ?exame;
                :fezTPC ?tpc.
        ?tpc :notaTPC ?notaTPC;
             :tp ?tp.
        ?exame :notaExame ?notaExame.
    }}
    ORDER BY asc(?nome)
    """
    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        alunos = []
        for row in data:
            aluno_exists = next((a for a in alunos if a["idAluno"] == row["idAluno"]["value"]), None)
            if aluno_exists:
                if "notaExame" in row and row["exame"]["value"].split("/")[-1] not in [e["exame"] for e in aluno_exists["exames"]]:
                    tipo = row["exame"]["value"].split("_")[1]
                    aluno_exists["exames"].append({
                        "exame": row["exame"]["value"].split("/")[-1],
                        "notaExame": row["notaExame"]["value"],
                        "tipo" : "Especial" if tipo == 'E' else "Normal" if tipo == 'N' else "Recurso" if tipo == 'R' else None
                    })
                if "notaTPC" in row and row["tp"]["value"] not in [t["tp"] for t in aluno_exists["tpc"]]:
                    aluno_exists["tpc"].append({
                        "tp": row["tp"]["value"],
                        "notaTPC": row["notaTPC"]["value"]
                    })
            else:
                aluno = {
                    "idAluno": row["idAluno"]["value"],
                    "nome": row["nome"]["value"],
                    "curso": row["curso"]["value"],
                    "exames": [],
                    "tpc": [],
                    "projeto": row["notaProjeto"]["value"]
                }
                if "notaExame" in row:
                    tipo = row["exame"]["value"].split("_")[1]
                    aluno["exames"].append({
                        "exame": row["exame"]["value"].split("/")[-1],
                        "notaExame": row["notaExame"]["value"],
                        "tipo" : "Especial" if tipo == 'E' else "Normal" if tipo == 'N' else "Recurso" if tipo == 'R' else None
                    })
                if "notaTPC" in row:
                    aluno["tpc"].append({
                        "tp": row["tp"]["value"],
                        "notaTPC": row["notaTPC"]["value"]
                    })
                alunos.append(aluno)
        return jsonify(alunos)
    else:
        return jsonify({"error": "No data found"}), 404


@app.route('/api/alunos/tpc', methods=['GET'])
def tpc():
    sparql_query= """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

SELECT ?idAluno ?nome ?curso (COUNT(?tpc) AS ?countTPC)
WHERE {
        ?aluno rdf:type :Aluno.
        ?aluno :idAluno ?idAluno;
                :nome ?nome;
                :curso ?curso;
                :fezTPC ?tpc.
        ?tpc :tp ?tp.
}
GROUP BY ?idAluno ?nome ?curso
ORDER BY asc(?nome)
"""
    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})

    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        alunos = []
        for row in data:
            aluno = {
                "idAluno": row["idAluno"]["value"],
                "nome": row["nome"]["value"],
                "curso": row["curso"]["value"],
                "tpcFeitos": row["countTPC"]["value"]
            }
            alunos.append(aluno)
        return jsonify(alunos)
    else:
        return jsonify({"error": "No data found"}), 404
    
@app.route('/api/alunos/avaliados', methods=['GET'])
def resultados():
    sparql_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/Alunos/>

        SELECT ?idAluno ?nome ?curso (GROUP_CONCAT(DISTINCT ?tp; SEPARATOR=", ") AS ?tps) (GROUP_CONCAT(DISTINCT ?notaTPC; SEPARATOR=", ") AS ?notasTPC) (MAX(?notaExame) AS ?maxNotaExame) ?notaProjeto
        WHERE {
            ?aluno rdf:type :Aluno.
            ?aluno :idAluno ?idAluno;
                    :nome ?nome;
                    :curso ?curso;
                    :notaProjeto ?notaProjeto;
                    :fezExame ?exame;
                    :fezTPC ?tpc.
            ?tpc :notaTPC ?notaTPC;
                :tp ?tp.
            ?exame :notaExame ?notaExame.
        }
        GROUP BY ?idAluno ?nome ?curso ?notaProjeto
        ORDER BY asc(?nome)
    """

    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload, headers={'Accept': 'application/sparql-results+json'})
    
    # Processar os resultados da consulta SPARQL e calcular a nota final de cada aluno
    alunos = []
    for result in response.json()['results']['bindings']:
        nota_projeto = float(result['notaProjeto']['value'])
        max_nota_exame = float(result['maxNotaExame']['value'])
        notas_tpc = [float(nota) for nota in result['notasTPC']['value'].split(", ")]
        
        nota_final = sum(notas_tpc) + 0.4 * nota_projeto + 0.4 * max_nota_exame
        
        if nota_projeto < 10 or max_nota_exame < 10 or nota_final < 10:
            nota_final = "R"
        
        aluno = {
            "idAluno": result['idAluno']['value'],
            "nome": result['nome']['value'],
            "curso": result['curso']['value'],
            "notaFinal": nota_final
        }
        alunos.append(aluno)
    
    return jsonify(alunos)

if __name__ == '__main__':
    app.run(debug=True)