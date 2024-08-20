import toga
from toga.style import Pack

def criar_botao_adicionar(handler):
    botao = toga.Button(
        "ADICIONAR CLIENTE",
        on_press=handler,
        style=Pack(padding=2, height=40)
    )
    return botao

def criar_botao_editar(handler):
    botao = toga.Button(
        "EDITAR CLIENTE",
        on_press=handler,
        style=Pack(padding=2, height=40)
    )
    return botao

def criar_botao_remover(handler):
    botao = toga.Button(
        "REMOVER CLIENTE",
        on_press=handler,
        style=Pack(padding=2, height=40)
    )
    return botao
