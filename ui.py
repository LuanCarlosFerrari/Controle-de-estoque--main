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
        # Clientes com contas que não estão totalmente pagas (abertas ou parcialmente pagas)
        clientes_com_contas_pendentes = sorted(list(set(c["cliente"] for c in self.consumos_registrados if c["status"] != "pago")))
        if clientes_com_contas_pendentes:
            self.caixa_cliente_combobox.configure(values=clientes_com_contas_pendentes)
            self.caixa_cliente_combobox.set(clientes_com_contas_pendentes[0])
            self.display_conta_cliente() # Display items for the first client
        else:
            self.caixa_cliente_combobox.configure(values=["Nenhum cliente com conta pendente"])
            self.caixa_cliente_combobox.set("Nenhum cliente com conta pendente")
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", "Nenhum consumo pendente para exibir.\n")

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

        # Label for status messages
        self.product_status_label = ctk.CTkLabel(self.produtos_tab, text="", height=1, anchor="w")
        self.product_status_label.pack(padx=20, pady=(5, 0), fill="x")

        # Frame for the products table
        self.products_table_frame = ctk.CTkScrollableFrame(self.produtos_tab, height=300)
        self.products_table_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Initial call to display headers or empty state
        self.exibir_estoque() 

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

        # Label for status messages in Clientes tab
        self.client_status_label = ctk.CTkLabel(self.clientes_tab, text="", height=1, anchor="w")
        self.client_status_label.pack(padx=20, pady=(5, 0), fill="x")

        # Frame for the clients table
        self.clients_table_frame = ctk.CTkScrollableFrame(self.clientes_tab, height=300)
        self.clients_table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Initial call to display headers or empty state
        self.exibir_clientes()

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

        if selected_client == "Nenhum cliente com conta aberta" or selected_client == "Nenhum cliente com conta pendente" or not selected_client: # Check stripped name
            self.caixa_display_area.insert("end", "Nenhum cliente selecionado ou sem contas pendentes.\n")
            return

        # Coleta consumos que não estão totalmente pagos ('aberto' ou 'parcialmente_pago')
        consumos_cliente_nao_pagos = [
            c for c in self.consumos_registrados 
            if c["cliente"] == selected_client and c.get("status", "aberto") != "pago"
        ]
        # Ordenar por timestamp para consistência na exibição e processamento
        consumos_cliente_nao_pagos.sort(key=lambda x: x.get("timestamp", ""))

        if not consumos_cliente_nao_pagos:
            self.caixa_display_area.insert("end", f"Nenhuma conta pendente (aberta ou parcialmente paga) para o cliente: {selected_client}\n")
            return

        self.caixa_display_area.insert("end", f"--- Conta de: {selected_client} ---\n")
        total_geral_devido_na_conta = 0.0
        for consumo in consumos_cliente_nao_pagos:
            valor_total_item = consumo.get('total', 0.0)
            valor_pago_neste_item = consumo.get("valor_pago_item", 0.0)
            valor_restante_neste_item = valor_total_item - valor_pago_neste_item
            total_geral_devido_na_conta += valor_restante_neste_item

            info = (f"ID: {consumo.get('id', 'N/A')}, Produto: {consumo.get('produto', 'N/A')}, Qtd: {consumo.get('quantidade', 0)}\n"
                    f"  Total Original do Item: R${valor_total_item:.2f}\n"
                    f"  Valor Pago neste Item: R${valor_pago_neste_item:.2f}\n"
                    f"  Valor Restante neste Item: R${valor_restante_neste_item:.2f}\n"
                    f"  Data: {consumo.get('timestamp', 'N/A')}, Status: {consumo.get('status', 'N/A').upper()}\n"
                    f"-----------------------------------\n")
            self.caixa_display_area.insert("end", info)
        
        self.caixa_display_area.insert("end", f"TOTAL DEVIDO NA CONTA: R${total_geral_devido_na_conta:.2f}\n")
        self.caixa_display_area.insert("end", "===================================\n")
        return total_geral_devido_na_conta # Retorna o total devido calculado

    def realizar_pagamento_caixa(self):
        selected_client_raw = self.caixa_cliente_combobox.get()
        if not selected_client_raw or selected_client_raw == "Nenhum cliente com conta pendente":
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", "ERRO: Nenhum cliente com conta pendente selecionado.\n")
            return
        selected_client = selected_client_raw.strip()
        
        valor_pago_str = self.caixa_valor_pago_entry.get()
        
        # Limpar a área de exibição no início da função para novas mensagens.
        # self.caixa_display_area.delete("1.0", "end") # Movido para depois da validação do valor pago

        if not valor_pago_str:
            # Não limpar a tela ainda, apenas adicionar mensagem de erro se o valor não for informado
            # para que o usuário veja o erro no contexto da conta atual.
            current_text = self.caixa_display_area.get("1.0", "end-1c") # Salva o texto atual
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", current_text + "\nERRO: Informe o valor a pagar.\n")
            return

        try:
            valor_pago_informado = float(valor_pago_str.replace(',', '.'))
            if valor_pago_informado <= 0.001: # Permitir pagamentos muito pequenos se necessário, mas geralmente > 0
                current_text = self.caixa_display_area.get("1.0", "end-1c")
                self.caixa_display_area.delete("1.0", "end")
                self.caixa_display_area.insert("end", current_text + "\nERRO: Valor a pagar deve ser positivo.\n")
                return
        except ValueError:
            current_text = self.caixa_display_area.get("1.0", "end-1c")
            self.caixa_display_area.delete("1.0", "end")
            self.caixa_display_area.insert("end", current_text + "\nERRO: Valor a pagar inválido.\n")
            return

        # Agora que as entradas são válidas, limpar a área para o resumo do pagamento e a conta atualizada.
        self.caixa_display_area.delete("1.0", "end")

        # Coletar itens que estão 'aberto' ou 'parcialmente_pago'
        itens_a_processar_pagamento = []
        for i, c in enumerate(self.consumos_registrados):
            # Usar .get("status", "aberto") para retrocompatibilidade se status não existir
            if c["cliente"] == selected_client and c.get("status", "aberto") != "pago":
                itens_a_processar_pagamento.append({
                    "id": c["id"],
                    "total_original_item": c["total"],
                    "valor_ja_pago_item": c.get("valor_pago_item", 0.0),
                    "timestamp": c.get("timestamp", ""), # Lidar com possível ausência de timestamp
                    "original_index": i 
                })

        itens_a_processar_pagamento.sort(key=lambda x: x["timestamp"])

        if not itens_a_processar_pagamento:
            self.caixa_display_area.insert("end", f"INFO: Nenhuma conta pendente para {selected_client} para aplicar pagamento.\n")
            # Mesmo sem itens, mostrar o "pagamento" como não utilizado se um valor foi informado
            if valor_pago_informado > 0:
                 self.caixa_display_area.insert("end", f"Valor informado de R${valor_pago_informado:.2f} não foi utilizado.\n")
            self.caixa_valor_pago_entry.delete(0, "end")
            self.update_caixa_cliente_combobox()
            self.update_consumo_comboboxes()
            return
            
        valor_disponivel_para_pagar = valor_pago_informado
        total_efetivamente_pago_nesta_operacao = 0.0
        itens_afetados_nesta_operacao_log = []

        for item_em_processamento in itens_a_processar_pagamento:
            if valor_disponivel_para_pagar < 0.01: # Se não há mais dinheiro significativo para aplicar
                break

            original_idx = item_em_processamento['original_index']
            consumo_original_ref = self.consumos_registrados[original_idx]

            if consumo_original_ref['id'] != item_em_processamento['id'] or consumo_original_ref.get('status','aberto') == 'pago':
                print(f"DEBUG: Discrepância ou item já pago ao tentar processar item ID {item_em_processamento['id']}")
                continue

            valor_devido_neste_item = consumo_original_ref['total'] - consumo_original_ref.get('valor_pago_item', 0.0)
            
            # Arredondar para evitar problemas com float
            valor_devido_neste_item = round(valor_devido_neste_item, 2)

            if valor_devido_neste_item <= 0:
                continue # Item já está (ou deveria estar) pago, pular

            valor_a_aplicar_neste_item = 0.0
            if valor_disponivel_para_pagar >= valor_devido_neste_item:
                valor_a_aplicar_neste_item = valor_devido_neste_item
                consumo_original_ref['valor_pago_item'] = round(consumo_original_ref.get('valor_pago_item', 0.0) + valor_a_aplicar_neste_item, 2)
                # Verificar se o item está totalmente pago após a aplicação
                if round(consumo_original_ref['total'] - consumo_original_ref['valor_pago_item'], 2) < 0.01:
                    consumo_original_ref['status'] = "pago"
                    consumo_original_ref['valor_pago_item'] = consumo_original_ref['total'] # Garante exatidão
                else: # Isso não deveria acontecer se valor_disponivel >= valor_devido
                    consumo_original_ref['status'] = "parcialmente_pago" 
            else: # Pagamento é menor que o devido no item, aplica o que resta do pagamento
                valor_a_aplicar_neste_item = valor_disponivel_para_pagar
                consumo_original_ref['valor_pago_item'] = round(consumo_original_ref.get('valor_pago_item', 0.0) + valor_a_aplicar_neste_item, 2)
                consumo_original_ref['status'] = "parcialmente_pago"
            
            consumo_original_ref['valor_pago_item'] = round(consumo_original_ref['valor_pago_item'], 2)
            total_efetivamente_pago_nesta_operacao += valor_a_aplicar_neste_item
            total_efetivamente_pago_nesta_operacao = round(total_efetivamente_pago_nesta_operacao, 2)
            valor_disponivel_para_pagar -= valor_a_aplicar_neste_item
            valor_disponivel_para_pagar = round(valor_disponivel_para_pagar, 2)
            
            itens_afetados_nesta_operacao_log.append(
                f"ID {consumo_original_ref['id']} (R${valor_a_aplicar_neste_item:.2f} aplicados, Novo Status: {consumo_original_ref['status'].upper()})"
            )

        # --- Exibição do resumo e atualização da UI ---
        self.caixa_valor_pago_entry.delete(0, "end")
        
        # Chamar display_conta_cliente PRIMEIRO para limpar e mostrar o estado atualizado da conta
        self.display_conta_cliente(client_name_to_display=selected_client) 

        # DEPOIS, anexar o resumo do pagamento que acabou de ser processado
        summary_message = f"\n--- Resumo do Pagamento para {selected_client} ---\n"
        summary_message += f"Valor Informado para Pagamento: R${valor_pago_informado:.2f}\n"
        summary_message += f"Total Efetivamente Aplicado nesta Operação: R${total_efetivamente_pago_nesta_operacao:.2f}\n"

        if valor_disponivel_para_pagar > 0.001: # Se houver troco/valor não utilizado significativo
            summary_message += f"Valor Restante do Pagamento (Troco/Não Utilizado): R${valor_disponivel_para_pagar:.2f}\n"
        
        if itens_afetados_nesta_operacao_log:
            summary_message += "Itens Afetados:\n"
            for log_entry in itens_afetados_nesta_operacao_log:
                summary_message += f"  - {log_entry}\n"
        elif valor_pago_informado > 0: # Se um pagamento foi informado mas nada foi afetado
            summary_message += "Nenhum item foi afetado por este pagamento (valor pode ter sido insuficiente ou já não há itens pendentes).\n"
        
        summary_message += "===================================\n"
        self.caixa_display_area.insert("end", summary_message) # Anexa o resumo
        
        self.update_caixa_cliente_combobox() 
        self.update_consumo_comboboxes()

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

        # Label for status messages in Consumo tab
        self.consumo_status_label = ctk.CTkLabel(self.consumo_tab, text="", height=1, anchor="w")
        self.consumo_status_label.pack(padx=20, pady=(5,0), fill="x")

        # Frame for the consumos table
        self.consumos_table_frame = ctk.CTkScrollableFrame(self.consumo_tab, height=300)
        self.consumos_table_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.exibir_consumos() # Initial display

    def registrar_consumo(self):
        cliente = self.cliente_combobox.get()
        produto = self.produto_combobox.get()
        cliente = self.cliente_combobox.get()
        produto = self.produto_combobox.get()
        quantidade_str = self.consumo_quantidade_entry.get().strip()

        if not (cliente and cliente != "Nenhum cliente ativo" and 
                produto and produto != "Nenhum produto ativo" and 
                quantidade_str):
            self.consumo_status_label.configure(text="Todos os campos (Cliente, Produto, Quantidade) devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                self.consumo_status_label.configure(text="Erro: Quantidade deve ser um número positivo.")
                return
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
                        "status": "aberto",  # 'aberto', 'parcialmente_pago', 'pago'
                        "valor_pago_item": 0.0 # Novo campo para rastrear o valor pago por este item
                    }
                    self.consumos_registrados.append(consumo_info)
                    
                    # Deduzir do estoque
                    self.estoque.produtos[produto_codigo]["quantidade"] -= quantidade
                    
                    self.consumo_status_label.configure(text=f"Consumo: {cliente}, {produto}, Qtd: {quantidade}, Total R${total:.2f}")
                    self.consumo_quantidade_entry.delete(0, "end") # Clear quantity entry
                    self.update_consumo_comboboxes() 
                    self.update_caixa_cliente_combobox() 
                    self.exibir_estoque() # Refresh product stock display if visible
                    self.exibir_consumos() # Refresh consumos table
                else:
                    self.consumo_status_label.configure(text=f"Erro: Quantidade em estoque insuficiente para {produto}.")
            else:
                self.consumo_status_label.configure(text="Erro: Cliente ou Produto não encontrado/ativo.")
        except ValueError:
            self.consumo_status_label.configure(text="Erro: Quantidade deve ser um número inteiro.")

    def remover_consumo(self):
        # Esta funcionalidade precisa de uma forma de identificar qual consumo remover (e.g., por ID)
        # e lógica para reverter o débito do estoque, etc.
        self.consumo_status_label.configure(text="Funcionalidade de remoção de consumo ainda não implementada.")

    def exibir_consumos(self):
        for widget in self.consumos_table_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Cliente", "Produto", "Qtd", "Preço Unit.", "Total Item", "Data/Hora", "Status", "Pago"]
        # Define relative column widths
        column_widths = [0.05, 0.15, 0.15, 0.05, 0.1, 0.1, 0.2, 0.1, 0.1]

        for col, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(self.consumos_table_frame, text=header_text, font=ctk.CTkFont(weight="bold"), anchor="center")
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        for i, weight in enumerate(column_widths):
            self.consumos_table_frame.grid_columnconfigure(i, weight=int(weight * 100))
        
        if not self.consumos_registrados:
            no_data_label = ctk.CTkLabel(self.consumos_table_frame, text="Nenhum consumo registrado.")
            no_data_label.grid(row=1, column=0, columnspan=len(headers), padx=5, pady=10, sticky="nsew")
            self.consumo_status_label.configure(text="Nenhum consumo registrado.")
        else:
            row_num = 1
            # Sort by timestamp, most recent first
            sorted_consumos = sorted(self.consumos_registrados, key=lambda x: x.get('timestamp', ''), reverse=True)
            
            for consumo in sorted_consumos:
                data_to_display = [
                    consumo.get('id', 'N/A'),
                    consumo.get('cliente', 'N/A'),
                    consumo.get('produto', 'N/A'),
                    consumo.get('quantidade', 0),
                    f"{consumo.get('preco_unitario', 0.0):.2f}",
                    f"{consumo.get('total', 0.0):.2f}",
                    consumo.get('timestamp', 'N/A'),
                    consumo.get('status', 'N/A').upper(),
                    f"{consumo.get('valor_pago_item', 0.0):.2f}"
                ]
                for col, item_data in enumerate(data_to_display):
                    item_label = ctk.CTkLabel(self.consumos_table_frame, text=str(item_data), anchor="center")
                    item_label.grid(row=row_num, column=col, padx=5, pady=2, sticky="nsew")
                row_num += 1
            self.consumo_status_label.configure(text=f"{len(self.consumos_registrados)} consumos exibidos.")

    def adicionar_produto(self):
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        quantidade_str = self.produto_quantidade_entry.get().strip()

        if not nome:
            self.product_status_label.configure(text="Erro: O campo Nome está vazio.")
            return
        if not preco_str:
            self.product_status_label.configure(text="Erro: O campo Preço está vazio.")
            return
        if not quantidade_str:
            self.product_status_label.configure(text="Erro: O campo Quantidade está vazio.")
            return

        try:
            preco = float(preco_str.replace(',', '.'))
        except ValueError:
            self.product_status_label.configure(text="Erro: Preço deve ser um número válido.")
            return

        try:
            quantidade = int(quantidade_str)
        except ValueError:
            self.product_status_label.configure(text="Erro: Quantidade deve ser um número inteiro válido.")
            return

        codigo = self.estoque.adicionar_produto(nome, preco, quantidade)
        self.product_status_label.configure(text=f"Produto {nome} adicionado com sucesso! Código: {codigo}")
        self.update_consumo_comboboxes()
        self.exibir_estoque() # Refresh table

    def remover_produto(self):
        codigo_str = self.codigo_entry.get().strip()

        if not codigo_str:
            self.product_status_label.configure(text="O campo Código deve ser preenchido para remover um produto.")
            return

        try:
            codigo = int(codigo_str)
            self.estoque.remover_produto(codigo)
            self.product_status_label.configure(text=f"Produto com código {codigo} marcado como excluído.")
            self.update_consumo_comboboxes()
            self.exibir_estoque() # Refresh table
        except ValueError:
            self.product_status_label.configure(text="Erro: Código deve ser um número inteiro.")

    def atualizar_produto(self):
        codigo_str = self.codigo_entry.get().strip()
        nome = self.nome_entry.get().strip() or None # Use strip here as well
        preco_str = self.preco_entry.get().strip()
        # Assuming self.quantidade_entry was a typo and it's self.produto_quantidade_entry for products tab
        quantidade_str = self.produto_quantidade_entry.get().strip()


        if not codigo_str:
            self.product_status_label.configure(text="O campo Código deve ser preenchido para atualizar um produto.")
            return

        try:
            codigo = int(codigo_str)
            preco = None
            if preco_str:
                preco = float(preco_str.replace(',', '.'))
            
            quantidade = None
            if quantidade_str:
                quantidade = int(quantidade_str)
                
            self.estoque.atualizar_produto(codigo, nome, preco, quantidade)
            self.product_status_label.configure(text=f"Produto com código {codigo} atualizado com sucesso!")
            self.update_consumo_comboboxes() # if product name/price changes
            self.exibir_estoque() # Refresh table
        except ValueError:
            self.product_status_label.configure(text="Erro: Código deve ser int, Preço float, Quantidade int.")

    def reativar_produto(self):
        codigo_str = self.codigo_entry.get().strip()

        if not codigo_str:
            self.product_status_label.configure(text="O campo Código deve ser preenchido para reativar um produto.")
            return

        try:
            codigo = int(codigo_str)
            self.estoque.reativar_produto(codigo)
            self.product_status_label.configure(text=f"Produto com código {codigo} reativado com sucesso!")
            self.update_consumo_comboboxes()
            self.exibir_estoque() # Refresh table
        except ValueError:
            self.product_status_label.configure(text="Erro: Código deve ser um número inteiro.")

    def exibir_estoque(self):
        # Clear previous widgets in the frame
        for widget in self.products_table_frame.winfo_children():
            widget.destroy()

        # Define headers
        headers = ["Código", "Nome", "Preço (R$)", "Quantidade", "Status"]
        column_widths = [0.1, 0.3, 0.15, 0.15, 0.2] # Relative widths

        for col, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(self.products_table_frame, text=header_text, font=ctk.CTkFont(weight="bold"), anchor="center")
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure column weights for the frame's grid
        for i, weight in enumerate(column_widths):
             self.products_table_frame.grid_columnconfigure(i, weight=int(weight*100)) # Use integer weights


        if not self.estoque.produtos:
            no_data_label = ctk.CTkLabel(self.products_table_frame, text="Estoque vazio.")
            no_data_label.grid(row=1, column=0, columnspan=len(headers), padx=5, pady=10, sticky="nsew")
            self.product_status_label.configure(text="Estoque vazio.")
        else:
            row_num = 1
            # Sort products by code (assuming codes are integers or can be directly compared)
            # Given the AttributeError, codes are likely integers.
            sorted_codigos = sorted(self.estoque.produtos.keys())

            for codigo in sorted_codigos:
                dados = self.estoque.produtos[codigo]
                data_to_display = [
                    codigo,
                    dados['nome'],
                    f"{dados['preco']:.2f}",
                    dados['quantidade'],
                    dados['status']
                ]
                for col, item_data in enumerate(data_to_display):
                    item_label = ctk.CTkLabel(self.products_table_frame, text=str(item_data), anchor="center")
                    item_label.grid(row=row_num, column=col, padx=5, pady=2, sticky="nsew")
                row_num += 1
            if row_num == 1: # Should be caught by `if not self.estoque.produtos` but as a fallback
                self.product_status_label.configure(text="Estoque carregado.") # Or some other neutral message
            else:
                 self.product_status_label.configure(text=f"{len(self.estoque.produtos)} produtos exibidos.")


    def adicionar_cliente(self):
        nome = self.cliente_nome_entry.get().strip()
        documento = self.documento_entry.get().strip()
        telefone = self.telefone_entry.get().strip()

        if not (nome and documento):
            self.client_status_label.configure(text="Os campos Nome e Documento são obrigatórios.")
            return

        codigo = self.clientes.adicionar_cliente(nome, documento, telefone)
        self.client_status_label.configure(text=f"Cliente/Mesa {nome} adicionado! Código: {codigo}")
        self.update_consumo_comboboxes()
        self.update_caixa_cliente_combobox() # Clientes might now have open accounts
        self.exibir_clientes()

    def remover_cliente(self):
        # Assuming codigo for removal is identified by Nome do Cliente/Mesa entry for now
        # This might need adjustment if a dedicated "Código do Cliente" entry is preferred for operations
        nome_cliente_para_remover = self.cliente_nome_entry.get().strip() 
        if not nome_cliente_para_remover:
            self.client_status_label.configure(text="Nome do Cliente/Mesa deve ser preenchido para remover.")
            return

        # Find client code by name - this is a simplification.
        # A more robust system would use a dedicated code entry or selection from the table.
        client_code_to_remove = None
        for code, data in self.clientes.clientes.items():
            if data["nome"] == nome_cliente_para_remover:
                client_code_to_remove = code
                break
        
        if client_code_to_remove is None:
            self.client_status_label.configure(text=f"Cliente/Mesa '{nome_cliente_para_remover}' não encontrado.")
            return

        try:
            # The self.clientes.remover_cliente likely expects an integer code
            self.clientes.remover_cliente(int(client_code_to_remove)) 
            self.client_status_label.configure(text=f"Cliente/Mesa cód. {client_code_to_remove} marcado como excluído.")
            self.update_consumo_comboboxes()
            self.update_caixa_cliente_combobox()
            self.exibir_clientes()
        except ValueError: # Should not happen if client_code_to_remove is from keys
            self.client_status_label.configure(text="Erro: Código do cliente inválido para remoção.")
        except Exception as e:
            self.client_status_label.configure(text=f"Erro ao remover cliente: {e}")


    def atualizar_cliente(self):
        # Similar to remover_cliente, identifying client by name from entry for update is a simplification.
        nome_cliente_para_atualizar = self.cliente_nome_entry.get().strip()
        novo_documento = self.documento_entry.get().strip() or None
        novo_telefone = self.telefone_entry.get().strip() or None

        if not nome_cliente_para_atualizar:
            self.client_status_label.configure(text="Nome do Cliente/Mesa deve ser preenchido para atualizar.")
            return

        client_code_to_update = None
        current_nome = None
        for code, data in self.clientes.clientes.items():
            if data["nome"] == nome_cliente_para_atualizar:
                client_code_to_update = code
                current_nome = data["nome"] # Keep current name if not changing via a dedicated field
                break
        
        if client_code_to_update is None:
            self.client_status_label.configure(text=f"Cliente/Mesa '{nome_cliente_para_atualizar}' não encontrado.")
            return

        try:
            # Pass current_nome as 'nome' if not changing, or a new name if a field for it existed
            self.clientes.atualizar_cliente(int(client_code_to_update), current_nome, novo_documento, novo_telefone)
            self.client_status_label.configure(text=f"Cliente/Mesa cód. {client_code_to_update} atualizado.")
            self.update_consumo_comboboxes() # Name might change
            self.update_caixa_cliente_combobox() # Name might change
            self.exibir_clientes()
        except ValueError:
            self.client_status_label.configure(text="Erro: Código do cliente inválido para atualização.")
        except Exception as e:
            self.client_status_label.configure(text=f"Erro ao atualizar cliente: {e}")

    def reativar_cliente(self):
        nome_cliente_para_reativar = self.cliente_nome_entry.get().strip()
        if not nome_cliente_para_reativar:
            self.client_status_label.configure(text="Nome do Cliente/Mesa deve ser preenchido para reativar.")
            return

        client_code_to_reativate = None
        for code, data in self.clientes.clientes.items():
            if data["nome"] == nome_cliente_para_reativar:
                client_code_to_reativate = code
                break
        
        if client_code_to_reativate is None:
            self.client_status_label.configure(text=f"Cliente/Mesa '{nome_cliente_para_reativar}' não encontrado.")
            return
            
        try:
            self.clientes.reativar_cliente(int(client_code_to_reativate))
            self.client_status_label.configure(text=f"Cliente/Mesa cód. {client_code_to_reativate} reativado.")
            self.update_consumo_comboboxes()
            self.update_caixa_cliente_combobox()
            self.exibir_clientes()
        except ValueError:
            self.client_status_label.configure(text="Erro: Código do cliente inválido para reativação.")
        except Exception as e:
            self.client_status_label.configure(text=f"Erro ao reativar cliente: {e}")

    def exibir_clientes(self):
        for widget in self.clients_table_frame.winfo_children():
            widget.destroy()

        headers = ["Código", "Nome", "Documento/Mesa", "Telefone", "Status"]
        # Adjust column widths as needed
        column_widths = [0.1, 0.3, 0.25, 0.2, 0.15] 

        for col, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(self.clients_table_frame, text=header_text, font=ctk.CTkFont(weight="bold"), anchor="center")
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        for i, weight in enumerate(column_widths):
             self.clients_table_frame.grid_columnconfigure(i, weight=int(weight*100))

        if not self.clientes.clientes:
            no_data_label = ctk.CTkLabel(self.clients_table_frame, text="Nenhum cliente/mesa cadastrado.")
            no_data_label.grid(row=1, column=0, columnspan=len(headers), padx=5, pady=10, sticky="nsew")
            self.client_status_label.configure(text="Nenhum cliente/mesa cadastrado.")
        else:
            row_num = 1
            # Assuming client codes are sortable (e.g., integers or numeric strings)
            sorted_codigos = sorted(self.clientes.clientes.keys(), key=lambda x: int(x) if str(x).isdigit() else str(x))


            for codigo in sorted_codigos:
                dados = self.clientes.clientes[codigo]
                # 'mesa' is used for documento in Clientes model based on previous context
                data_to_display = [
                    codigo,
                    dados.get('nome', 'N/A'),
                    dados.get('mesa', 'N/A'), # 'mesa' field seems to hold Documento
                    dados.get('telefone', 'N/A'),
                    dados.get('status', 'N/A')
                ]
                for col, item_data in enumerate(data_to_display):
                    item_label = ctk.CTkLabel(self.clients_table_frame, text=str(item_data), anchor="center")
                    item_label.grid(row=row_num, column=col, padx=5, pady=2, sticky="nsew")
                row_num += 1
            self.client_status_label.configure(text=f"{len(self.clientes.clientes)} clientes/mesas exibidos.")
            
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
                            "status": linha["status"],
                            "valor_pago_item": float(linha.get("valor_pago_item", 0.0)) # Carrega o novo campo, com padrão 0.0 se não existir
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
                    # file.write("id,cliente,produto,quantidade,preco_unitario,total,timestamp,status,valor_pago_item\n")
                    return

                fieldnames = ["id", "cliente", "produto", "quantidade", "preco_unitario", "total", "timestamp", "status", "valor_pago_item"]
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
