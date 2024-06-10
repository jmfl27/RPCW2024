from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

from icecream import ic

import datetime

app = Flask(__name__)

max_diplomas = 20

a = '\n'

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

def organize_data(sparql_response):
    diploma_data = {
        "identificacao": None,
        "emissor": set(),
        "data_publicacao": None,
        "local_publicacao": None,
        "numero_publicacao": None,
        "preambulo": None,
        "sumario": None,
        "articulado": None,
        "dr_number" : None,
        "tipo": None
    }

    i = 0
    for binding in sparql_response:
        if i == 0:
            if "identificacao" in binding:
                diploma_data["identificacao"] = binding["identificacao"]["value"]
            if "data_publicacao" in binding:
                diploma_data["data_publicacao"] = binding["data_publicacao"]["value"]
            if "local_publicacao" in binding:
                diploma_data["local_publicacao"] = binding["local_publicacao"]["value"]
            if "numero_publicacao" in binding:
                diploma_data["numero_publicacao"] = binding["numero_publicacao"]["value"]
            if "preambulo" in binding:
                diploma_data["preambulo"] = binding["preambulo"]["value"]
            if "sumario" in binding:
                diploma_data["sumario"] = binding["sumario"]["value"]
            if "articulado" in binding:
                diploma_data["articulado"] = binding["articulado"]["value"]
            if "dr_number" in binding:
                diploma_data["dr_number"] = binding["dr_number"]["value"]
            if "tipo" in binding:
                diploma_data["tipo"] = binding["tipo"]["value"].split('/')[-1]
        if "emissor" in binding:
            diploma_data["emissor"].add(binding["emissor"]["value"])

        i += 1

    diploma_data["emissor"] = list(diploma_data["emissor"])
    return diploma_data

# (R) Listar todos os diplomas
#
def get_all_diplomas(page):
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
    SELECT ?diploma ?identificacao ?data_publicacao
    WHERE {{ 
        ?diploma rdf:type :Diploma;
        :identificacao_diploma ?identificacao;
        :data_publicacao ?data_publicacao
    }}
    ORDER BY ?identificacao
    OFFSET {(page)*max_diplomas}
    LIMIT {max_diplomas}
    """
    resultado = sparql_get_query(query)
    diplomas = []
    for linha in resultado['results']['bindings']:
        diploma = {
            "diploma_id" : linha['diploma']['value'].split('/')[-1],
            "identificacao": linha['identificacao']['value'],
            "data_publicacao": linha['data_publicacao']['value']
        }
        diplomas.append(diploma)
    return diplomas

def get_search_diplomas(input_query, category, page):
    if category == "entidade_emissora":
        query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        SELECT ?diploma ?identificacao ?data_publicacao 
        WHERE {{
        ?diploma a :Diploma ;
                :identificacao_diploma ?identificacao ;
                :data_publicacao ?data_publicacao .
        ?diploma :emitido ?entidade .
        ?entidade  :{category} ?texto .
        FILTER(regex(?texto, "{input_query}", "i"))
        }}
        LIMIT {max_diplomas}
        OFFSET {page*max_diplomas}
        """

    else:
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        SELECT ?diploma ?identificacao ?data_publicacao 
        WHERE {{
            ?diploma a :Diploma ;
                    :identificacao_diploma ?identificacao ;
                    :data_publicacao ?data_publicacao .
            ?diploma :{category} ?texto .
            FILTER(regex(?texto, "{input_query}", "i"))
        }}
        ORDER BY ?text
        OFFSET {page*max_diplomas}
        LIMIT {max_diplomas}
    """

    resultado = sparql_get_query(query)
    diplomas = []

    for linha in resultado['results']['bindings']:
        diploma = {
            "diploma_id" : linha['diploma']['value'].split('/')[-1],
            "identificacao": linha['identificacao']['value'],
            "data_publicacao": linha['data_publicacao']['value']
        }
        diplomas.append(diploma)

    return diplomas

def get_diploma(id):
    query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
select ?identificacao ?data_publicacao ?numero_publicacao ?local_publicacao ?preambulo ?sumario ?articulado ?emissor ?dr_number ?tipo where {{
	:{id} rdf:type :Diploma;
       :identificacao_diploma ?identificacao;
       :data_publicacao ?data_publicacao;
       :local_publicacao ?local_publicacao;
       :numero_publicacao ?numero_publicacao;
       :preambulo ?preambulo ;
       :sumario ?sumario ;
       :articulado ?articulado .
    ?entidade :emite :{id} .
    ?entidade :entidade_emissora ?emissor.
    ?dr :publica :{id} .
    ?dr :dr_number ?dr_number .
    :{id} rdf:type ?tipo .
    ?tipo rdfs:subClassOf :Diploma .
}}
    """
    resultado = sparql_get_query(query)
    diploma = organize_data(resultado['results']['bindings'])
    return diploma


