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


def ler_input(prompt, obrigatorio=True):
    while True:
        valor = input(prompt).strip()
        if obrigatorio and not valor:
            print("  ⚠  Campo obrigatório. Tente novamente.")
            continue
        return valor


def cabecalho(titulo):
    print(f"\n{SEPARADOR}\n  {titulo}\n{SEPARADOR}")


def acao_cadastrar_produto():
    cabecalho("CADASTRAR PRODUTO")
    while True:
        codigo = ler_input("  Código: ").upper()
        ok, msg = validar_codigo(codigo)
        if not ok:
            print(f"  ⚠  {msg}")
            continue
        if Estoque.buscar_por_codigo(codigo):
            print(f"  ⚠  Código '{codigo}' já cadastrado.")
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
        preco_str = ler_input("  Preço (ex: 19.90): ")
        ok, msg, preco = validar_preco(preco_str)
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        qtd_str = ler_input("  Quantidade inicial: ")
        ok, msg, quantidade = validar_quantidade(qtd_str)
        if ok:
            break
        print(f"  ⚠  {msg}")
    produto = Produto(codigo, nome, categoria, preco, quantidade)
    ok, msg = Estoque.cadastrar_produto(produto)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"CADASTRO produto '{codigo}'")
        print(f"\n  ✔  Produto '{nome}' cadastrado!")
    else:
        print(f"\n  ✖  {msg}")


def acao_editar_produto():
    cabecalho("EDITAR PRODUTO")
    codigo = ler_input("  Código: ").upper()
    produto = Estoque.buscar_por_codigo(codigo)
    if not produto:
        print(f"  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Atual: {produto.nome} | {produto.categoria} | R${produto.preco:.2f} | Qtd: {produto.quantidade}")
    print("  (Deixe em branco para manter)\n")
    nome_novo = ler_input(f"  Novo nome [{produto.nome}]: ", obrigatorio=False)
    cat_nova  = ler_input(f"  Nova categoria [{produto.categoria}]: ", obrigatorio=False)
    preco_str = ler_input(f"  Novo preço [{produto.preco:.2f}]: ", obrigatorio=False)
    qtd_str   = ler_input(f"  Nova quantidade [{produto.quantidade}]: ", obrigatorio=False)
    preco_novo = None
    if preco_str:
        ok, msg, preco_novo = validar_preco(preco_str)
        if not ok:
            print(f"  ⚠  {msg}")
            preco_novo = None
    qtd_nova = None
    if qtd_str:
        ok, msg, qtd_nova = validar_quantidade(qtd_str)
        if not ok:
            print(f"  ⚠  {msg}")
            qtd_nova = None
    ok, msg = Estoque.editar_produto(codigo, nome=nome_novo or None,
                                     categoria=cat_nova or None,
                                     preco=preco_novo, quantidade=qtd_nova)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"EDIÇÃO produto '{codigo}'")
        print("\n  ✔  Produto atualizado!")
    else:
        print(f"\n  ✖  {msg}")


MENU = [
    ("1", "Cadastrar produto", acao_cadastrar_produto),
    ("2", "Editar produto",    acao_editar_produto),
    ("0", "Sair",              None),
]


def main():
    produtos = Arquivos.carregar_dados()
    Estoque.inicializar(produtos)
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