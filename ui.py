import customtkinter as ctk
from models.estoque import Estoque
from models.clientes import Clientes
import csv
from datetime import datetime

class EstoqueUI:
    def __init__(self):
        self.estoque = Estoque()
        self.clientes = Clientes()
        self.consumos_registrados = [] 
        self.carregar_consumos() # Carregar consumos ao iniciar

        # Configuração da janela principal
        self.window = ctk.CTk()
        self.window.title("Sistema de Controle")
        self.window.geometry("1000x600")  # Ajustado para apresentar todas as abas adequadamente
        self.window.protocol("WM_DELETE_WINDOW", self.salvar_e_sair)  # Chamar salvar_e_sair ao fechar

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
        self.update_consumo_comboboxes() # Initial population for Consumo tab
        self.update_caixa_cliente_combobox() # Initial population for Caixa tab

    def update_caixa_cliente_combobox(self):
        clientes_com_contas_abertas = sorted(list(set(c["cliente"] for c in self.consumos_registrados if c["status"] == "aberto")))
        if clientes_com_contas_abertas:
            self.caixa_cliente_combobox.configure(values=clientes_com_contas_abertas)
            self.caixa_cliente_combobox.set(clientes_com_contas_abertas[0])
            self.display_conta_cliente() # Display items for the first client
        else:
            self.caixa_cliente_combobox.configure(values=["Nenhum cliente com conta aberta"])
            self.caixa_cliente_combobox.set("Nenhum cliente com conta aberta")
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", "Nenhum consumo em aberto para exibir.\n")

    def update_consumo_comboboxes(self):
        active_client_names = [c["nome"] for c in self.clientes.clientes.values() if c["status"] == "ativo"]
        if active_client_names:
            self.cliente_combobox.configure(values=active_client_names)
            self.cliente_combobox.set(active_client_names[0])
        else:
            self.cliente_combobox.configure(values=["Nenhum cliente ativo"])
            self.cliente_combobox.set("Nenhum cliente ativo")

        active_product_names = [p["nome"] for p in self.estoque.produtos.values() if p["status"] == "ativo"]
        if active_product_names:
            self.produto_combobox.configure(values=active_product_names)
            self.produto_combobox.set(active_product_names[0])
        else:
            self.produto_combobox.configure(values=["Nenhum produto ativo"])
            self.produto_combobox.set("Nenhum produto ativo")

    def setup_produtos_tab(self):
        # Reutilizar a lógica existente para a aba de produtos
        input_frame = ctk.CTkFrame(self.produtos_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

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
        self.produto_quantidade_entry = ctk.CTkEntry(input_frame)
        self.produto_quantidade_entry.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

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
        # Frame para seleção de cliente e botão
        control_frame = ctk.CTkFrame(self.caixa_tab)
        control_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(control_frame, text="Cliente com Conta Aberta:").pack(side="left", padx=(0, 5))
        self.caixa_cliente_combobox = ctk.CTkComboBox(control_frame, values=["Nenhum cliente com conta aberta"], command=self.display_conta_cliente, width=200)
        self.caixa_cliente_combobox.pack(side="left", padx=5) # Removed expand=True, fill="x" to give space

        ctk.CTkLabel(control_frame, text="Valor a Pagar: R$").pack(side="left", padx=(10, 0))
        self.caixa_valor_pago_entry = ctk.CTkEntry(control_frame, width=80) # Reduced width
        self.caixa_valor_pago_entry.pack(side="left", padx=5)
        
        self.realizar_pagamento_button = ctk.CTkButton(control_frame, text="Realizar Pagamento", command=self.realizar_pagamento_caixa)
        self.realizar_pagamento_button.pack(side="left", padx=5)

        # Área de exibição para os consumos do cliente
        self.caixa_display_area = ctk.CTkTextbox(self.caixa_tab, height=350) 
        self.caixa_display_area.pack(padx=20, pady=10, fill="both", expand=True)

    def display_conta_cliente(self, client_name_to_display=None):
        _selected_client_from_arg = client_name_to_display
        
        if _selected_client_from_arg is None:
            client_name_from_combobox = self.caixa_cliente_combobox.get()
            if not client_name_from_combobox: # Should not happen if combobox has a default
                self.caixa_display_area.delete("1.0", "end")
                self.caixa_display_area.insert("end", "Nenhum cliente selecionado na ComboBox.\n")
                return
            selected_client = client_name_from_combobox.strip()
        else:
            selected_client = _selected_client_from_arg.strip()

        self.caixa_display_area.delete("1.0", "end")

        if selected_client == "Nenhum cliente com conta aberta" or not selected_client: # Check stripped name
            self.caixa_display_area.insert("end", "Nenhum cliente selecionado ou sem contas abertas.\n")
            return

        consumos_cliente_aberto = [
            c for c in self.consumos_registrados 
            if c["cliente"] == selected_client and c["status"] == "aberto"
        ]

        if not consumos_cliente_aberto:
            self.caixa_display_area.insert("end", f"Nenhuma conta aberta para o cliente: {selected_client}\n")
            return

        self.caixa_display_area.insert("end", f"--- Conta Aberta: {selected_client} ---\n")
        total_conta = 0
        for consumo in consumos_cliente_aberto:
            info = (f"ID: {consumo['id']}, Produto: {consumo['produto']}, Qtd: {consumo['quantidade']}, "
                    f"Preço Unit.: R${consumo['preco_unitario']:.2f}, Total Item: R${consumo['total']:.2f}\n"
                    f"  Data: {consumo['timestamp']}\n")
            self.caixa_display_area.insert("end", info)
            total_conta += consumo['total']
        
        self.caixa_display_area.insert("end", "-----------------------------------\n")
        self.caixa_display_area.insert("end", "-----------------------------------\n")
        self.caixa_display_area.insert("end", f"TOTAL DA CONTA ABERTA: R${total_conta:.2f}\n")
        self.caixa_display_area.insert("end", "-----------------------------------\n")
        return total_conta # Return the calculated total

    def realizar_pagamento_caixa(self):
        selected_client_raw = self.caixa_cliente_combobox.get()
        if not selected_client_raw: # Handle empty selection if possible
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", "ERRO: Nenhum cliente selecionado.\n")
            return
        selected_client = selected_client_raw.strip()
        
        valor_pago_str = self.caixa_valor_pago_entry.get()
        
        self.caixa_display_area.delete("1.0", "end") # Clear display area at the beginning

        if selected_client == "Nenhum cliente com conta aberta": # Check after strip
            self.caixa_display_area.insert("end", "ERRO: Nenhum cliente selecionado.\n")
            return

        if not valor_pago_str:
            self.caixa_display_area.insert("end", "ERRO: Informe o valor a pagar.\n")
            return

        try:
            valor_pago_informado = float(valor_pago_str.replace(',', '.'))
            if valor_pago_informado <= 0:
                self.caixa_display_area.insert("end", "\nERRO: Valor a pagar deve ser positivo.\n")
                return
        except ValueError:
            self.caixa_display_area.insert("end", "\nERRO: Valor a pagar inválido.\n")
            return

        # Coletar IDs e totais dos itens abertos para o cliente, mantendo a ordem original de self.consumos_registrados
        # para depois poder ordená-los por timestamp e ainda assim encontrar o índice correto em self.consumos_registrados
        
        itens_abertos_do_cliente_para_pagar = []
        for i, c in enumerate(self.consumos_registrados):
            if c["cliente"] == selected_client and c["status"] == "aberto":
                itens_abertos_do_cliente_para_pagar.append({
                    "id": c["id"],
                    "total": c["total"],
                    "timestamp": c["timestamp"],
                    "original_index": i # Guardar o índice original em self.consumos_registrados
                })

        # Ordenar os itens a pagar pelo timestamp
        itens_abertos_do_cliente_para_pagar.sort(key=lambda x: x["timestamp"])

        if not itens_abertos_do_cliente_para_pagar:
            self.caixa_display_area.insert("end", f"INFO: Nenhuma conta aberta para {selected_client}.\n")
            return
            
        valor_restante_do_pagamento = valor_pago_informado
        total_baixado_nesta_operacao = 0
        itens_pagos_nesta_operacao = 0
        ids_consumos_pagos_log = []

        for item_a_pagar in itens_abertos_do_cliente_para_pagar:
            if valor_restante_do_pagamento >= item_a_pagar['total']:
                # Modificar o item original em self.consumos_registrados usando o índice guardado
                original_idx = item_a_pagar['original_index']
                if self.consumos_registrados[original_idx]['id'] == item_a_pagar['id'] and self.consumos_registrados[original_idx]['status'] == 'aberto':
                    self.consumos_registrados[original_idx]['status'] = "pago"
                    ids_consumos_pagos_log.append(item_a_pagar['id'])
                    total_baixado_nesta_operacao += item_a_pagar['total']
                    valor_restante_do_pagamento -= item_a_pagar['total']
                    itens_pagos_nesta_operacao += 1
                else:
                    # Algo deu errado, o item no índice original não é o esperado ou já foi pago
                    # Isso não deveria acontecer com esta lógica, mas é uma salvaguarda
                    print(f"DEBUG: Discrepância ao tentar pagar item ID {item_a_pagar['id']}")
                    continue 
            else:
                # Não pode pagar este item integralmente
                break 
        
        # Mensagens sobre o pagamento
        if itens_pagos_nesta_operacao > 0:
            self.caixa_display_area.insert("end", f"--- Pagamento Processado para {selected_client} ---\n")
            self.caixa_display_area.insert("end", f"Valor Informado: R${valor_pago_informado:.2f}\n")
            self.caixa_display_area.insert("end", f"Total Baixado da Conta: R${total_baixado_nesta_operacao:.2f}\n")
            if valor_restante_do_pagamento > 0:
                 self.caixa_display_area.insert("end", f"Valor Restante do Pagamento (Troco/Não Utilizado): R${valor_restante_do_pagamento:.2f}\n")
            self.caixa_display_area.insert("end", f"Itens Pagos (IDs): {', '.join(map(str, ids_consumos_pagos_log))}\n")
            self.caixa_display_area.insert("end", "-----------------------------------\n\n")
        else:
            self.caixa_display_area.insert("end", f"Nenhum item integralmente pago para {selected_client} com o valor de R${valor_pago_informado:.2f}.\n")
            if valor_restante_do_pagamento == valor_pago_informado : 
                 self.caixa_display_area.insert("end", f"O valor R${valor_pago_informado:.2f} não foi suficiente para quitar nenhum item.\n")
        
        self.caixa_valor_pago_entry.delete(0, "end")

        # Atualizar a exibição da conta do cliente (mostrando itens restantes em aberto)
        # Esta chamada é crucial e deve usar o selected_client que teve o pagamento processado.
        # As mensagens de resumo do pagamento já foram inseridas antes desta chamada.
        # Esta chamada irá REESCREVER a caixa de texto com a lista atualizada de itens abertos.
        
        # Adicionar as mensagens de resumo do pagamento ANTES de mostrar a lista de itens restantes.
        # (Esta parte foi movida para ser ANTES da chamada a display_conta_cliente)
        # ... [mensagens de resumo do pagamento] ... (já estão lá)

        # Agora, display_conta_cliente é chamado para mostrar o estado atual da conta.
        self.display_conta_cliente(client_name_to_display=selected_client)
        
        # E então, atualizamos a combobox, que pode re-selecionar e chamar display_conta_cliente novamente.
        self.update_caixa_cliente_combobox() 
        self.update_consumo_comboboxes() # Atualiza comboboxes da aba Consumo também

    def setup_consumo_tab(self):
        # Configuração inicial para a aba de consumo
        input_frame = ctk.CTkFrame(self.consumo_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

        # Centralizar e organizar as caixas de entrada
        input_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        ctk.CTkLabel(input_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cliente_combobox = ctk.CTkComboBox(input_frame, values=["Nenhum cliente ativo"]) # Initial placeholder
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Produto:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.produto_combobox = ctk.CTkComboBox(input_frame, values=["Nenhum produto ativo"]) # Initial placeholder
        self.produto_combobox.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.consumo_quantidade_entry = ctk.CTkEntry(input_frame)
        self.consumo_quantidade_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

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
        quantidade = self.consumo_quantidade_entry.get()

        if not (cliente and produto and quantidade):
            self.consumo_display_area.insert("end", "Todos os campos devem ser preenchidos para registrar um consumo.\n")
            return

        try:
            quantidade = int(quantidade)
            produto_dados = next((p for p in self.estoque.produtos.values() if p["nome"] == produto), None)
            cliente_dados = next((c for c in self.clientes.clientes.values() if c["nome"] == cliente), None)

            if produto_dados and cliente_dados:
                # Encontrar o código do produto para atualizar o estoque
                produto_codigo = None
                for code, data in self.estoque.produtos.items():
                    if data["nome"] == produto and data["status"] == "ativo": # Certificar que é o produto ativo
                        produto_codigo = code
                        break
                
                if produto_codigo is None:
                    self.consumo_display_area.insert("end", "Erro: Produto ativo não encontrado para deduzir do estoque.\n")
                    return

                if self.estoque.produtos[produto_codigo]["quantidade"] >= quantidade:
                    total = produto_dados["preco"] * quantidade
                    
                    consumo_info = {
                        "id": len(self.consumos_registrados) + 1,
                        "cliente": cliente,
                        "produto": produto,
                        "quantidade": quantidade,
                        "preco_unitario": produto_dados["preco"],
                        "total": total,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "aberto"  # 'aberto' ou 'pago'
                    }
                    self.consumos_registrados.append(consumo_info)
                    
                    # Deduzir do estoque
                    self.estoque.produtos[produto_codigo]["quantidade"] -= quantidade
                    
                    self.consumo_display_area.insert("end", f"Consumo registrado: Cliente {cliente}, Produto {produto}, Qtd: {quantidade}, Total R${total:.2f}\n")
                    self.update_consumo_comboboxes() 
                    self.update_caixa_cliente_combobox() # Atualizar caixa se novo cliente tem conta
                    self.exibir_estoque() 
                else:
                    self.consumo_display_area.insert("end", f"Erro: Quantidade em estoque insuficiente para {produto}.\n")
            else:
                self.consumo_display_area.insert("end", "Erro ao registrar consumo: Cliente ou Produto não encontrado.\n")
        except ValueError:
            self.consumo_display_area.insert("end", "Erro: Quantidade deve ser um número inteiro.\n")

    def remover_consumo(self):
        self.consumo_display_area.insert("end", "Funcionalidade de remoção de consumo ainda não implementada.\n")

    def exibir_consumos(self):
        self.consumo_display_area.delete("1.0", "end")
        if not self.consumos_registrados:
            self.consumo_display_area.insert("end", "Nenhum consumo registrado.\n")
        else:
            self.consumo_display_area.insert("end", "--- Lista de Consumos Registrados ---\n")
            # Ordenar por timestamp para consistência, talvez mais recentes primeiro
            for consumo in sorted(self.consumos_registrados, key=lambda x: x.get('timestamp', ''), reverse=True):
                info = (f"ID: {consumo.get('id', 'N/A')}, Cliente: {consumo['cliente']}, Produto: {consumo['produto']}, "
                        f"Qtd: {consumo['quantidade']}, Preço Unit.: R${consumo['preco_unitario']:.2f}, "
                        f"Total: R${consumo['total']:.2f}, Data: {consumo.get('timestamp', 'N/A')}, "
                        f"Status: {consumo.get('status', 'N/A')}\n")
                self.consumo_display_area.insert("end", info)
            self.consumo_display_area.insert("end", "-----------------------------------\n")

    def adicionar_produto(self):
        nome = self.nome_entry.get().strip()
        preco = self.preco_entry.get().strip()
        quantidade = self.produto_quantidade_entry.get().strip()

        # Depuração: Exibir valores capturados
        self.display_area.insert("end", f"Depuração: Nome='{nome}', Preço='{preco}', Quantidade='{quantidade}'\n")

        # Verificar se todos os campos estão preenchidos
        if not nome:
            self.display_area.insert("end", "Erro: O campo Nome está vazio.\n")
            return
        if not preco:
            self.display_area.insert("end", "Erro: O campo Preço está vazio.\n")
            return
        if not quantidade:
            self.display_area.insert("end", "Erro: O campo Quantidade está vazio.\n")
            return

        try:
            preco = float(preco.replace(',', '.'))
        except ValueError:
            self.display_area.insert("end", "Erro: Preço deve ser um número válido.\n")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            self.display_area.insert("end", "Erro: Quantidade deve ser um número inteiro válido.\n")
            return

        codigo = self.estoque.adicionar_produto(nome, preco, quantidade)
        self.display_area.insert("end", f"Produto {nome} adicionado com sucesso! Código: {codigo}\n")
        self.update_consumo_comboboxes()

    def remover_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para remover um produto.\n")
            return

        try:
            codigo = int(codigo)
            self.estoque.remover_produto(codigo)
            self.display_area.insert("end", f"Produto com código {codigo} marcado como excluído.\n")
            self.update_consumo_comboboxes()
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
            if preco: # Se o preço foi fornecido para atualização
                preco = float(preco.replace(',', '.'))
            quantidade = int(quantidade) if quantidade else None
            self.estoque.atualizar_produto(codigo, nome, preco, quantidade)
            self.display_area.insert("end", f"Produto com código {codigo} atualizado com sucesso!\n")
        except ValueError:
            self.display_area.insert("end", "Erro: Código deve ser um número inteiro, Preço (ex: 10.50) deve ser um número e Quantidade deve ser um inteiro.\n")

    def reativar_produto(self):
        codigo = self.codigo_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para reativar um produto.\n")
            return

        try:
            codigo = int(codigo)
            self.estoque.reativar_produto(codigo)
            self.display_area.insert("end", f"Produto com código {codigo} reativado com sucesso!\n")
            self.update_consumo_comboboxes()
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
        nome = self.cliente_nome_entry.get().strip() # Adicionado .strip()
        documento = self.documento_entry.get().strip()
        telefone = self.telefone_entry.get().strip()

        if not (nome and documento): # 'nome' já está stripado
            self.clientes_display_area.insert("end", "Os campos Nome e Documento são obrigatórios para adicionar um cliente/mesa.\n")
            return

        codigo = self.clientes.adicionar_cliente(nome, documento, telefone)
        self.clientes_display_area.insert("end", f"Cliente/Mesa {nome} adicionado com sucesso! Código: {codigo}\n")
        self.update_consumo_comboboxes()

    def remover_cliente(self):
        codigo = self.cliente_nome_entry.get()

        if not codigo:
            self.clientes_display_area.insert("end", "O campo Código deve ser preenchido para remover um cliente.\n")
            return

        try:
            codigo = int(codigo)
            self.clientes.remover_cliente(codigo)
            self.clientes_display_area.insert("end", f"Cliente com código {codigo} marcado como excluído.\n")
            self.update_consumo_comboboxes()
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
            self.update_consumo_comboboxes()
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
        self.salvar_consumos() # Salvar consumos ao sair
        self.window.destroy()

    def carregar_consumos(self, arquivo_csv="consumos.csv"):
        try:
            with open(arquivo_csv, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for linha in reader:
                    try:
                        consumo = {
                            "id": int(linha["id"]),
                            "cliente": linha["cliente"],
                            "produto": linha["produto"],
                            "quantidade": int(linha["quantidade"]),
                            "preco_unitario": float(linha["preco_unitario"]),
                            "total": float(linha["total"]),
                            "timestamp": linha["timestamp"],
                            "status": linha["status"]
                        }
                        self.consumos_registrados.append(consumo)
                    except ValueError as e:
                        print(f"Erro ao converter dados do consumo ao carregar: {linha} - {e}")
                    except KeyError as e:
                        print(f"Campo faltando no consumo ao carregar: {linha} - {e}")
            
            # Garantir que o próximo ID de consumo seja maior que qualquer ID carregado
            if self.consumos_registrados:
                # Esta linha não é necessária se o ID é sempre len(...) + 1, 
                # mas seria para um sistema de ID mais robusto.
                # self.proximo_id_consumo = max(c['id'] for c in self.consumos_registrados) + 1
                pass # ID é gerado por len(self.consumos_registrados) + 1

        except FileNotFoundError:
            # Arquivo não existe, começa com lista vazia (normal na primeira execução)
            pass
        except Exception as e:
            # Outros erros ao carregar o arquivo
            print(f"Erro inesperado ao carregar consumos de {arquivo_csv}: {e}")

    def salvar_consumos(self, arquivo_csv="consumos.csv"):
        try:
            with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
                if not self.consumos_registrados: # Não escreve nada se não há consumos (nem cabeçalho)
                    # Ou pode optar por escrever apenas o cabeçalho se o arquivo deve existir
                    # file.write("id,cliente,produto,quantidade,preco_unitario,total,timestamp,status\n")
                    return

                fieldnames = ["id", "cliente", "produto", "quantidade", "preco_unitario", "total", "timestamp", "status"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for consumo in self.consumos_registrados:
                    writer.writerow(consumo)
        except Exception as e:
            print(f"Erro ao salvar consumos em {arquivo_csv}: {e}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EstoqueUI()
    app.run()
