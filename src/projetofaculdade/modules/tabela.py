from toga import Table
from toga.style import Pack

def criar_tabela():
    table = Table(
        headings=['Nome', 'Idade', 'Quantidade'],
        style=Pack(flex=1)
    )
    table.data.append(('Victor', 20, 5))
    table.data.append(('Hugo', 20, 2))
    return table
