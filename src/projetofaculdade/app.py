import toga
from toga import App, Box, TextInput, Button, Label, Table, MainWindow
from toga.style import Pack
from toga.style.pack import COLUMN

from modules.tabela import criar_tabela
from modules.botoes import criar_botao_adicionar, criar_botao_editar, criar_botao_remover
from modules.bd import listar_clientes, novo_cliente, excluir_cliente, clientes


class ProjetoFaculdade(App):
    def startup(self):
        # Cria a janela principal
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.max_size = (600, 400)
        self.main_window.content = self.pagina_inicio()
        self.main_window.show()

    def pagina_inicio(self):
        self.main_window.size = (600, 400)
        caixa_principal = Box(style=Pack(direction=COLUMN, padding=10))

        # Cria a tabela com os clientes
        self.tabela = Table(
            headings=['ID', 'Nome', 'Idade', 'Quantidade'],
            style=Pack(flex=1)
        )

        # Popula a tabela com os clientes
        listar_clientes()
        for cliente in clientes:
            self.tabela.data.append((
                cliente['_id'],
                cliente['nome'],
                cliente['idade'],
                cliente['quantidade']
            ))

        # Adiciona a tabela e os botões na interface principal
        caixa_principal.add(self.tabela)
        caixa_principal.add(criar_botao_adicionar(self.abrir_tela_adicionar_cliente))
        caixa_principal.add(criar_botao_remover(self.remover_cliente))
        caixa_principal.add(criar_botao_editar(self.abrir_tela_adicionar_cliente))

        return caixa_principal

    def remover_cliente(self, widget):
        selecionado = self.tabela.selection
        if selecionado:
            excluir_cliente(selecionado.id)
            self.voltar_inicio()
        else:
            print("Nenhum item selecionado.")

    def abrir_tela_adicionar_cliente(self, widget):
        # Cria a tela para adicionar clientes
        self.caixa_adicionar_cliente = Box(style=Pack(direction=COLUMN, padding=10))

        self.nome_input = TextInput(placeholder="Nome", style=Pack(flex=1, padding_bottom=10))
        self.idade_input = TextInput(placeholder="Idade", style=Pack(flex=1, padding_bottom=10))
        self.quantidade_input = TextInput(placeholder="Quantidade", style=Pack(flex=1, padding_bottom=10))

        botao_adicionar = Button("Adicionar", on_press=self.adicionar_cliente, style=Pack(flex=1, padding=10))
        botao_cancelar = Button("Cancelar", on_press=self.voltar_inicio, style=Pack(flex=1, padding=10))

        caixa_inputs = Box(style=Pack(direction=COLUMN, padding=10))
        caixa_inputs.add(self.nome_input)
        caixa_inputs.add(self.idade_input)
        caixa_inputs.add(self.quantidade_input)
        caixa_inputs.add(botao_adicionar)
        caixa_inputs.add(botao_cancelar)

        self.caixa_adicionar_cliente.add(Label("Adicionar Novo Cliente", style=Pack(padding_bottom=10, font_size=20)))
        self.caixa_adicionar_cliente.add(caixa_inputs)

        # Substitui o conteúdo da janela principal pela tela de adição
        self.main_window.content = self.caixa_adicionar_cliente
        self.main_window.size = (300, 300)

    def adicionar_cliente(self, widget):
        nome = self.nome_input.value
        try:
            idade = int(self.idade_input.value)
            quantidade = int(self.quantidade_input.value)
        except ValueError:
            self.main_window.error_dialog("Dados incorretos!", "Idade e Quantidade devem ser números inteiros.")
            return

        novo_cliente(nome, idade, quantidade)
        self.voltar_inicio()

    def voltar_inicio(self, widget=None):
        # Volta para a tela principal
        self.main_window.content = self.pagina_inicio()


def main():
    return ProjetoFaculdade()