@app.route('/diplomas')
def get_diplomas():

    id = request.args.get('id')
    page = request.args.get('page')
    query = request.args.get('query')
    category = request.args.get('category')

    if not page:
        page = 1

    if id:
        data = get_diploma(id)
    else:
        if not query or query=="" or query=="None":
            data = get_all_diplomas(int(page))
        else:
            data = get_search_diplomas(query, category, int(page))
    return jsonify(data), 200

def get_all_entidades():
    query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
PREFIX ns1: <http://rpcw.di.uminho.pt/2024/diario-republica/>
SELECT ?n (COUNT(?e) as ?nPub)
WHERE {{
	?entidade rdf:type :Entidade_Emissora;
            :entidade_emissora ?n;
    		:emite ?e
}}
GROUP BY ?n ?entidade
ORDER BY ?n 
    """
    resultado = sparql_get_query(query)
    entidades = []
    for linha in resultado['results']['bindings']:
        entidade = {
            "entidade": linha["n"]["value"],
            "nPub": linha["nPub"]["value"]
        }
        entidades.append(entidade)
    
    return entidades

def get_entidade(name):

    query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
PREFIX ns1: <http://rpcw.di.uminho.pt/2024/diario-republica/>
SELECT ?e ?identficacao
WHERE {{
	?entidade rdf:type :Entidade_Emissora;
            :entidade_emissora '{name}';
    		:emite ?e .
    ?e :identificacao_diploma ?identficacao . 
}}
    """
    resultado = sparql_get_query(query)
    entidade = {"entidade": name,
                "documentos": set()}
    
    for d in resultado['results']['bindings']:
        entidade['documentos'].add((d['e']['value'].split('/')[-1],d['identficacao']['value']))

    entidade['documentos'] = list(entidade['documentos'])

    return entidade

@app.get('/entidades')
def get_entidades():

    name = request.args.get('name')
    if name:
        data = get_entidade(name)
    else:
        data = get_all_entidades()

    
    return jsonify(data), 200

def get_all_tipos():
    query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
PREFIX ns1: <http://rpcw.di.uminho.pt/2024/diario-republica/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?entidade (COUNT(?d) as ?nPub)
WHERE {{
	?entidade rdfs:subClassOf :Diploma.
    ?d rdf:type ?entidade 
}}GROUP BY ?entidade
    """
    resultado = sparql_get_query(query)
    tipos = []
    for linha in resultado['results']['bindings']:
        tipo = {
            "tipo": linha["entidade"]["value"].split('/')[-1],
            "nPub": linha["nPub"]["value"]
        }
        tipos.append(tipo)
    
    return tipos

def get_tipo(tipo):

    query = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
PREFIX ns1: <http://rpcw.di.uminho.pt/2024/diario-republica/>
SELECT ?t ?n
WHERE {{
    ?t rdf:type :{tipo} ;
       :identificacao_diploma ?n.
}}
    """
    resultado = sparql_get_query(query)
    entidade = {"entidade": tipo,
                "documentos": set()}
    
    for d in resultado['results']['bindings']:
        entidade['documentos'].add(((d['t']['value'].split('/')[-1],d['n']['value'])))

    entidade['documentos'] = list(entidade['documentos'])

    return entidade

@app.get('/tipos')
def get_tipos():

    tipo = request.args.get('tipo')

    if tipo:
        data = get_tipo(tipo)
    else:
        data = get_all_tipos()

    return jsonify(data), 200


