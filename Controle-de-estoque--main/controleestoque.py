import csv
import os
import customtkinter as ctk

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

class EstoqueApp:
    def __init__(self, root, estoque):
        self.root = root
        self.estoque = estoque
        self.root.title("Controle de Estoque")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Frame principal
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20)

        # Botões principais lado a lado
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10)

        ctk.CTkButton(self.button_frame, text="Adicionar Produto", command=self.adicionar_produto).pack(side="left", padx=5)
        ctk.CTkButton(self.button_frame, text="Remover Produto", command=self.remover_produto).pack(side="left", padx=5)
        ctk.CTkButton(self.button_frame, text="Atualizar Produto", command=self.atualizar_produto).pack(side="left", padx=5)
        ctk.CTkButton(self.button_frame, text="Exibir Estoque", command=self.exibir_estoque).pack(side="left", padx=5)
        ctk.CTkButton(self.button_frame, text="Salvar e Sair", command=self.salvar_e_sair).pack(side="left", padx=5)

        # Área de entrada de dados
        self.input_frame = ctk.CTkFrame(self.frame)
        self.input_frame.pack(pady=10)

        ctk.CTkLabel(self.input_frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.codigo_entry = ctk.CTkEntry(self.input_frame)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.input_frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
        self.nome_entry = ctk.CTkEntry(self.input_frame)
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.input_frame, text="Preço:").grid(row=2, column=0, padx=5, pady=5)
        self.preco_entry = ctk.CTkEntry(self.input_frame)
        self.preco_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.input_frame, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5)
        self.quantidade_entry = ctk.CTkEntry(self.input_frame)
        self.quantidade_entry.grid(row=3, column=1, padx=5, pady=5)

        # Área de exibição
        self.display_area = ctk.CTkTextbox(self.frame, width=600, height=300)
        self.display_area.pack(pady=10)

    def adicionar_produto(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        quantidade = self.quantidade_entry.get()

        if not (codigo and nome and preco and quantidade):
            self.display_area.insert("end", "Todos os campos devem ser preenchidos para adicionar um produto.\n")
            return

        try:
            preco = float(preco)
            quantidade = int(quantidade)
            self.estoque.adicionar_produto(codigo, nome, preco, quantidade)
            self.display_area.insert("end", f"Produto {nome} adicionado com sucesso!\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Preço deve ser um número e Quantidade deve ser um inteiro.\n")

    def remover_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para remover um produto.\n")
            return

        self.estoque.remover_produto(codigo)
        self.display_area.insert("end", f"Produto com código {codigo} removido com sucesso!\n")

    def atualizar_produto(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get() or None
        preco = self.preco_entry.get()
        quantidade = self.quantidade_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para atualizar um produto.\n")
            return

        try:
            preco = float(preco) if preco else None
            quantidade = int(quantidade) if quantidade else None
            self.estoque.atualizar_produto(codigo, nome, preco, quantidade)
            self.display_area.insert("end", f"Produto com código {codigo} atualizado com sucesso!\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Preço deve ser um número e Quantidade deve ser um inteiro.\n")

    def exibir_estoque(self):
        self.display_area.delete("1.0", "end")
        if not self.estoque.produtos:
            self.display_area.insert("end", "Estoque vazio.\n")
        else:
            for produto in self.estoque.produtos.values():
                info = f"Código: {produto.codigo} | Nome: {produto.nome} | Preço: R${produto.preco:.2f} | Quantidade: {produto.quantidade}\n"
                self.display_area.insert("end", info)

    def salvar_e_sair(self):
        self.estoque.salvar_estoque()
        self.root.destroy()

if __name__ == "__main__":
    estoque = Estoque()
    root = ctk.CTk()
    app = EstoqueApp(root, estoque)
    root.mainloop()