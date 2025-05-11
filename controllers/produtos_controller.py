class ProdutosController:
    def __init__(self, model_estoque, view_produtos, main_ui_instance):
        self.model_estoque = model_estoque
        self.view = view_produtos
        self.main_ui = main_ui_instance  # To call methods like update_consumo_comboboxes

    def adicionar_produto(self):
        nome = self.view.get_nome_entry()
        preco_str = self.view.get_preco_entry()
        quantidade_str = self.view.get_quantidade_entry()

        if not nome:
            self.view.set_status_message("Erro: O campo Nome está vazio.")
            return
        if not preco_str:
            self.view.set_status_message("Erro: O campo Preço está vazio.")
            return
        if not quantidade_str:
            self.view.set_status_message("Erro: O campo Quantidade está vazio.")
            return

        try:
            preco = float(preco_str.replace(',', '.'))
        except ValueError:
            self.view.set_status_message("Erro: Preço deve ser um número válido.")
            return

        try:
            quantidade = int(quantidade_str)
        except ValueError:
            self.view.set_status_message("Erro: Quantidade deve ser um número inteiro válido.")
            return

        codigo = self.model_estoque.adicionar_produto(nome, preco, quantidade)
        self.view.set_status_message(f"Produto {nome} adicionado com sucesso! Código: {codigo}")
        self.main_ui.update_consumo_comboboxes()
        self.exibir_estoque()
        self.view.clear_input_fields()

    def remover_produto(self):
        codigo_str = self.view.get_codigo_entry()

        if not codigo_str:
            self.view.set_status_message("O campo Código deve ser preenchido para remover um produto.")
            return

        try:
            codigo = int(codigo_str)
            self.model_estoque.remover_produto(codigo)
            self.view.set_status_message(f"Produto com código {codigo} marcado como excluído.")
            self.main_ui.update_consumo_comboboxes()
            self.exibir_estoque()
            self.view.clear_input_fields()
        except ValueError:
            self.view.set_status_message("Erro: Código deve ser um número inteiro.")
        except KeyError:
            self.view.set_status_message(f"Erro: Produto com código {codigo_str} não encontrado.")


    def atualizar_produto(self):
        codigo_str = self.view.get_codigo_entry()
        nome = self.view.get_nome_entry() or None
        preco_str = self.view.get_preco_entry()
        quantidade_str = self.view.get_quantidade_entry()

        if not codigo_str:
            self.view.set_status_message("O campo Código deve ser preenchido para atualizar um produto.")
            return

        try:
            codigo = int(codigo_str)
            preco = None
            if preco_str:
                preco = float(preco_str.replace(',', '.'))
            
            quantidade = None
            if quantidade_str:
                quantidade = int(quantidade_str)
                
            self.model_estoque.atualizar_produto(codigo, nome, preco, quantidade)
            self.view.set_status_message(f"Produto com código {codigo} atualizado com sucesso!")
            self.main_ui.update_consumo_comboboxes()
            self.exibir_estoque()
            self.view.clear_input_fields()
        except ValueError:
            self.view.set_status_message("Erro: Código deve ser int, Preço float, Quantidade int.")
        except KeyError:
            self.view.set_status_message(f"Erro: Produto com código {codigo_str} não encontrado.")

    def reativar_produto(self):
        codigo_str = self.view.get_codigo_entry()

        if not codigo_str:
            self.view.set_status_message("O campo Código deve ser preenchido para reativar um produto.")
            return

        try:
            codigo = int(codigo_str)
            self.model_estoque.reativar_produto(codigo)
            self.view.set_status_message(f"Produto com código {codigo} reativado com sucesso!")
            self.main_ui.update_consumo_comboboxes()
            self.exibir_estoque()
            self.view.clear_input_fields()
        except ValueError:
            self.view.set_status_message("Erro: Código deve ser um número inteiro.")
        except KeyError:
            self.view.set_status_message(f"Erro: Produto com código {codigo_str} não encontrado.")

    def exibir_estoque(self):
        # The model_estoque.produtos is expected to be a dictionary {codigo: dados_produto}
        produtos_data = self.model_estoque.produtos
        self.view.display_estoque(produtos_data)

    def toggle_produto_status(self, product_code):
        # Ensure product_code is the correct type (likely int, as keys in Estoque model)
        try:
            code_key = int(product_code)
        except ValueError:
            self.view.set_status_message(f"Erro: Código de produto inválido {product_code}.")
            return

        produto = self.model_estoque.produtos.get(code_key)
        
        if not produto:
            # Attempt to find by string key if int key fails (though model uses int keys)
            produto_str_key = self.model_estoque.produtos.get(str(product_code))
            if not produto_str_key:
                self.view.set_status_message(f"Erro: Produto com código {product_code} não encontrado.")
                return
            produto = produto_str_key # Use the found product
            code_key = str(product_code) # Use the string key for operations if that's how it was found


        if produto['status'] == 'ativo':
            self.model_estoque.remover_produto(code_key)
            self.view.set_status_message(f"Produto {code_key} marcado como inativo.")
        else:  # 'excluido'
            self.model_estoque.reativar_produto(code_key)
            self.view.set_status_message(f"Produto {code_key} reativado.")
        
        self.exibir_estoque()
        self.main_ui.update_consumo_comboboxes()
