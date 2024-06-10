import json

# Nome do ficheiro
file_name = 'new_data.json'

# Função para obter todos os "doc_classs" distintos
def obter_doc_classs_distintos(file_name):
    try:
        # Abrir e carregar o ficheiro JSON
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Verificar se o ficheiro contém uma lista
        if isinstance(data, list):
            # Criar um conjunto para armazenar "doc_classs" distintos
            doc_classs_distintos = set()
            
            # Iterar sobre os elementos da lista e adicionar "doc_classs" ao conjunto
            for item in data:
                if 'emiting_body' in item:
                    for entidade in item['emiting_body']:
                        doc_classs_distintos.add(entidade)
            
            # Mostrar os "doc_classs" distintos
            print('Doc Types Distintos:')
            for doc_class in doc_classs_distintos:
                print(doc_class)
        else:
            print('O ficheiro JSON não contém uma lista.')
    
    except FileNotFoundError:
        print(f'Erro: O ficheiro {file_name} não foi encontrado.')
    except json.JSONDecodeError:
        print('Erro: O ficheiro não está num formato JSON válido.')

# Chamar a função
obter_doc_classs_distintos(file_name)