@app.get('/diplomas/search/count')
def count_search_diplomas():
    tipo = request.args.get('tipo')
    texto = request.args.get('texto')
    
    # Verifique se os parâmetros 'tipo' e 'texto' foram fornecidos
    if not tipo or not texto:
        return jsonify({"erro": "Os parâmetros 'tipo' e 'texto' são necessários."}), 400
    
    # Verifique se o tipo é válido
    valid_types = ["identificacao_diploma", "data_publicacao", "local_publicacao", "numero_publicacao", "preambulo", "sumario", "articulado"]
    if tipo not in valid_types:
        return jsonify({"erro": f"Tipo inválido. Os tipos válidos são: {', '.join(valid_types)}"}), 400
    
    if tipo == "entidade_emissora":
            query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>

        SELECT (COUNT(?diploma) as ?count)
        WHERE {{
            ?diploma a :Diploma .
            ?diploma :emitido ?entidade .
            ?entidade :{tipo} ?texto.

            FILTER(regex(?texto, "{texto}", "i"))
        }}

        """

    else:
        query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>

        SELECT (COUNT(?diploma) as ?count)
        WHERE {{
            ?diploma a :Diploma .
            ?diploma :{tipo} ?texto.

            FILTER(regex(?texto, "{texto}", "i"))
        }}

        """
    resultado = sparql_get_query(query)
    count = resultado['results']['bindings'][0]['count']['value']
    return jsonify(int(count)), 200

@app.get('/diplomas/search/<offset>')
def search_offset_diplomas(offset):
    tipo = request.args.get('tipo')
    texto = request.args.get('texto')

    # Verifique se os parâmetros 'tipo' e 'texto' foram fornecidos
    if not tipo or not texto:
        return jsonify({"erro": "Os parâmetros 'tipo' e 'texto' são necessários."}), 400

    # Verifique se o tipo é válido
    valid_types = ["identificacao_diploma", "data_publicacao", "local_publicacao", "numero_publicacao", "preambulo", "sumario", "articulado", "doc_type", "entidade_emissora"]
    if tipo not in valid_types:
        return jsonify({"erro": f"Tipo inválido. Os tipos válidos são: {', '.join(valid_types)}"}), 400

    if tipo == "entidade_emissora":
            query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        SELECT ?diploma ?identificacao ?data_publicacao ?local_publicacao ?numero_publicacao ?preambulo ?sumario ?articulado
        WHERE {{
        ?diploma a :Diploma ;
                :identificacao_diploma ?identificacao ;
                :data_publicacao ?data_publicacao ;
                :local_publicacao ?local_publicacao ;
                :numero_publicacao ?numero_publicacao ;
                :preambulo ?preambulo ;
                :sumario ?sumario ;
                :articulado ?articulado .
        ?diploma :emitido ?entidade .
        ?entidade  :{tipo} ?texto .
        FILTER(regex(?texto, "{texto}", "i"))
        }}
        LIMIT {max_diplomas}
        OFFSET {offset}
        """

    else:
        query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        SELECT ?diploma ?identificacao ?data_publicacao ?local_publicacao ?numero_publicacao ?preambulo ?sumario ?articulado
        WHERE {{
        ?diploma a :Diploma ;
                :identificacao_diploma ?identificacao ;
                :data_publicacao ?data_publicacao ;
                :local_publicacao ?local_publicacao ;
                :numero_publicacao ?numero_publicacao ;
                :preambulo ?preambulo ;
                :sumario ?sumario ;
                :articulado ?articulado .
        ?diploma :{tipo} ?texto .
        FILTER(regex(?texto, "{texto}", "i"))
        }}
        LIMIT {max_diplomas}
        OFFSET {offset}
        """
    resultado = sparql_get_query(query)
    diplomas = []
    for linha in resultado['results']['bindings']:
        diploma = {
            "diploma_id" : linha['diploma']['value'].split('/')[-1],
            "identificacao": linha['identificacao']['value'],
            "data_publicacao": linha['data_publicacao']['value'],
            "local_publicacao": linha['local_publicacao']['value'],
            "numero_publicacao": linha['numero_publicacao']['value'],
            "preambulo": linha['preambulo']['value'],
            "sumario": linha['sumario']['value'],
            "articulado": linha['articulado']['value']
        }
        diplomas.append(diploma)
    return jsonify(diplomas), 200

