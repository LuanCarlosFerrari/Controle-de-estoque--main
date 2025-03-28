import csv
import os

vermelho = '\033[31m'
verde = '\033[32m'
azul = '\033[34m'
ciano = '\033[36m'
magenta = '\033[35m'
amarelo = '\033[33m'
preto = '\033[30m'
branco = '\033[37m'
reset = "033[0m"
reverso = '\033[2m'

class Produto:
    def __init__(self, codigo, nome, preco, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

class Estoque:
    def __init__(self, arquivo_csv="estoque.csv"):
        self.produtos = {}
        self.arquivo_csv = arquivo_csv
        self.carregar_estoque()

    def carregar_estoque(self):
        try:
            with open(self.arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    codigo = linha["codigo"]
                    nome = linha["nome"]
                    preco = float(linha["preco"])
                    quantidade = int(linha["quantidade"])
                    self.produtos[codigo] = Produto(codigo, nome, preco, quantidade)
            print("Estoque carregado com sucesso!")
            atualizar_readme("Estoque carregado com sucesso!")
        except FileNotFoundError:
            print("Arquivo de estoque não encontrado. Iniciando estoque vazio.")
            atualizar_readme("Estoque iniciado vazio - arquivo não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar estoque: {e}")
            atualizar_readme(f"Erro ao carregar estoque: {e}")

    def salvar_estoque(self):
        try:
            with open(self.arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["codigo", "nome", "preco", "quantidade"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for produto in self.produtos.values():
                    writer.writerow({
                        "codigo": produto.codigo,
                        "nome": produto.nome,
                        "preco": produto.preco,
                        "quantidade": produto.quantidade
                    })
            print("Estoque salvo com sucesso!")
            atualizar_readme("Estoque salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar estoque: {e}")
            atualizar_readme(f"Erro ao salvar estoque: {e}")

    def adicionar_produto(self, codigo, nome, preco, quantidade):
        if codigo in self.produtos:
            print(f"Produto com código {codigo} já existe!")
            atualizar_readme(f"Tentativa de adicionar produto duplicado: código {codigo}")
        else:
            novo_produto = Produto(codigo, nome, preco, quantidade)
            self.produtos[codigo] = novo_produto
            print(f"Produto {nome} adicionado com sucesso!")
            atualizar_readme(f"Produto adicionado: {nome} (código: {codigo}, preço: R${preco:.2f}, quantidade: {quantidade})")

    def remover_produto(self, codigo):
        if codigo in self.produtos:
            removido = self.produtos.pop(codigo)
            print(f"Produto {removido.nome} removido com sucesso!")
            atualizar_readme(f"Produto removido: {removido.nome} (código: {codigo})")
        else:
            print(f"Produto com código {codigo} não encontrado!")
            atualizar_readme(f"Tentativa de remover produto inexistente: código {codigo}")

    def atualizar_produto(self, codigo, nome=None, preco=None, quantidade=None):
        if codigo in self.produtos:
            produto = self.produtos[codigo]
            produto_antigo = f"{produto.nome} (preço: R${produto.preco:.2f}, quantidade: {produto.quantidade})"
            
            if nome:
                produto.nome = nome
            if preco:
                produto.preco = preco
            if quantidade is not None:
                produto.quantidade = quantidade
                
            print(f"Produto {codigo} atualizado com sucesso!")
            produto_novo = f"{produto.nome} (preço: R${produto.preco:.2f}, quantidade: {produto.quantidade})"
            atualizar_readme(f"Produto atualizado: código {codigo}\nDe: {produto_antigo}\nPara: {produto_novo}")
        else:
            print(f"Produto com código {codigo} não encontrado!")
            atualizar_readme(f"Tentativa de atualizar produto inexistente: código {codigo}")

    def exibir_estoque(self):
        if not self.produtos:
            print("Estoque vazio.")
            atualizar_readme("Consulta de estoque: estoque vazio.")
        else:
            print("Consulta de estoque realizada:")
            produtos_lista = []
            for produto in self.produtos.values():
                info = f"Código: {produto.codigo} | Nome: {produto.nome} | Preço: R${produto.preco:.2f} | Quantidade: {produto.quantidade}"
                print(info)
                produtos_lista.append(info)
            atualizar_readme("Consulta de estoque realizada. Produtos listados: " + str(len(produtos_lista)))

def atualizar_readme(mensagem):
    """Atualiza o arquivo README.md com as alterações do sistema"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    
    try:
        # Ler o conteúdo atual do README
        with open(readme_path, 'r', encoding='utf-8') as file:
            conteudo = file.read()
        
        # Verificar se já existe uma seção de log
        if "## Histórico de Alterações" not in conteudo:
            # Adicionar seção de log se não existir
            conteudo += "\n\n## Histórico de Alterações\n"
        
        # Adicionar nova entrada no log
        from datetime import datetime
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Encontrar a posição para inserir a nova entrada
        pos = conteudo.find("## Histórico de Alterações") + len("## Histórico de Alterações")
        nova_entrada = f"\n\n### {timestamp}\n- {mensagem}"
        
        # Inserir a nova entrada após o cabeçalho da seção
        conteudo_atualizado = conteudo[:pos] + nova_entrada + conteudo[pos:]
        
        # Salvar o arquivo atualizado
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(conteudo_atualizado)
    
    except Exception as e:
        print(f"Erro ao atualizar README: {e}")

def menu():
    print(f"\n {verde} -----Menu de Controle de Estoque-----")
    print("[1] Adicionar Produto")
    print("[2] Remover Produto")
    print("[3] Atualizar Produto")
    print("[4] Exibir Estoque")
    print("[5] Sair e Salvar")
    print("[6] SOBRE")
    print("  ")

def main():
    estoque = Estoque()
    
    while True:
        menu()
        opcao = input(f"{vermelho}SELECT>> \033[2m ")
        print(f" {branco} ")
        
        if opcao == '1':
            codigo = input("Informe o código do produto: ")
            nome = input("Informe o nome do produto: ")
            preco = float(input("Informe o preço do produto: "))
            quantidade = int(input("Informe a quantidade do produto: "))
            estoque.adicionar_produto(codigo, nome, preco, quantidade)

        elif opcao == '2':
            codigo = input("Informe o código do produto a ser removido: ")
            estoque.remover_produto(codigo)

        elif opcao == '3':
            codigo = input("Informe o código do produto a ser atualizado: ")
            nome = input("Novo nome (pressione Enter para manter o atual): ")
            preco = input("Novo preço (pressione Enter para manter o atual): ")
            quantidade = input("Nova quantidade (pressione Enter para manter a atual): ")
            
            nome = nome if nome else None
            preco = float(preco) if preco else None
            quantidade = int(quantidade) if quantidade else None
            
            estoque.atualizar_produto(codigo, nome, preco, quantidade)

        elif opcao == '4':
            estoque.exibir_estoque()

        elif opcao == '5':
            estoque.salvar_estoque()
            print("Saindo e salvando estoque...")
            atualizar_readme("Sessão encerrada - estoque salvo.")
            break
            
        elif opcao =="6":
            info = """
            --- Codado por wan ---
            --- Python 3           ---
            --- Pydroid        ---
            
            
            """
            print(info)
            atualizar_readme("Informações sobre o sistema visualizadas.")

        else:
            print("Opção inválida, tente novamente!")
            atualizar_readme("Tentativa de opção inválida no menu.")

if __name__ == "__main__":
    main()