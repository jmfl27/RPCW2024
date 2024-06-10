from flask import Flask, render_template, jsonify, request, redirect
import requests
from datetime import datetime

from icecream import ic

app = Flask(__name__)

max_diplomas = 20

# data do sistema em formato ANSI ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime('%Y-%m-%dT%H:%M:%S')


# Página inicial
@app.get('/')
def pag_inicial():
    return render_template('index.html', data={"data": data_iso_formatada})


# Página Entidades
@app.get('/entidades')
def pag_entidades():
    resposta = requests.get('http://127.0.0.1:5000/entidades')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('entidades.html', data = {"data" : data, "tempo": data_iso_formatada})
    else:
        return jsonify({"erro": f"Erro ao buscar dados da pagina inicial"}), 400
    
# Página de uma Entidade
@app.get('/entidades/<name>')
def pag_entidade(name):

    resposta = requests.get(f'http://127.0.0.1:5000/entidades?name={name}')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('entidade.html', data = {"data" : data, "tempo": data_iso_formatada})
    else:
        return jsonify({"erro": f"Erro ao buscar dados da pagina inicial"}), 400

# Página de Tipos
@app.get('/tipos')
def pag_tipos():

    resposta = requests.get(f'http://127.0.0.1:5000/tipos')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('tipos.html', data = {"data" : data, "tempo": data_iso_formatada})
    else:
        return jsonify({"erro": f"Erro ao buscar dados da pagina inicial"}), 400

# Página de uma Tipo
@app.get('/tipos/<tipo>')
def pag_tipo(tipo):

    resposta = requests.get(f'http://127.0.0.1:5000/tipos?tipo={tipo}')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('tipo.html', data = {"data" : data, "tempo": data_iso_formatada})
    else:
        return jsonify({"erro": f"Erro ao buscar dados da pagina inicial"}), 400

# Página de Diplomas
@app.get('/diplomas')
def pag_diplomas():

    page = request.args.get('page', type=int)
    query = request.args.get('query')
    category= request.args.get('category')

    if not page or (int(page)==0):
        page = 1

    if query and query != "":
        if not category:
            category = 'identificacao_diploma'
        buttons = (
            f'?query={query}&category={category}&page={page + 1}',
            f'?query={query}&category={category}&page={page - 1}'
        )
        url = f'http://127.0.0.1:5000/diplomas?query={query}&category={category}&page={page-1}'
    else:
        if not page or int(page) == 0:
            url = f'http://127.0.0.1:5000/diplomas?page=0'
        else:
            url = f'http://127.0.0.1:5000/diplomas?page={page-1}'
        buttons = (
            f'?page={page + 1}',
            f'?page={page - 1}'
        )

    resposta = requests.get(url)
    if resposta.status_code == 200:
        data = resposta.json()
        page_next = page + 1
        prev_page = page - 1
        
        if(len(data) < 20):
            buttons = (
            f'?query={query}&category={category}&page={page - 1}'
        )
            if page == 1:
                buttons = ()
        elif page == 1:
            prev_page = page_next
            buttons = (
            f'?query={query}&category={category}&page={page_next}'
        )
        return render_template('diplomas.html', data = {"data" : data, "tempo": data_iso_formatada, "buttons": buttons, "prev_page": prev_page ,"next_page": page_next, "query": query, "category": category})
    else:
        return jsonify({"erro": f"Erro ao buscar dados da pagina inicial"}), 400
    
# Página de um Diploma
@app.get('/diplomas/<id>')
def pag_diploma(id):
    resposta = requests.get(f'http://127.0.0.1:5000/diplomas?id={id}')
    if resposta.status_code == 200:
        data = resposta.json()
        ic(data)
        return render_template('diploma.html', data = {"data" : data, "tempo": data_iso_formatada,"id_dip": str(id)})
    else:
        return jsonify({"erro": f"Erro ao buscar dados do diploma {id}"}), 400

# Pagina de Criar Diploma
@app.get('/diplomas/form')
def diploma_form():
    resposta = requests.get(f'http://127.0.0.1:5000/tipos')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('diploma_form.html', data_iso_formatada=data_iso_formatada,data=data)
    else:
        return jsonify({"erro": f"Erro ao buscar os tipos existentes"}), 400

@app.post('/diplomas/form')
def submit_diploma_form():
    form_data = {
        "data_publicacao": request.form['data_publicacao'],
        "local_publicacao": request.form['local_publicacao'],
        "numero_publicacao": request.form['numero_publicacao'],
        "preambulo": request.form['preambulo'],
        "sumario": request.form['sumario'],
        "articulado": request.form['articulado'],
        "dr_number": request.form['dr_number'],
        "tipo": request.form['tipo'],
        "emissor": request.form['emissor'].split(",")
    }
    response = requests.post(f'http://127.0.0.1:5000//diplomas', json=form_data)
    if response.status_code == 200:
        return redirect('/diplomas/form?success=true')
    else:
        return jsonify({"erro": "Erro ao criar diploma"}), 400
    
# Criar um diploma
@app.post('/diplomas')
def create_diploma():
    form_data = request.json
    resposta = requests.post('http://127.0.0.1:5000/diplomas', json=form_data)
    if resposta.status_code == 200:
        return jsonify({"mensagem": "Diploma criado com sucesso"}), 200
    else:
        return jsonify({"erro": "Erro ao criar diploma"}), 400    

# Apagar diploma cujo id foi fornecido
@app.post('/delete_diploma/<id>')
def delete_diploma(id):
    # Exemplo de implementação:
    response = requests.delete(f'http://127.0.0.1:5000/diplomas/{id}')
    if response.status_code == 200:
        return redirect('/diplomas')  # Redirecionar de volta para a página de diplomas após a exclusão
    else:
        return jsonify({"erro": f"Erro ao apagar diploma com ID: {id}"}), 400


# Pagina de Criar Diploma
@app.get('/diplomas/edit/<id>')
def diploma_edit_form(id):
    dados = requests.get(f'http://127.0.0.1:5000/diplomas?id={id}')
    resposta = requests.get(f'http://127.0.0.1:5000/tipos')
    if resposta.status_code == 200:
        data = resposta.json()
        return render_template('diploma_edit_form.html', data_iso_formatada=data_iso_formatada,dados=dados.json(),data=data,id_dip=str(id))
    else:
        return jsonify({"erro": f"Erro ao buscar os tipos existentes"}), 400
    
@app.post('/diplomas/edit/form/<id>')
def update_diploma(id):
    form_data = {
        "data_publicacao": request.form['data_publicacao'],
        "local_publicacao": request.form['local_publicacao'],
        "numero_publicacao": request.form['numero_publicacao'],
        "preambulo": request.form['preambulo'],
        "sumario": request.form['sumario'],
        "articulado": request.form['articulado'],
        "dr_number": request.form['dr_number'],
        "tipo": request.form['tipo'],
        "emissor": request.form['emissor'].split(",")
    }
    response = requests.put(f'http://127.0.0.1:5000//diplomas/{id}', json=form_data)
    if response.status_code == 200:
        return redirect(f'/diplomas/{id}?success=true')
    else:
        return jsonify({"erro": "Erro ao criar diploma"}), 400

if __name__ == '__main__':
    app.run(port=8000, debug=True)