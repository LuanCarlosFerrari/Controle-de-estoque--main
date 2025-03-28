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
                    mesa = linha["mesa"]
                    telefone = linha.get("telefone", "")
                    status = linha["status"]
                    self.clientes[codigo] = {"nome": nome, "mesa": mesa, "telefone": telefone, "status": status}
                    self.proximo_codigo = max(self.proximo_codigo, codigo + 1)  # Atualiza o próximo código
        except FileNotFoundError:
            pass

    def salvar_clientes(self):
        with open(self.arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["codigo", "nome", "mesa", "telefone", "status"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for codigo, dados in self.clientes.items():
                writer.writerow({"codigo": codigo, "nome": dados["nome"], "mesa": dados["mesa"], "telefone": dados["telefone"], "status": dados["status"]})

    def adicionar_cliente(self, nome, mesa, telefone=""):
        codigo = self.proximo_codigo
        self.clientes[codigo] = {"nome": nome, "mesa": mesa, "telefone": telefone, "status": "ativo"}
        self.proximo_codigo += 1
        return codigo

    def remover_cliente(self, codigo):
        if codigo in self.clientes:
            self.clientes[codigo]["status"] = "excluido"

    def atualizar_cliente(self, codigo, nome=None, mesa=None, telefone=None):
        if codigo in self.clientes and self.clientes[codigo]["status"] == "ativo":
            if nome:
                self.clientes[codigo]["nome"] = nome
            if mesa:
                self.clientes[codigo]["mesa"] = mesa
            if telefone:
                self.clientes[codigo]["telefone"] = telefone

    def reativar_cliente(self, codigo):
        if codigo in self.clientes and self.clientes[codigo]["status"] == "excluido":
            self.clientes[codigo]["status"] = "ativo"

class EstoqueUI:
    def __init__(self):
        self.estoque = Estoque()
        self.clientes = Clientes()

        # Configuração da janela principal
        self.window = ctk.CTk()
        self.window.title("Sistema de Controle")
        self.window.geometry("1000x600")  # Ajustado para apresentar todas as abas adequadamente

        # Configuração do sistema de abas
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Adicionar abas
        self.produtos_tab = self.tabview.add("Produtos")
        self.clientes_tab = self.tabview.add("Clientes/Mesa")
        self.consumo_tab = self.tabview.add("Consumo")
        self.caixa_tab = self.tabview.add("Caixa")

        # Configurar cada aba
        self.setup_produtos_tab()
        self.setup_clientes_tab()
        self.setup_consumo_tab()
        self.setup_caixa_tab()

    def setup_produtos_tab(self):
        # Reutilizar a lógica existente para a aba de produtos
        input_frame = ctk.CTkFrame(self.produtos_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

        input_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        ctk.CTkLabel(input_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.nome_entry = ctk.CTkEntry(input_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Preço:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.preco_entry = ctk.CTkEntry(input_frame)
        self.preco_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.quantidade_entry = ctk.CTkEntry(input_frame)
        self.quantidade_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.produtos_tab)
        button_frame.pack(padx=20, pady=10)

        ctk.CTkButton(button_frame, text="Adicionar", command=self.adicionar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Remover", command=self.remover_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Reativar", command=self.reativar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Exibir Estoque", command=self.exibir_estoque).pack(side="left", padx=5)

        self.display_area = ctk.CTkTextbox(self.produtos_tab, height=300)
        self.display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def setup_clientes_tab(self):
        # Configuração inicial para a aba de clientes/mesa
        input_frame = ctk.CTkFrame(self.clientes_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

        # Centralizar e organizar as caixas de entrada
        input_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        ctk.CTkLabel(input_frame, text="Nome do Cliente/Mesa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cliente_nome_entry = ctk.CTkEntry(input_frame)
        self.cliente_nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Documento:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.documento_entry = ctk.CTkEntry(input_frame)
        self.documento_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Telefone:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.telefone_entry = ctk.CTkEntry(input_frame)
        self.telefone_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.clientes_tab)
        button_frame.pack(padx=20, pady=10)

        ctk.CTkButton(button_frame, text="Adicionar", command=self.adicionar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Remover", command=self.remover_cliente).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Reativar", command=self.reativar_cliente).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Exibir", command=self.exibir_clientes).pack(side="left", padx=5)

        self.clientes_display_area = ctk.CTkTextbox(self.clientes_tab, height=300)
        self.clientes_display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def setup_estoque_tab(self):
        # Removida a configuração da aba de estoque
        pass

    def setup_caixa_tab(self):
        # Configuração inicial para a aba de caixa
        ctk.CTkLabel(self.caixa_tab, text="Gerenciamento de Caixa", font=("Arial", 16)).pack(pady=10)
        self.caixa_display_area = ctk.CTkTextbox(self.caixa_tab, height=400)
        self.caixa_display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def setup_consumo_tab(self):
        # Configuração inicial para a aba de consumo
        input_frame = ctk.CTkFrame(self.consumo_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

        # Centralizar e organizar as caixas de entrada
        input_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        ctk.CTkLabel(input_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cliente_combobox = ctk.CTkComboBox(input_frame, values=list(self.clientes.clientes.values()))
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Produto:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.produto_combobox = ctk.CTkComboBox(input_frame, values=list(self.estoque.produtos.values()))
        self.produto_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.quantidade_entry = ctk.CTkEntry(input_frame)
        self.quantidade_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.consumo_tab)
        button_frame.pack(padx=20, pady=10)

        ctk.CTkButton(button_frame, text="Registrar Consumo", command=self.registrar_consumo).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Remover Consumo", command=self.remover_consumo).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Exibir Consumos", command=self.exibir_consumos).pack(side="left", padx=5)

        self.consumo_display_area = ctk.CTkTextbox(self.consumo_tab, height=300)
        self.consumo_display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def registrar_consumo(self):
        cliente = self.cliente_combobox.get()
        produto = self.produto_combobox.get()
        quantidade = self.quantidade_entry.get()

        if not (cliente and produto and quantidade):
            self.consumo_display_area.insert("end", "Todos os campos devem ser preenchidos para registrar um consumo.\n")
            return

        try:
            quantidade = int(quantidade)
            produto_dados = next((p for p in self.estoque.produtos.values() if p["nome"] == produto), None)
            cliente_dados = next((c for c in self.clientes.clientes.values() if c["nome"] == cliente), None)

            if produto_dados and cliente_dados:
                total = produto_dados["preco"] * quantidade
                self.consumo_display_area.insert("end", f"Consumo registrado: Cliente {cliente}, Produto {produto}, Quantidade {quantidade}, Total R${total:.2f}\n")
            else:
                self.consumo_display_area.insert("end", "Erro ao registrar consumo: Cliente ou Produto não encontrado.\n")
        except ValueError:
            self.consumo_display_area.insert("end", "Erro: Quantidade deve ser um número inteiro.\n")

    def remover_consumo(self):
        self.consumo_display_area.insert("end", "Funcionalidade de remoção de consumo ainda não implementada.\n")

    def exibir_consumos(self):
        self.consumo_display_area.delete("1.0", "end")
        self.consumo_display_area.insert("end", "Lista de consumos ainda não implementada.\n")

    def adicionar_produto(self):
        nome = self.nome_entry.get().strip()
        preco = self.preco_entry.get().strip()
        quantidade = self.quantidade_entry.get().strip()

        # Verificar se todos os campos estão preenchidos
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

    def adicionar_cliente(self):
        nome = self.cliente_nome_entry.get()
        documento = self.documento_entry.get()
        telefone = self.telefone_entry.get()

        if not (nome and documento):
            self.clientes_display_area.insert("end", "Os campos Nome e Documento são obrigatórios para adicionar um cliente/mesa.\n")
            return

        codigo = self.clientes.adicionar_cliente(nome, documento, telefone)
        self.clientes_display_area.insert("end", f"Cliente/Mesa {nome} adicionado com sucesso! Código: {codigo}\n")

    def remover_cliente(self):
        codigo = self.cliente_nome_entry.get()

        if not codigo:
            self.clientes_display_area.insert("end", "O campo Código deve ser preenchido para remover um cliente.\n")
            return

        try:
            codigo = int(codigo)
            self.clientes.remover_cliente(codigo)
            self.clientes_display_area.insert("end", f"Cliente com código {codigo} marcado como excluído.\n")
        except ValueError:
            self.clientes_display_area.insert("end", "Erro: Código deve ser um número inteiro.\n")

    def atualizar_cliente(self):
        codigo = self.cliente_nome_entry.get()
        nome = self.cliente_nome_entry.get() or None
        documento = self.documento_entry.get() or None
        telefone = self.telefone_entry.get() or None

        if not codigo:
            self.clientes_display_area.insert("end", "O campo Código deve ser preenchido para atualizar um cliente/mesa.\n")
            return

        try:
            codigo = int(codigo)
            self.clientes.atualizar_cliente(codigo, nome, documento, telefone)
            self.clientes_display_area.insert("end", f"Cliente/Mesa com código {codigo} atualizado com sucesso!\n")
        except ValueError:
            self.clientes_display_area.insert("end", "Erro: Código deve ser um número inteiro.\n")

    def reativar_cliente(self):
        codigo = self.cliente_nome_entry.get()

        if not codigo:
            self.clientes_display_area.insert("end", "O campo Código deve ser preenchido para reativar um cliente.\n")
            return

        try:
            codigo = int(codigo)
            self.clientes.reativar_cliente(codigo)
            self.clientes_display_area.insert("end", f"Cliente com código {codigo} reativado com sucesso!\n")
        except ValueError:
            self.clientes_display_area.insert("end", "Erro: Código deve ser um número inteiro.\n")

    def exibir_clientes(self):
        self.clientes_display_area.delete("1.0", "end")
        if not self.clientes.clientes:
            self.clientes_display_area.insert("end", "Nenhum cliente/mesa cadastrado.\n")
        else:
            for codigo, dados in self.clientes.clientes.items():
                info = f"Código: {codigo} | Nome: {dados['nome']} | Documento: {dados['mesa']} | Telefone: {dados.get('telefone', 'N/A')} | Status: {dados['status']}\n"
                self.clientes_display_area.insert("end", info)

    def salvar_e_sair(self):
        self.estoque.salvar_estoque()
        self.clientes.salvar_clientes()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EstoqueUI()
    app.run()