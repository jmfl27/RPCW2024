import json

# Nome do ficheiro
file_name = 'new_data.json'

# Função para ler e mostrar os primeiros quatro elementos do ficheiro JSON
def mostrar_primeiros_quatro_elementos(file_name):
    try:
        # Abrir e carregar o ficheiro JSON
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Verificar se o ficheiro contém uma lista
        if isinstance(data, list):
            # Mostrar os primeiros quatro elementos
            primeiros_quatro = data[:4]
            for i, elemento in enumerate(primeiros_quatro, 1):
                print(f'Elemento {i}: {json.dumps(elemento, indent=4)}')
        else:
            print('O ficheiro JSON não contém uma lista.')
    
    except FileNotFoundError:
        print(f'Erro: O ficheiro {file_name} não foi encontrado.')
    except json.JSONDecodeError:
        print('Erro: O ficheiro não está num formato JSON válido.')

# Chamar a função
mostrar_primeiros_quatro_elementos(file_name)