def criaEmissores(dados):
    entidades = []
    for dado in dados:
        entidades.append(f"{{?entidade rdf:type :Entidade_Emissora . ?entidade :entidade_emissora \"{dado}\", ?emissor .}}")
    emissor_query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT distinct ?emissor WHERE{{
                {(a+"UNION").join(entidades)}
        }}
        """
    resultado = sparql_get_query(emissor_query)
    
    cria_emissores = []
    string_emissores = ""
    
    values = []
    for value in resultado['results']['bindings']:
        values.append(value['emissor']['value'])

    for dado in dados:
        if dado not in values:
            aux = dado.replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_')
            cria_emissores.append(f":{aux} a :Entidade_Emissora, owl:NamedIndividual ;")
            cria_emissores.append(f":entidade_emissora \"{dado}\" .")
            string_emissores += dado + " "

    if cria_emissores != []:
        cria_emissor_query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        INSERT DATA{{
            {a.join(cria_emissores)}
        }}
        """ 
        sparql_query(cria_emissor_query)

    if string_emissores == "":
        return ""
    else:
        status = f"Entidade(s) Emissora(s) criada(s) com sucesso: {string_emissores}"
        return status[:-1]

def criaDR(dados):
    diario_query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT distinct ?dr WHERE{{
                ?dr rdf:type :Diario_da_Republica ;
                        :dr_number "{dados}" .
                }}
        """
    resultado = sparql_get_query(diario_query)

    cria_diarios = []
    string_diarios = ""
    if resultado['results']['bindings'] == []:
        cria_diarios.append(f":{dados.replace(' ', '_').replace('/','-')} a :Diario_da_Republica, owl:NamedIndividual ;")
        cria_diarios.append(f":dr_number \"{dados}\" .")
        string_diarios = dados

        cria_diario_query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        INSERT DATA{{
            {a.join(cria_diarios)}
        }}
        """ 
        sparql_query(cria_diario_query)

    if string_diarios == "":
        return ""
    else:
        status = f"Diário criado com sucesso: {string_diarios}"
        return status[:-1]



# (C)riar um diploma
#
@app.post('/diplomas')
def create_diploma():
    dados = request.json
    if not dados:
        return jsonify({"erro": "Não foram enviados dados do diploma a criar..."}), 400
    else:
        query_id = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
    PREFIX ns1: <http://rpcw.di.uminho.pt/2024/diario-republica/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT (COUNT(?entidade) as ?n)
    WHERE {{
        ?entidade a :Diploma.
    }}
"""
        resultado = sparql_get_query(query_id)
        id = int(resultado['results']['bindings'][0]['n']['value']) + 1
        status = status2 = ""
        triplos = []
        if "data_publicacao" in dados:
            triplos.append(f":{id} :data_publicacao \"{dados['data_publicacao']}\" .")
        if "local_publicacao" in dados:
            triplos.append(f":{id} :local_publicacao \"{dados['local_publicacao'] + '.ª Série'}\" .")
        if "numero_publicacao" in dados:
            triplos.append(f":{id} :numero_publicacao \"{dados['numero_publicacao']}\" .")
        if "preambulo" in dados:
            triplos.append(f":{id} :preambulo \"{dados['preambulo']}\" .")
        if "sumario" in dados:
            triplos.append(f":{id} :sumario \"{dados['sumario']}\" .")
        if "articulado" in dados:
            triplos.append(f":{id} :articulado \"{dados['articulado']}\" .")
        if "dr_number" in dados:
            status2 = criaDR(dados["dr_number"])
            triplos.append(f":{dados['dr_number'].replace(' ', '_').replace('/','-')} :publica :{id} .")
            triplos.append(f":{id} :publicado :{dados['dr_number'].replace(' ', '_').replace('/','-')} .")
        if "tipo" in dados:
            tipo = dados["tipo"]
            triplos.append(f":{id} :doc_type \"{tipo}\" .")
        if "data_publicacao" in dados and "numero_publicacao" in dados:
            dia, mes, ano = giveDate(dados["data_publicacao"])
            aux = f"{dados['numero_publicacao']}/{ano}"
            triplos.append(f":{id} :number \"{aux}\" .")
            if "tipo" in dados:
                aux = f"{dados['tipo'].replace('_',' ')} n.º {aux}, de {dia} de {mes}"
                triplos.append(f":{id} :identificacao_diploma \"{aux}\" .")
        if "emissor" in dados:
            status = criaEmissores(dados["emissor"])
            for emissor in dados["emissor"]:
                aux = emissor.replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_')
                triplos.append(f":{aux} :emite :{id} .")
                triplos.append(f":{id} :emitido :{aux} .")
                

        query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        INSERT DATA{{
            :{id} a :{tipo}, owl:NamedIndividual .
            {a.join(triplos)}
        }}
        """
        sparql_query(query)
        if status == "" and status2 == "":
            return jsonify({"mensagem": f"Diploma criado com sucesso: {id}"})
        elif status2 == "":
            return jsonify({"mensagem": f"Diploma criado com sucesso: {id}, {status}"})
        elif status == "":
            return jsonify({"mensagem": f"Diploma criado com sucesso: {id}, {status2}"})
        else:
            return jsonify({"mensagem": f"Diploma criado com sucesso: {id}, {status}, {status2}"})


