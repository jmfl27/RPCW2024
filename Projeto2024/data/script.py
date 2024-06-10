# Nome dos ficheiros de entrada e saída
input_file = 'script.txt'
output_file = 'subclasses.txt'

# Função para criar subclasses a partir de tipos de documentos distintos
def criar_subclasses(input_file, output_file):
    try:
        # Ler os tipos distintos de documentos do ficheiro de entrada
        with open(input_file, 'r', encoding='utf-8') as file:
            doc_classs = file.readlines()
        
        # Limpar os tipos de documentos para remover espaços em branco e quebras de linha
        doc_classs = [doc_class.strip() for doc_class in doc_classs if doc_class.strip()]

        # Criar e escrever no ficheiro de saída no formato desejado
        with open(output_file, 'w', encoding='utf-8') as file:
            for doc_class in doc_classs:
                # Substituir espaços por underscores e remover caracteres especiais para criar URIs válidas
                uri_safe_doc_class = doc_class.replace(' ', '_')
                file.write(f'###  http://rpcw.di.uminho.pt/2024/diario-republica/{uri_safe_doc_class}\n')
                file.write(f':{uri_safe_doc_class} rdf:type owl:Class ;\n')
                file.write(f'     rdfs:subClassOf :Diploma .\n\n')
        
        print(f'Ficheiro {output_file} criado com sucesso.')
    
    except FileNotFoundError:
        print(f'Erro: O ficheiro {input_file} não foi encontrado.')

# Chamar a função
criar_subclasses(input_file, output_file)
