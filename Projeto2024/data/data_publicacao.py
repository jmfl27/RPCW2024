import json

# Nome do ficheiro
file_name = 'new_data.json'


# Função para obter todos os "dates" distintos
def obter_dates_distintos(file_name):
    try:
        # Abrir e carregar o ficheiro JSON
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Verificar se o ficheiro contém uma lista
        if isinstance(data, list):
            # Criar um conjunto para armazenar "dates" distintos
            dates_distintos = set()
            
            # Iterar sobre os elementos da lista e adicionar "dates" ao conjunto

            for item in data:
                if 'claint' in item:
                    if item['claint'] == 179670:

                        print(item)
            
            # Mostrar os "dates" distintos
            #print('Doc Types Distintos:')
            #for date in dates_distintos:
            #   print(date)
            
        else:
            print('O ficheiro JSON não contém uma lista.')

    
    except FileNotFoundError:
        print(f'Erro: O ficheiro {file_name} não foi encontrado.')
    except json.JSONDecodeError:
        print('Erro: O ficheiro não está num formato JSON válido.')

# Chamar a função
obter_dates_distintos(file_name)