# (D) Apagar um diploma
#
@app.delete('/diplomas/<id>')
def delete_diploma(id):
    aux_query = f"""
                PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
                SELECT DISTINCT ?dr_number ?emissor WHERE{{
                ?diario :publica :{id} ;
                          :dr_number ?dr_number .
                ?entidade :emite :{id} ;
                          :entidade_emissora ?emissor .
                }}
                """
    triplos_apagar = []
    resultado = sparql_get_query(aux_query)

    for linha in resultado['results']['bindings']:
        aux = linha['emissor']['value'].replace(' ', '_').replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_')
        triplos_apagar.append(f":{aux} :emite :{id} .")
        triplos_apagar.append(f":{id} :emitido :{aux} .")

    dr_number = resultado['results']['bindings'][0]['dr_number']['value'].replace(' ', '_').replace('/','-')
    triplos_apagar.append(f":{dr_number} :publica :{id} .")
    triplos_apagar.append(f":{id} :publicado :{dr_number} .")  

    query = f"""
    PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
    DELETE{{
        :{id} ?p ?o .
        {a.join(triplos_apagar)}
    }}
    WHERE{{
       :{id} ?p ?o . 
    }}
    """
    sparql_query(query)
    return jsonify({"mensagem": f"Indivíduo removido da base de dados: {id}"})


