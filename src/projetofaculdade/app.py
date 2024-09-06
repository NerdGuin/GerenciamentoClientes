import toga
from toga import App, Box, TextInput, Button, Label, Table, MainWindow
from toga.style import Pack
from toga.style.pack import COLUMN

from modules.tabela import criar_tabela
from modules.botoes import criar_botao_adicionar, criar_botao_editar, criar_botao_remover
from modules.bd import listar_clientes, novo_cliente, excluir_cliente, clientes


class ProjetoFaculdade(App):
    def voltar_inicio(self, widget=None):
        # Volta para a tela principal
        self.main_window.content = self.pagina_inicio()

    def startup(self):
        # Cria a janela principal
        self.main_window = MainWindow(title="Gerenciamento de Clientes")
        self.main_window.max_size = (600, 400)
        self.main_window.content = self.pagina_inicio()
        self.main_window.show()

    def pagina_inicio(self):
        self.main_window.size = (600, 400)
        caixa_principal = Box(style=Pack(direction=COLUMN, padding=10))

        # Cria a tabela com os clientes
        self.tabela = Table(
            headings=['ID', 'Nome', 'Telefone', 'Endereço', 'Vendas'],
            style=Pack(flex=1)
        )

        # Popula a tabela com os clientes
        listar_clientes()
        for cliente in clientes:
            self.tabela.data.append((
                cliente['_id'],
                cliente['nome'],
                cliente['telefone'],
                cliente['end'],
                cliente['vendas']
            ))

        # Adiciona a tabela e os botões na interface principal
        caixa_principal.add(self.tabela)
        caixa_principal.add(criar_botao_adicionar(self.abrir_tela_adicionar_cliente))
        caixa_principal.add(criar_botao_remover(self.remover_cliente))
        caixa_principal.add(criar_botao_editar(self.abrir_tela_editar_cliente))

        return caixa_principal

    def remover_cliente(self, widget):
        selecionado = self.tabela.selection
        if selecionado:
            excluir_cliente(selecionado.id)  # ID está na posição 0
            self.voltar_inicio()
        else:
            self.main_window.error_dialog("Nenhum cliente selecionado", "Selecione um cliente para removê-lo.")

    def abrir_tela_adicionar_cliente(self, widget):
        # Cria a tela para adicionar clientes
        caixa_adicionar_cliente = Box(style=Pack(direction=COLUMN, padding=10))

        nome_input = TextInput(placeholder="Nome", style=Pack(flex=1, padding_bottom=10))
        telefone_input = TextInput(placeholder="Telefone", style=Pack(flex=1, padding_bottom=10))
        endereco_input = TextInput(placeholder="Endereço", style=Pack(flex=1, padding_bottom=10))
        quantidade_input = TextInput(placeholder="Vendas", style=Pack(flex=1, padding_bottom=10))

        botao_adicionar = Button("Adicionar", on_press=self.adicionar_cliente, style=Pack(flex=1, padding=10))
        botao_cancelar = Button("Cancelar", on_press=self.voltar_inicio, style=Pack(flex=1, padding=10))

        caixa_inputs = Box(style=Pack(direction=COLUMN, padding=10))
        caixa_inputs.add(nome_input)
        caixa_inputs.add(telefone_input)
        caixa_inputs.add(endereco_input)
        caixa_inputs.add(quantidade_input)
        caixa_inputs.add(botao_adicionar)
        caixa_inputs.add(botao_cancelar)

        caixa_adicionar_cliente.add(Label("ADICIONAR NOVO CLIENTE", style=Pack(padding_bottom=10, font_size=20)))
        caixa_adicionar_cliente.add(caixa_inputs)

        # Armazena os campos de entrada como atributos da instância
        self.nome_input = nome_input
        self.telefone_input = telefone_input
        self.endereco_input = endereco_input
        self.quantidade_input = quantidade_input

        # Substitui o conteúdo da janela principal pela tela de adição
        self.main_window.content = caixa_adicionar_cliente
        self.main_window.size = (300, 300)

    def adicionar_cliente(self, widget):
        nome = self.nome_input.value
        endereco = self.endereco_input.value
        telefone = self.telefone_input.value
        try:
            vendas = int(self.quantidade_input.value)
        except ValueError:
            self.main_window.error_dialog("Dados incorretos!", "Quantidade deve ser um número inteiro.")
            return

        novo_cliente(0, nome, telefone, endereco, vendas)  # ID é 0 para novo cliente
        self.voltar_inicio()

    def abrir_tela_editar_cliente(self, widget):
        selecionado = self.tabela.selection
        if selecionado:
            # Cria a tela para editar clientes
            self.caixa_editar_cliente = Box(style=Pack(direction=COLUMN, padding=10))

            id_input = TextInput(value=selecionado.id, placeholder="ID", style=Pack(flex=1, padding_bottom=10), readonly=True)
            nome_input = TextInput(value=selecionado.nome, placeholder="Nome", style=Pack(flex=1, padding_bottom=10))
            telefone_input = TextInput(value=selecionado.telefone, placeholder="Telefone", style=Pack(flex=1, padding_bottom=10))
            endereco_input = TextInput(value=selecionado.endereço, placeholder="Endereço", style=Pack(flex=1, padding_bottom=10))
            quantidade_input = TextInput(value=str(selecionado.vendas), placeholder="Vendas", style=Pack(flex=1, padding_bottom=10))

            botao_editar = Button("Salvar", on_press=self.salvar_edicao, style=Pack(flex=1, padding=10))
            botao_cancelar = Button("Cancelar", on_press=self.voltar_inicio, style=Pack(flex=1, padding=10))

            caixa_inputs = Box(style=Pack(direction=COLUMN, padding=10))
            caixa_inputs.add(id_input)
            caixa_inputs.add(nome_input)
            caixa_inputs.add(telefone_input)
            caixa_inputs.add(endereco_input)
            caixa_inputs.add(quantidade_input)
            caixa_inputs.add(botao_editar)
            caixa_inputs.add(botao_cancelar)

            self.caixa_editar_cliente.add(Label("EDITAR CLIENTE", style=Pack(padding_bottom=10, font_size=20)))
            self.caixa_editar_cliente.add(caixa_inputs)

            # Armazena os campos de entrada como atributos da instância
            self.id_input = id_input
            self.nome_input = nome_input
            self.telefone_input = telefone_input
            self.endereco_input = endereco_input
            self.quantidade_input = quantidade_input

            # Substitui o conteúdo da janela principal pela tela de edição
            self.main_window.content = self.caixa_editar_cliente
            self.main_window.size = (300, 300)
        else:
            self.main_window.error_dialog("Nenhum cliente selecionado", "Selecione um cliente para editá-lo.")

    def salvar_edicao(self, widget):
        id = self.id_input.value
        nome = self.nome_input.value
        telefone = self.telefone_input.value
        endereco = self.endereco_input.value
        try:
            vendas = int(self.quantidade_input.value)
        except ValueError:
            self.main_window.error_dialog("Dados incorretos!", "Quantidade deve ser um número inteiro.")
            return

        # Atualizar o cliente com o ID correspondente
        novo_cliente(id, nome, telefone, endereco, vendas)  # Atualiza o cliente existente
        self.voltar_inicio()


def main():
    return ProjetoFaculdade()
