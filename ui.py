import customtkinter as ctk
import csv

class Estoque:
    def __init__(self, arquivo_csv="estoque.csv"):
        self.produtos = {}
        self.arquivo_csv = arquivo_csv
        self.proximo_codigo = 1  # Inicializa o próximo código como 1
        self.carregar_estoque()

    def carregar_estoque(self):
        try:
            with open(self.arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    codigo = int(linha["codigo"])
                    nome = linha["nome"]
                    preco = float(linha["preco"])
                    quantidade = int(linha["quantidade"])
                    status = linha["status"]
                    self.produtos[codigo] = {"nome": nome, "preco": preco, "quantidade": quantidade, "status": status}
                    self.proximo_codigo = max(self.proximo_codigo, codigo + 1)  # Atualiza o próximo código
        except FileNotFoundError:
            pass

    def salvar_estoque(self):
        with open(self.arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["codigo", "nome", "preco", "quantidade", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for codigo, dados in self.produtos.items():
                writer.writerow({"codigo": codigo, "nome": dados["nome"], "preco": dados["preco"], "quantidade": dados["quantidade"], "status": dados["status"]})

    def adicionar_produto(self, nome, preco, quantidade):
        codigo = self.proximo_codigo
        self.produtos[codigo] = {"nome": nome, "preco": preco, "quantidade": quantidade, "status": "ativo"}
        self.proximo_codigo += 1
        return codigo

    def remover_produto(self, codigo):
        if codigo in self.produtos:
            self.produtos[codigo]["status"] = "excluido"

    def atualizar_produto(self, codigo, nome=None, preco=None, quantidade=None):
        if codigo in self.produtos and self.produtos[codigo]["status"] == "ativo":
            if nome:
                self.produtos[codigo]["nome"] = nome
            if preco:
                self.produtos[codigo]["preco"] = preco
            if quantidade is not None:
                self.produtos[codigo]["quantidade"] = quantidade

    def reativar_produto(self, codigo):
        if codigo in self.produtos and self.produtos[codigo]["status"] == "excluido":
            self.produtos[codigo]["status"] = "ativo"

class EstoqueUI:
    def __init__(self):
        self.estoque = Estoque()

        # Configuração da janela principal
        self.window = ctk.CTk()
        self.window.title("Controle de Estoque")
        self.window.geometry("1000x400")  # Ajustado para apresentar todos os botões e campos adequadamente

        # Configuração do layout
        self.setup_ui()

    def setup_ui(self):
        # Frame de entrada de dados
        input_frame = ctk.CTkFrame(self.window)
        input_frame.pack(padx=20, pady=10, fill="x")

        # Centralizar as caixas de entrada
        input_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        ctk.CTkLabel(input_frame, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.codigo_entry = ctk.CTkEntry(input_frame)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.nome_entry = ctk.CTkEntry(input_frame)
        self.nome_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Preço:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.preco_entry = ctk.CTkEntry(input_frame)
        self.preco_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.quantidade_entry = ctk.CTkEntry(input_frame)
        self.quantidade_entry.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Botões de ação
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(padx=20, pady=10)

        ctk.CTkButton(button_frame, text="Adicionar", command=self.adicionar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Remover", command=self.remover_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Reativar", command=self.reativar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Exibir Estoque", command=self.exibir_estoque).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Salvar e Sair", command=self.salvar_e_sair).pack(side="left", padx=5)

        # Área de exibição
        self.display_area = ctk.CTkTextbox(self.window, height=300)
        self.display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def adicionar_produto(self):
        nome = self.nome_entry.get()
        preco = self.preco_entry.get()
        quantidade = self.quantidade_entry.get()

        if not (nome and preco and quantidade):
            self.display_area.insert("end", "Todos os campos devem ser preenchidos para adicionar um produto.\n")
            return

        try:
            preco = float(preco)
            quantidade = int(quantidade)
            codigo = self.estoque.adicionar_produto(nome, preco, quantidade)
            self.display_area.insert("end", f"Produto {nome} adicionado com sucesso! Código: {codigo}\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Preço deve ser um número e Quantidade deve ser um inteiro.\n")

    def remover_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para remover um produto.\n")
            return

        try:
            codigo = int(codigo)
            self.estoque.remover_produto(codigo)
            self.display_area.insert("end", f"Produto com código {codigo} marcado como excluído.\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Código deve ser um número inteiro.\n")

    def atualizar_produto(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get() or None
        preco = self.preco_entry.get()
        quantidade = self.quantidade_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para atualizar um produto.\n")
            return

        try:
            codigo = int(codigo)
            preco = float(preco) if preco else None
            quantidade = int(quantidade) if quantidade else None
            self.estoque.atualizar_produto(codigo, nome, preco, quantidade)
            self.display_area.insert("end", f"Produto com código {codigo} atualizado com sucesso!\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Código deve ser um número inteiro, Preço deve ser um número e Quantidade deve ser um inteiro.\n")

    def reativar_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para reativar um produto.\n")
            return

        try:
            codigo = int(codigo)
            self.estoque.reativar_produto(codigo)
            self.display_area.insert("end", f"Produto com código {codigo} reativado com sucesso!\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Código deve ser um número inteiro.\n")

    def exibir_estoque(self):
        self.display_area.delete("1.0", "end")
        if not self.estoque.produtos:
            self.display_area.insert("end", "Estoque vazio.\n")
        else:
            for codigo, dados in self.estoque.produtos.items():
                info = f"Código: {codigo} | Nome: {dados['nome']} | Preço: R${dados['preco']:.2f} | Quantidade: {dados['quantidade']} | Status: {dados['status']}\n"
                self.display_area.insert("end", info)

    def salvar_e_sair(self):
        self.estoque.salvar_estoque()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EstoqueUI()
    app.run()