# (U) Alterar um diploma
#
@app.put('/diplomas/<id>')
def update_diploma(id):
    #FIX: falta acrescentar emissores
    dados = request.json
    if not dados:
        return jsonify({"erro": "Não foram enviados dados do diploma a alterar..."}), 400
    else:
        status = ""
        status2 = ""
        triplos_apagar = []
        triplos_inserir = []
        if "data_publicacao" in dados:
            triplos_apagar.append(f":{id} :data_publicacao ?o .")
            triplos_inserir.append(f":{id} :data_publicacao \"{dados['data_publicacao']}\" .")
        if "local_publicacao" in dados:
            triplos_apagar.append(f":{id} :local_publicacao ?o .")
            triplos_inserir.append(f":{id} :local_publicacao \"{dados['local_publicacao']}\" .")
        if "numero_publicacao" in dados:
            triplos_apagar.append(f":{id} :numero_publicacao ?o .")
            triplos_inserir.append(f":{id} :numero_publicacao \"{dados['numero_publicacao']}\" .")
        if "tipo" in dados:
            triplos_apagar.append(f":{id} a ?o .")
            triplos_apagar.append(f":{id} :doc_type ?o .")
            triplos_inserir.append(f":{id} a :{dados['tipo']}, owl:NamedIndividual  .")
            triplos_inserir.append(f":{id} :doc_type \"{dados['tipo']}\" .")
        if "data_publicacao" in dados or "numero_publicacao" in dados:
            aux_query = f"""
                PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    SELECT ?data_publicacao ?numero_publicacao ?tipo WHERE{{
                    :{id} :doc_type ?tipo ;
                            :data_publicacao ?data_publicacao ;
                            :numero_publicacao ?numero_publicacao.
                }}
                """
            resultado = sparql_get_query(aux_query)
            data_publicacao = resultado['results']['bindings'][0]['data_publicacao']['value']
            tipo = resultado['results']['bindings'][0]['tipo']['value']
            numero_publicacao = resultado['results']['bindings'][0]['numero_publicacao']['value']
            if "data_publicacao" in dados:
                data_publicacao = dados['data_publicacao']
            if "numero_publicacao" in dados:
                numero_publicacao = dados['numero_publicacao']
            if "tipo" in dados:
                tipo = dados['tipo']
            dia, mes, ano = giveDate(data_publicacao)
            aux = f"{numero_publicacao}/{ano}"
            triplos_apagar.append(f":{id} :number ?o .")
            triplos_inserir.append(f":{id} :number \"{aux}\" .")
            if "tipo" in dados:
                aux = f"{tipo} n.º {numero_publicacao}/{ano}, de {dia} de {mes}"
                triplos_apagar.append(f":{id} :identificacao_diploma ?o .")
                triplos_inserir.append(f":{id} :identificacao_diploma \"{aux}\" .")
        if "preambulo" in dados:
            triplos_apagar.append(f":{id} :preambulo ?o .")
            triplos_inserir.append(f":{id} :preambulo \"{dados['preambulo']}\" .")
        if "sumario" in dados:
            triplos_apagar.append(f":{id} :sumario ?o .")
            triplos_inserir.append(f":{id} :sumario \"{dados['sumario']}\" .")
        if "articulado" in dados:
            triplos_apagar.append(f":{id} :articulado ?o .")
            triplos_inserir.append(f":{id} :articulado \"{dados['articulado']}\" .")
        if "dr_number" in dados:
            diario_query = f"""
                PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
                SELECT ?dr_number WHERE{{
                ?diario :publica :{id} ;
                          :dr_number ?dr_number .
                }}
                """
            #Apagar as ligações do diário com o diploma
            resultado = sparql_get_query(diario_query)
            dr_number = resultado['results']['bindings'][0]['dr_number']['value'].replace(' ', '_').replace('/','-')
            triplos_apagar.append(f":{dr_number} :publica :{id} .")
            triplos_apagar.append(f":{id} :publicado :{dr_number} .")            

            #Inserir diário no diploma, que já existem nos dados
            status2 = criaDR(dados["dr_number"])
            aux = dados['dr_number'].replace(' ', '_').replace('/','-')
            triplos_inserir.append(f":{aux} :publica :{id} .")
            triplos_inserir.append(f":{id} :publicado :{aux} .")

        if "emissor" in dados:
            #Apagar as ligações de todos os emissores que emitem o diploma
            emissor_query = f"""
                PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
                SELECT ?emissor WHERE{{
                ?entidade :emite :{id} ;
                          :entidade_emissora ?emissor .
                }}
                """
            resultado = sparql_get_query(emissor_query)
            for linha in resultado['results']['bindings']:
                aux = linha['emissor']['value'].replace(' ', '_').replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_')
                triplos_apagar.append(f":{aux} :emite :{id} .")
                triplos_apagar.append(f":{id} :emitido :{aux} .")

            #Inserir emissores no diploma
            status = criaEmissores(dados["emissor"])
            for emissor in dados["emissor"]:
                aux = emissor.replace(' ', '_').replace('"','').replace('º','').replace('ª','').replace('%','').replace('\n','').replace('[','').replace(']','').replace('__','_').replace('__','_')
                triplos_inserir.append(f":{aux} :emite :{id} .")
                triplos_inserir.append(f":{id} :emitido :{aux} .")
                       
        query = f"""
        PREFIX : <http://rpcw.di.uminho.pt/2024/diario-republica/>
        DELETE{{
            {a.join(triplos_apagar)}
        }}
        INSERT{{
            {a.join(triplos_inserir)}
        }}
        WHERE{{
            :{id} ?p ?o . 
        }}
        """
        sparql_query(query)
        if status == "" and status2 == "":
            return jsonify({"mensagem": f"Diploma alterado com sucesso: {id}"})
        elif status2 == "":
            return jsonify({"mensagem": f"Diploma alterado com sucesso: {id}, {status}"})
        elif status == "":
            return jsonify({"mensagem": f"Diploma alterado com sucesso: {id}, {status2}"})
        else:
            return jsonify({"mensagem": f"Diploma alterado com sucesso: {id}, {status}, {status2}"})


# ------- Funções Auxiliares --------------------------
def sparql_get_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/diarioRepublica")
    sparql.setMethod('GET')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def sparql_query(query):
    sparql = SPARQLWrapper("http://localhost:7200/repositories/diarioRepublica/statements")
    sparql.setMethod('POST')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == '__main__':
    app.run(debug=True)