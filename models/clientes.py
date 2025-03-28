import csv

class Clientes:
    def __init__(self, arquivo_csv="clientes.csv"):
        self.clientes = {}
        self.arquivo_csv = arquivo_csv
        self.proximo_codigo = 1  # Inicializa o próximo código como 1
        self.carregar_clientes()

    def carregar_clientes(self):
        try:
            with open(self.arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    codigo = int(linha["codigo"])
                    nome = linha["nome"]
                    telefone = linha["telefone"]
                    status = linha["status"]
                    self.clientes[codigo] = {"nome": nome, "telefone": telefone, "status": status}
                    self.proximo_codigo = max(self.proximo_codigo, codigo + 1)  # Atualiza o próximo código
        except FileNotFoundError:
            pass

    def salvar_clientes(self):
        with open(self.arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["codigo", "nome", "telefone", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for codigo, dados in self.clientes.items():
                writer.writerow({"codigo": codigo, "nome": dados["nome"], "telefone": dados["telefone"], "status": dados["status"]})

    def adicionar_cliente(self, nome, telefone):
        codigo = self.proximo_codigo
        self.clientes[codigo] = {"nome": nome, "telefone": telefone, "status": "ativo"}
        self.proximo_codigo += 1
        return codigo

    def remover_cliente(self, codigo):
        if codigo in self.clientes:
            self.clientes[codigo]["status"] = "excluido"

    def atualizar_cliente(self, codigo, nome=None, telefone=None):
        if codigo in self.clientes and self.clientes[codigo]["status"] == "ativo":
            if nome:
                self.clientes[codigo]["nome"] = nome
            if telefone:
                self.clientes[codigo]["telefone"] = telefone

    def reativar_cliente(self, codigo):
        if codigo in self.clientes and self.clientes[codigo]["status"] == "excluido":
            self.clientes[codigo]["status"] = "ativo"