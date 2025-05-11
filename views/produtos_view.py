import customtkinter as ctk

class ProdutosView:
    def __init__(self, parent_tab, controller):
        self.parent_tab = parent_tab
        self.controller = controller

        # Input Frame
        input_frame = ctk.CTkFrame(self.parent_tab)
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

        # Button Frame
        button_frame = ctk.CTkFrame(self.parent_tab)
        button_frame.pack(padx=20, pady=10)

        self.adicionar_button = ctk.CTkButton(button_frame, text="Adicionar")
        self.adicionar_button.pack(side="left", padx=5)
        self.remover_button = ctk.CTkButton(button_frame, text="Remover")
        self.remover_button.pack(side="left", padx=5)
        self.atualizar_button = ctk.CTkButton(button_frame, text="Atualizar")
        self.atualizar_button.pack(side="left", padx=5)
        self.reativar_button = ctk.CTkButton(button_frame, text="Reativar")
        self.reativar_button.pack(side="left", padx=5)
        self.exibir_button = ctk.CTkButton(button_frame, text="Exibir Estoque")
        self.exibir_button.pack(side="left", padx=5)

        # Status Label
        self.product_status_label = ctk.CTkLabel(self.parent_tab, text="", height=1, anchor="w")
        self.product_status_label.pack(padx=20, pady=(5, 0), fill="x")

        # Products Table Frame
        self.products_table_frame = ctk.CTkScrollableFrame(self.parent_tab, height=300)
        self.products_table_frame.pack(padx=20, pady=10, fill="both", expand=True)

    def get_codigo_entry(self):
        return self.codigo_entry.get().strip()

    def get_nome_entry(self):
        return self.nome_entry.get().strip()

    def get_preco_entry(self):
        return self.preco_entry.get().strip()

    def get_quantidade_entry(self):
        return self.produto_quantidade_entry.get().strip()

    def set_button_commands(self):
        if self.controller:
            self.adicionar_button.configure(command=self.controller.adicionar_produto)
            self.remover_button.configure(command=self.controller.remover_produto)
            self.atualizar_button.configure(command=self.controller.atualizar_produto)
            self.reativar_button.configure(command=self.controller.reativar_produto)
            self.exibir_button.configure(command=self.controller.exibir_estoque)
        else:
            # Handle the case where controller is still None, perhaps log an error or disable buttons
            print("Error: Controller not set in ProdutosView when trying to set button commands.")
            self.adicionar_button.configure(state="disabled")
            self.remover_button.configure(state="disabled")
            self.atualizar_button.configure(state="disabled")
            self.reativar_button.configure(state="disabled")
            self.exibir_button.configure(state="disabled")


    def set_status_message(self, message):
        self.product_status_label.configure(text=message)

    def clear_input_fields(self):
        self.codigo_entry.delete(0, "end")
        self.nome_entry.delete(0, "end")
        self.preco_entry.delete(0, "end")
        self.produto_quantidade_entry.delete(0, "end")

    def display_estoque(self, produtos_data):
        # Clear previous widgets in the frame
        for widget in self.products_table_frame.winfo_children():
            widget.destroy()

        headers = ["Ativo", "Código", "Nome", "Preço (R$)", "Quantidade"]
        column_widths = [0.1, 0.1, 0.3, 0.15, 0.15]

        for col, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(self.products_table_frame, text=header_text, font=ctk.CTkFont(weight="bold"), anchor="center")
            header_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        for i, weight in enumerate(column_widths):
             self.products_table_frame.grid_columnconfigure(i, weight=int(weight*100))

        if not produtos_data:
            no_data_label = ctk.CTkLabel(self.products_table_frame, text="Estoque vazio.")
            no_data_label.grid(row=1, column=0, columnspan=len(headers), padx=5, pady=10, sticky="nsew")
            self.set_status_message("Estoque vazio.")
        else:
            row_num = 1
            # produtos_data is expected to be a dictionary {codigo: dados_produto}
            # Sort by code
            sorted_codigos = sorted(produtos_data.keys())

            for codigo in sorted_codigos:
                dados = produtos_data[codigo]
                
                status_checkbox = ctk.CTkCheckBox(
                    self.products_table_frame,
                    text="", 
                    onvalue="ativo", offvalue="excluido",
                    command=lambda c=codigo: self.controller.toggle_produto_status(c)
                )
                if dados['status'] == 'ativo':
                    status_checkbox.select()
                else:
                    status_checkbox.deselect()
                status_checkbox.grid(row=row_num, column=0, padx=5, pady=2, sticky="nsew")

                data_to_display = [
                    codigo,
                    dados['nome'],
                    f"{dados['preco']:.2f}",
                    dados['quantidade']
                ]
                for i, item_data in enumerate(data_to_display):
                    item_label = ctk.CTkLabel(self.products_table_frame, text=str(item_data), anchor="center")
                    item_label.grid(row=row_num, column=i + 1, padx=5, pady=2, sticky="nsew")
                
                row_num += 1
            self.set_status_message(f"{len(produtos_data)} produtos exibidos.")
