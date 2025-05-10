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
