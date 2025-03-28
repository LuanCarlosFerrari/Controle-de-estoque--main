import customtkinter as ctk
from models.estoque import Estoque
from models.clientes import Clientes
import csv
from tkinter import ttk

class EstoqueUI:
    def __init__(self):
        self.estoque = Estoque()
        self.clientes = Clientes()

        # Configuração da janela principal
        self.window = ctk.CTk()
        self.window.title("Sistema de Controle")
        self.window.geometry("1000x600")  # Ajustado para apresentar todas as abas adequadamente

        # Exibir estoque ao iniciar para confirmar carregamento
        print(f"Estoque carregado: {self.estoque.produtos}")

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
        
    def habilitar_para_remocao(self):
        # Limpar o campo de código e habilitar para inserção
        self.codigo_entry.configure(state="normal")  # Habilita o campo
        self.codigo_entry.delete(0, "end")  # Limpa o conteúdo existente
        self.display_area.insert("end", "Digite o código do produto que deseja remover e clique em 'Remover'.\n")
        
        # Redefinir função do botão Remover
        for widget in self.produtos_tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and child.cget("text") == "Remover":
                        child.configure(command=self.remover_produto)
                        
    def habilitar_para_atualizacao(self):
        # Limpar e habilitar campos para atualização
        self.codigo_entry.configure(state="normal")  # Habilita o campo
        self.codigo_entry.delete(0, "end")  # Limpa o conteúdo existente
        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.produtos_quantidade_entry.delete(0, "end")
        self.display_area.insert("end", "Digite o código do produto que deseja atualizar, preencha apenas os campos que deseja modificar e clique em 'Atualizar'.\n")
        
        # Redefinir função do botão Atualizar
        for widget in self.produtos_tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and child.cget("text") == "Atualizar":
                        child.configure(command=self.atualizar_produto)
                        
    def habilitar_para_reativacao(self):
        # Limpar o campo de código e habilitar para inserção
        self.codigo_entry.configure(state="normal")  # Habilita o campo
        self.codigo_entry.delete(0, "end")  # Limpa o conteúdo existente
        self.display_area.insert("end", "Digite o código do produto que deseja reativar e clique em 'Reativar'.\n")
        
        # Redefinir função do botão Reativar
        for widget in self.produtos_tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton) and child.cget("text") == "Reativar":
                        child.configure(command=self.reativar_produto)
    
    def setup_produtos_tab(self):
        # Reutilizar a lógica existente para a aba de produtos
        input_frame = ctk.CTkFrame(self.produtos_tab)
        input_frame.pack(padx=20, pady=10, fill="x")

        input_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Campos de entrada com labels
        ctk.CTkLabel(input_frame, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.codigo_entry = ctk.CTkEntry(input_frame)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Adicionar texto de placeholder no campo de código
        self.codigo_entry.insert(0, "Gerado pelo sistema")
        self.codigo_entry.configure(state="disabled")  # Desabilita o campo por padrão

        ctk.CTkLabel(input_frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.nome_entry = ctk.CTkEntry(input_frame)
        self.nome_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Preço:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.preco_entry = ctk.CTkEntry(input_frame)
        self.preco_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.produtos_quantidade_entry = ctk.CTkEntry(input_frame)
        self.produtos_quantidade_entry.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        button_frame = ctk.CTkFrame(self.produtos_tab)
        button_frame.pack(padx=20, pady=10)

        # Botões de ação
        ctk.CTkButton(button_frame, text="Adicionar", command=self.adicionar_produto).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Remover", command=self.habilitar_para_remocao).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.habilitar_para_atualizacao).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Reativar", command=self.habilitar_para_reativacao).pack(side="left", padx=5)
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

        # Preparar listas de nomes para os comboboxes
        cliente_nomes = []
        for codigo, cliente in self.clientes.clientes.items():
            if cliente["status"] == "ativo":
                cliente_nomes.append(f"{codigo} - {cliente['nome']}")
                
        produto_nomes = []
        for codigo, produto in self.estoque.produtos.items():
            if produto["status"] == "ativo":
                produto_nomes.append(f"{codigo} - {produto['nome']}")

        ctk.CTkLabel(input_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cliente_combobox = ctk.CTkComboBox(input_frame, values=cliente_nomes)
        self.cliente_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(input_frame, text="Produto:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.produto_combobox = ctk.CTkComboBox(input_frame, values=produto_nomes)
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
        
        # Cabeçalho formatado com espaçamento uniforme
        header = f"{'ID':<5} {'Cliente':<15} {'Produto':<15} {'Quantidade':<10} {'Valor':<10} {'Data/Hora':<15}\n"
        self.consumo_display_area.insert("end", header)
        
        # Linha de separação
        separator = "-" * 70 + "\n"
        self.consumo_display_area.insert("end", separator)
        
        # Dados de exemplo para demonstração
        dados_exemplo = [
            {"id": 1, "cliente": "Mesa 01", "produto": "Refrigerante", "quantidade": 2, "valor": 8.00, "data": "28/03 14:30"},
            {"id": 2, "cliente": "Mesa 02", "produto": "Pizza", "quantidade": 1, "valor": 45.00, "data": "28/03 14:45"}
        ]
        
        # Preencher com dados de exemplo
        row_idx = 1
        for item in dados_exemplo:
            # Criar linha formatada com espaçamento uniforme
            linha = f"{item['id']:<5} {item['cliente']:<15} {item['produto']:<15} {item['quantidade']:<10} {f'R$ {item['valor']:.2f}':<10} {item['data']:<15}\n"
            
            # Inserir a linha no texto
            self.consumo_display_area.insert("end", linha)
            
            # Alternar cor de fundo para linhas pares e ímpares
            tag_name = f"row_{row_idx}"
            self.consumo_display_area.tag_add(tag_name, f"{row_idx+1}.0", f"{row_idx+2}.0")
            
            # Definir cores alternadas para linhas
            if row_idx % 2 == 0:
                self.consumo_display_area.tag_config(tag_name, background="#EFEFEF")
            else:
                self.consumo_display_area.tag_config(tag_name, background="#DFDFDF")
            
            row_idx += 1
            
        # Mensagem informativa
        if not dados_exemplo:
            self.consumo_display_area.insert("end", "Nenhum consumo registrado.\n")
        
        # Nota explicativa
        self.consumo_display_area.insert("end", "\nNota: Esta é uma visualização de exemplo. O registro de consumos será implementado em breve.\n")

    def adicionar_produto(self):
        nome = self.nome_entry.get().strip()
        preco = self.preco_entry.get().strip()
        quantidade = self.produtos_quantidade_entry.get().strip()

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
            preco = float(preco)
        except ValueError:
            self.display_area.insert("end", "Erro: Preço deve ser um número válido.\n")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            self.display_area.insert("end", "Erro: Quantidade deve ser um número inteiro válido.\n")
            return

        # Adicionar o produto e obter o código
        codigo = self.estoque.adicionar_produto(nome, preco, quantidade)
        
        # Mostrar o código gerado no campo de código
        self.codigo_entry.configure(state="normal")
        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, str(codigo))
        self.codigo_entry.configure(state="disabled")
        
        # Limpar os outros campos para facilitar a adição de um novo produto
        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.produtos_quantidade_entry.delete(0, "end")
        
        # Exibir mensagem de sucesso
        self.display_area.insert("end", f"Produto '{nome}' adicionado com sucesso! Código: {codigo}\n")
        
        # Salvar estoque automaticamente após adicionar
        self.estoque.salvar_estoque()

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
        quantidade = self.produtos_quantidade_entry.get()

        if not codigo:
            self.display_area.insert("end", "O campo Código deve ser preenchido para atualizar um produto.\n")
            return

        try:
            codigo = int(codigo)
            preco = float(preco) if preco else None
            quantidade = int(quantidade) if quantidade else None
            
            # Atualizar o produto no sistema
            self.estoque.atualizar_produto(codigo, nome, preco, quantidade)
            
            # Salvar as alterações no estoque
            self.estoque.salvar_estoque()
            
            # Criar uma mensagem informativa para ser exibida após a atualização da visualização
            mensagem = f"Produto com código {codigo} atualizado com sucesso!\n"
            
            # Atualizar a visualização (isso recria todos os widgets, incluindo a área de texto)
            self.exibir_estoque()
            
            # Após a atualização, mostrar a mensagem na nova área de texto
            if hasattr(self, 'display_area'):
                self.display_area.insert("end", mensagem)
                
        except ValueError:
            self.display_area.insert("end", "Erro: Código deve ser um número inteiro, Preço deve ser um número e Quantidade deve ser um inteiro.\n")
            
    def atualizar_produto_selecionado(self):
        """Abre um diálogo para atualizar os produtos selecionados na tabela."""
        # Verificar quais produtos estão selecionados
        produtos_selecionados = []
        
        for item_id, dados in self.selected_items.items():
            if dados["selected"]:
                produto_id = dados["produto_id"]
                produtos_selecionados.append(produto_id)
        
        if not produtos_selecionados:
            self.display_area.insert("end", "Nenhum produto selecionado para atualização.\n")
            return
            
        # Criar uma janela de diálogo para entrada de dados
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Atualizar Produtos")
        dialog.geometry("500x300")
        dialog.transient(self.window)  # Torna o diálogo modal
        dialog.grab_set()  # Impede interação com a janela principal
        dialog.resizable(False, False)  # Impede redimensionamento
        
        # Centralizar o diálogo na janela principal
        # Calcular posição x, y para centralizar
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        window_x = self.window.winfo_x()
        window_y = self.window.winfo_y()
        
        dialog_width = 500
        dialog_height = 300
        
        position_x = window_x + (window_width - dialog_width) // 2
        position_y = window_y + (window_height - dialog_height) // 2
        
        # Definir a geometria com a posição calculada
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_x}+{position_y}")
        
        # Adicionar widgets ao diálogo
        ctk.CTkLabel(dialog, text=f"Atualizando {len(produtos_selecionados)} produto(s)", font=("Arial", 16)).pack(pady=10)
        
        # Frame para os campos de entrada
        input_frame = ctk.CTkFrame(dialog)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Configurar o input_frame para ter duas colunas com pesos iguais
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=3)
        
        # Campos para atualização
        ctk.CTkLabel(input_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        nome_entry = ctk.CTkEntry(input_frame)
        nome_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(input_frame, text="Preço:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        preco_entry = ctk.CTkEntry(input_frame)
        preco_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(input_frame, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        quantidade_entry = ctk.CTkEntry(input_frame)
        quantidade_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Texto explicativo
        ctk.CTkLabel(dialog, text="Deixe em branco os campos que não deseja alterar", font=("Arial", 12)).pack(pady=5)
        
        # Função para processar a atualização
        def processar_atualizacao():
            nome = nome_entry.get() or None
            preco_str = preco_entry.get()
            quantidade_str = quantidade_entry.get()
            
            try:
                preco = float(preco_str) if preco_str else None
                quantidade = int(quantidade_str) if quantidade_str else None
                
                # Atualizar cada produto selecionado
                for produto_id in produtos_selecionados:
                    self.estoque.atualizar_produto(produto_id, nome, preco, quantidade)
                
                # Salvar as alterações
                self.estoque.salvar_estoque()
                
                # Fechar o diálogo
                dialog.destroy()
                
                # Atualizar a visualização
                self.exibir_estoque()
                
                # Mostrar mensagem de sucesso
                if hasattr(self, 'display_area'):
                    self.display_area.insert("end", f"{len(produtos_selecionados)} produto(s) atualizado(s) com sucesso: {', '.join(map(str, produtos_selecionados))}\n")
                
            except ValueError:
                error_label.configure(text="Erro: Preço deve ser um número e Quantidade deve ser um número inteiro")
        
        # Botões
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(button_frame, text="Atualizar", command=processar_atualizacao).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancelar", command=dialog.destroy).pack(side="left", padx=5)
        
        # Label para mensagens de erro
        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)
        
        # Ajuste para garantir que a centralização seja aplicada após a criação da janela
        # Este update assegura que o tamanho da janela principal seja corretamente medido
        self.window.update_idletasks()
        
        # Recalcular posição após o update
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        window_x = self.window.winfo_x()
        window_y = self.window.winfo_y()
        
        position_x = window_x + (window_width - dialog_width) // 2
        position_y = window_y + (window_height - dialog_height) // 2
        
        # Aplicar a geometria atualizada
        dialog.geometry(f"{dialog_width}x{dialog_height}+{position_x}+{position_y}")
        
        # Definir o foco no campo de nome
        nome_entry.focus_set()

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
        # Remover todos os widgets da aba de produtos para exibir uma nova visualização
        for widget in self.produtos_tab.winfo_children():
            widget.destroy()

        # Primeiro criar os frames de entrada e botões no topo
        self.setup_produtos_tab()
        
        # Agora remover apenas a área de texto (display_area) para colocar a tabela em seu lugar
        if hasattr(self, 'display_area'):
            self.display_area.destroy()
        
        # Criar um frame para a tabela na parte inferior
        tree_frame = ctk.CTkFrame(self.produtos_tab)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar o estilo do Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        
        # Criar o Treeview com barras de rolagem
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        # Adicionar coluna de seleção para a funcionalidade de checkbox
        tree = ttk.Treeview(tree_frame, 
                           columns=("Selecionar", "ID", "Nome", "Preço", "Quantidade", "Status"),
                           show="headings",
                           yscrollcommand=tree_scroll_y.set,
                           xscrollcommand=tree_scroll_x.set)
        
        # Configurar as colunas incluindo a nova coluna de seleção
        tree.heading("Selecionar", text="Selecionar")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Preço", text="Preço (R$)")
        tree.heading("Quantidade", text="Quantidade")
        tree.heading("Status", text="Status")
        
        tree.column("Selecionar", width=80, anchor="center")
        tree.column("ID", width=50)
        tree.column("Nome", width=150)
        tree.column("Preço", width=100)
        tree.column("Quantidade", width=100)
        tree.column("Status", width=100)
        
        # Adicionar dados do estoque com checkbox
        self.selected_items = {}  # Dicionário para armazenar o estado dos checkboxes
        
        for produto_id, produto_info in self.estoque.produtos.items():
            item_id = tree.insert("", "end", values=(
                "",  # Espaço para o checkbox
                produto_id,
                produto_info["nome"],
                f"{produto_info['preco']:.2f}",
                produto_info["quantidade"],
                produto_info["status"]
            ))
            # Armazenar o ID do produto associado ao ID do item na árvore
            self.selected_items[item_id] = {"selected": False, "produto_id": produto_id}
        
        tree.pack(fill="both", expand=True)
        
        # Armazenar referência à árvore para uso em outras funções
        self.tree = tree
        
        # Configurar o evento de clique para alternar a seleção
        tree.bind("<Button-1>", self.toggle_selection)
        
        # Conectar as barras de rolagem
        tree_scroll_y.configure(command=tree.yview)
        tree_scroll_x.configure(command=tree.xview)
        
        # Atualizar os botões para usar a seleção da árvore
        for widget in self.produtos_tab.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkButton):
                        if child.cget("text") == "Remover":
                            child.configure(command=self.remover_produto_selecionado)
                        elif child.cget("text") == "Reativar":
                            child.configure(command=self.reativar_produto_selecionado)
                        elif child.cget("text") == "Atualizar":
                            child.configure(command=self.atualizar_produto_selecionado)

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
            return
        
        # Cabeçalho formatado com espaçamento uniforme
        header = f"{'CÓDIGO':<10} {'NOME':<20} {'MESA/DOC':<15} {'TELEFONE':<15} {'STATUS':<10}\n"
        self.clientes_display_area.insert("end", header)
        self.clientes_display_area.tag_add("header", "1.0", "2.0")
        self.clientes_display_area.tag_config("header", foreground="#FFFFFF", background="#1F538D")
        
        # Linha de separação
        separator = "-" * 70 + "\n"
        self.clientes_display_area.insert("end", separator)
        
        # Preparar dados para exibição
        clientes_para_exibir = []
        for codigo, dados in self.clientes.clientes.items():
            clientes_para_exibir.append((codigo, dados))
        
        # Ordenar por código para melhor visualização
        clientes_para_exibir.sort(key=lambda x: x[0])
        
        # Preencher com dados
        linha_atual = 3  # Começa na linha 3 (após cabeçalho e separador)
        for i, (codigo, dados) in enumerate(clientes_para_exibir):
            # Criar linha formatada com espaçamento uniforme
            linha = f"{codigo:<10} {dados['nome']:<20} {dados['mesa']:<15} {dados.get('telefone', 'N/A'):<15} {dados['status']:<10}\n"
            
            # Inserir a linha no texto
            self.clientes_display_area.insert("end", linha)
            
            # Tag para colorir a linha inteira
            linha_tag = f"linha_{i}"
            
            # Adicionar tag à linha (do início ao fim da linha atual)
            self.clientes_display_area.tag_add(linha_tag, f"{linha_atual}.0", f"{linha_atual+1}.0")
            
            # Definir cores alternadas para linhas - Fundo escuro e letras claras
            if i % 2 == 0:
                self.clientes_display_area.tag_config(linha_tag, foreground="#FFFFFF", background="#2B2B2B")  # Escuro mais claro
            else:
                self.clientes_display_area.tag_config(linha_tag, foreground="#FFFFFF", background="#1E1E1E")  # Escuro mais escuro
            
            # Adicionar tag para colorir o status
            status_tag = f"status_{i}"
            line_count = float(self.clientes_display_area.index("end").split(".")[0])
            current_line = line_count - 1  # A linha atual é a última linha inserida
            
            # Calcular a posição inicial e final do texto do status na linha
            status_position = linha.rfind(dados['status'])
            if status_position != -1:
                start_pos = f"{current_line}.{status_position}"
                end_pos = f"{current_line}.{status_position + len(dados['status'])}"
                
                self.clientes_display_area.tag_add(status_tag, start_pos, end_pos)
                
                if dados['status'] == "ativo":
                    self.clientes_display_area.tag_config(status_tag, foreground="#008800")  # Verde para ativos
                else:
                    self.clientes_display_area.tag_config(status_tag, foreground="#FF0000")  # Vermelho para excluídos
            
            linha_atual += 1

    def salvar_e_sair(self):
        self.estoque.salvar_estoque()
        self.clientes.salvar_clientes()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

    def toggle_selection(self, event):
        # Identificar em qual linha o usuário clicou
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            
            # Verificar se o clique foi na coluna de seleção (coluna #1)
            if column == "#1" and row_id:
                # Inverter o estado de seleção
                if row_id in self.selected_items:
                    self.selected_items[row_id]["selected"] = not self.selected_items[row_id]["selected"]
                    
                    # Atualizar o marcador visual na interface
                    current_values = self.tree.item(row_id, "values")
                    if self.selected_items[row_id]["selected"]:
                        # Marcar com ✓ se selecionado
                        new_values = ("✓",) + current_values[1:]
                    else:
                        # Remover a marca se não selecionado
                        new_values = ("",) + current_values[1:]
                    
                    # Atualizar os valores na árvore
                    self.tree.item(row_id, values=new_values)
                    
                    # Atualizar mensagem na área de texto
                    if hasattr(self, 'display_area'):
                        produto_id = self.selected_items[row_id]["produto_id"]
                        if self.selected_items[row_id]["selected"]:
                            self.display_area.insert("end", f"Produto com código {produto_id} selecionado.\n")
                        else:
                            self.display_area.insert("end", f"Produto com código {produto_id} desmarcado.\n")

    def remover_produto_selecionado(self):
        """Remove todos os produtos selecionados na tabela."""
        produtos_removidos = 0
        produtos_ids = []  # Lista para armazenar todos os IDs dos produtos removidos
        
        for item_id, dados in self.selected_items.items():
            if dados["selected"]:
                produto_id = dados["produto_id"]
                self.estoque.remover_produto(produto_id)
                produtos_removidos += 1
                produtos_ids.append(produto_id)
        
        if produtos_removidos > 0:
            # Salvar as alterações no estoque
            self.estoque.salvar_estoque()
            
            # Criar uma área de texto temporária para manter as mensagens
            mensagens = f"{produtos_removidos} produto(s) marcado(s) como excluído(s): {', '.join(map(str, produtos_ids))}\n"
            
            # Atualizar a visualização (isso recria todos os widgets, incluindo a área de texto)
            self.exibir_estoque()
            
            # Após a atualização, mostrar as mensagens na nova área de texto
            if hasattr(self, 'display_area'):
                self.display_area.insert("end", mensagens)
        else:
            # Não é necessário atualizar a visualização se nenhum produto foi removido
            self.display_area.insert("end", "Nenhum produto selecionado para remoção.\n")

    def reativar_produto_selecionado(self):
        """Reativa todos os produtos selecionados na tabela."""
        produtos_reativados = 0
        produtos_ids = []  # Lista para armazenar todos os IDs dos produtos reativados
        
        for item_id, dados in self.selected_items.items():
            if dados["selected"]:
                produto_id = dados["produto_id"]
                self.estoque.reativar_produto(produto_id)
                produtos_reativados += 1
                produtos_ids.append(produto_id)
        
        if produtos_reativados > 0:
            # Salvar as alterações no estoque
            self.estoque.salvar_estoque()
            
            # Criar uma área de texto temporária para manter as mensagens
            mensagens = f"{produtos_reativados} produto(s) reativado(s): {', '.join(map(str, produtos_ids))}\n"
            
            # Atualizar a visualização (isso recria todos os widgets, incluindo a área de texto)
            self.exibir_estoque()
            
            # Após a atualização, mostrar as mensagens na nova área de texto
            if hasattr(self, 'display_area'):
                self.display_area.insert("end", mensagens)
        else:
            # Não é necessário atualizar a visualização se nenhum produto foi reativado
            self.display_area.insert("end", "Nenhum produto selecionado para reativação.\n")

    def preparar_atualizacao_selecionado(self):
        """Prepara a atualização do primeiro produto selecionado."""
        # Verificar se há algum produto selecionado
        produto_selecionado = None
        
        for item_id, dados in self.selected_items.items():
            if dados["selected"]:
                produto_selecionado = dados["produto_id"]
                break
        
        if produto_selecionado is None:
            self.display_area.insert("end", "Nenhum produto selecionado para atualização.\n")
            return
        
        # Carregar os dados do produto nos campos de entrada para edição
        produto_info = self.estoque.produtos.get(produto_selecionado)
        if produto_info:
            # Habilitar e preencher o campo de código
            self.codigo_entry.configure(state="normal")
            self.codigo_entry.delete(0, "end")
            self.codigo_entry.insert(0, str(produto_selecionado))
            
            # Preencher os outros campos com os valores atuais do produto
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, produto_info["nome"])
            
            self.preco_entry.delete(0, "end")
            self.preco_entry.insert(0, str(produto_info["preco"]))
            
            self.produtos_quantidade_entry.delete(0, "end")
            self.produtos_quantidade_entry.insert(0, str(produto_info["quantidade"]))
            
            # Instruções para o usuário
            self.display_area.insert("end", f"Editando produto com código {produto_selecionado}. Altere os campos desejados e clique em 'Atualizar'.\n")
            
            # Redefinir função do botão Atualizar para usar a função padrão de atualização
            for widget in self.produtos_tab.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkButton) and child.cget("text") == "Atualizar":
                            child.configure(command=self.atualizar_produto)

if __name__ == "__main__":
    app = EstoqueUI()
    app.run()