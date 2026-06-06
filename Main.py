import sys
import os
import Estoque
import Arquivos
from Produto import (Produto, validar_codigo, validar_nome,
                     validar_categoria, validar_preco, validar_quantidade)

SEPARADOR = "─" * 54


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para continuar...")


def cabecalho(titulo):
    print(f"\n{SEPARADOR}\n  {titulo}\n{SEPARADOR}")


def ler_input(prompt, obrigatorio=True):
    while True:
        valor = input(prompt).strip()
        if obrigatorio and not valor:
            print("  ⚠  Campo obrigatório. Tente novamente.")
            continue
        return valor


def acao_cadastrar_produto():
    cabecalho("CADASTRAR PRODUTO")
    while True:
        codigo = ler_input("  Código: ").upper()
        ok, msg = validar_codigo(codigo)
        if not ok:
            print(f"  ⚠  {msg}")
            continue
        if Estoque.buscar_por_codigo(codigo):
            print("  ⚠  Código já existe.")
            continue
        break
    while True:
        nome = ler_input("  Nome: ")
        ok, msg = validar_nome(nome)
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        categoria = ler_input("  Categoria: ")
        ok, msg = validar_categoria(categoria)
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        ok, msg, preco = validar_preco(ler_input("  Preço: "))
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        ok, msg, quantidade = validar_quantidade(ler_input("  Quantidade: "))
        if ok:
            break
        print(f"  ⚠  {msg}")
    Produto = Produto(codigo, nome, categoria, preco, quantidade)
    ok, msg = Estoque.cadastrar_produto(Produto)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"CADASTRO '{codigo}'")
        print(f"\n  ✔  Produto '{nome}' cadastrado!")
    else:
        print(f"\n  ✖  {msg}")


def acao_editar_produto():
    cabecalho("EDITAR PRODUTO")
    codigo = ler_input("  Código: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if not Produto:
        print(f"  ✖  Não encontrado.")
        return
    print(f"\n  Atual: {Produto.nome} | {Produto.categoria} | R${Produto.preco:.2f} | Qtd: {Produto.quantidade}")
    nome_novo = ler_input(f"  Novo nome [{Produto.nome}]: ", obrigatorio=False)
    cat_nova  = ler_input(f"  Nova categoria [{Produto.categoria}]: ", obrigatorio=False)
    preco_str = ler_input(f"  Novo preço [{Produto.preco:.2f}]: ", obrigatorio=False)
    qtd_str   = ler_input(f"  Nova quantidade [{Produto.quantidade}]: ", obrigatorio=False)
    preco_novo = None
    if preco_str:
        ok, msg, preco_novo = validar_preco(preco_str)
        if not ok:
            preco_novo = None
    qtd_nova = None
    if qtd_str:
        ok, msg, qtd_nova = validar_quantidade(qtd_str)
        if not ok:
            qtd_nova = None
    ok, msg = Estoque.editar_produto(codigo, nome=nome_novo or None,
                                     categoria=cat_nova or None,
                                     preco=preco_novo, quantidade=qtd_nova)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"EDIÇÃO '{codigo}'")
        print("\n  ✔  Atualizado!")
    else:
        print(f"\n  ✖  {msg}")


def acao_remover_produto():
    cabecalho("REMOVER PRODUTO")
    codigo = ler_input("  Código: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if not Produto:
        print(f"  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto: {Produto.nome} | R${Produto.preco:.2f} | Qtd: {Produto.quantidade}")
    if ler_input("  Confirmar remoção? (s/n): ").lower() != "s":
        print("  Cancelado.")
        return
    ok, msg = Estoque.remover_produto(codigo)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"REMOÇÃO '{codigo}'")
        print("\n  ✔  Produto removido!")
    else:
        print(f"\n  ✖  {msg}")


def acao_buscar_por_codigo():
    cabecalho("BUSCAR POR CÓDIGO")
    codigo = ler_input("  Código: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if Produto:
        print(f"\n  ✔  Código: {Produto.codigo} | Nome: {Produto.nome}")
        print(f"     Categoria: {Produto.categoria} | Preço: R${Produto.preco:.2f} | Qtd: {Produto.quantidade}")
    else:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")


MENU = [
    ("1", "Cadastrar Produto",               acao_cadastrar_produto),
    ("2", "Editar Produto",                  acao_editar_produto),
    ("3", "Remover Produto",                 acao_remover_produto),
    ("4", "Buscar por código (bin. O(log n))", acao_buscar_por_codigo),
    ("0", "Sair",                            None),
]


def main():
    Estoque.inicializar(Arquivos.carregar_dados())
    while True:
        limpar_tela()
        print("\n" + "═" * 54)
        print("   📦  SISTEMA DE ESTOQUE E VENDAS")
        print("═" * 54)
        for op, desc, _ in MENU:
            print(f"  [{op}] {desc}")
        print("═" * 54)
        escolha = input("  Opção: ").strip()
        mapa = {op: fn for op, _, fn in MENU}
        if escolha not in mapa:
            print("  ⚠  Inválido.")
            pausar()
            continue
        if escolha == "0":
            print("\n  Até logo! 👋\n")
            sys.exit(0)
        mapa[escolha]()
        pausar()


if __name__ == "__main__":
    main()