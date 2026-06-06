import os
import sys

import Estoque
import Arquivos
from Produto import (
    Produto,
    validar_codigo,
    validar_nome,
    validar_categoria,
    validar_preco,
    validar_quantidade,
)

LIMITE_ESTOQUE_BAIXO_PADRAO = 5
ITENS_POR_PAGINA = 10
SEPARADOR = "─" * 54


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho(titulo: str) -> None:
    print(f"\n{SEPARADOR}")
    print(f"  {titulo}")
    print(SEPARADOR)


def pausar() -> None:
    input("\nPressione Enter para continuar...")


def ler_input(prompt: str, obrigatorio: bool = True) -> str:
    while True:
        valor = input(prompt).strip()
        if obrigatorio and not valor:
            print("  ⚠  Campo obrigatório. Tente novamente.")
            continue
        return valor


def paginar(lista: list, titulo_coluna: str = "") -> None:
    if not lista:
        print("  Nenhum Produto encontrado.")
        return
    total = len(lista)
    pagina = 0
    total_paginas = (total + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
    while True:
        inicio = pagina * ITENS_POR_PAGINA
        fim = min(inicio + ITENS_POR_PAGINA, total)
        print(f"\n{titulo_coluna}  (Página {pagina + 1}/{total_paginas}  |  {total} Produto(s))")
        print(f"{'CÓD':<12} {'NOME':<28} {'CATEGORIA':<15} {'PREÇO':>8} {'QTD':>5}")
        print("─" * 72)
        for p in lista[inicio:fim]:
            print(
                f"{p.codigo:<12} {p.nome[:28]:<28} {p.categoria[:15]:<15} "
                f"R${p.preco:>7.2f} {p.quantidade:>5}"
            )
        if total_paginas == 1:
            break
        nav = input("\n[P] Próxima  [A] Anterior  [Q] Sair  → ").strip().upper()
        if nav == "P" and pagina < total_paginas - 1:
            pagina += 1
        elif nav == "A" and pagina > 0:
            pagina -= 1
        elif nav == "Q":
            break


def acao_cadastrar_produto() -> None:
    cabecalho("CADASTRAR PRODUTO")
    while True:
        codigo = ler_input("  Código: ").upper()
        ok, msg = validar_codigo(codigo)
        if not ok:
            print(f"  ⚠  {msg}")
            continue
        if Estoque.buscar_por_codigo(codigo):
            print(f"  ⚠  Código '{codigo}' já cadastrado. Use outro.")
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
    Produto = Produto(codigo, nome, categoria, preco, quantidade)
    ok, msg = Estoque.cadastrar_produto(Produto)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"CADASTRO Produto '{codigo}' - {nome}")
        print(f"\n  ✔  Produto '{nome}' cadastrado com sucesso!")
    else:
        print(f"\n  ✖  {msg}")


def acao_editar_produto() -> None:
    cabecalho("EDITAR PRODUTO")
    codigo = ler_input("  Código do Produto: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if not Produto:
        print(f"  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto atual: {Produto.nome} | {Produto.categoria} | "
          f"R${Produto.preco:.2f} | Qtd: {Produto.quantidade}")
    print("  (Deixe em branco para manter o valor atual)\n")
    nome_novo = ler_input(f"  Novo nome [{Produto.nome}]: ", obrigatorio=False)
    categoria_nova = ler_input(f"  Nova categoria [{Produto.categoria}]: ", obrigatorio=False)
    preco_str = ler_input(f"  Novo preço [{Produto.preco:.2f}]: ", obrigatorio=False)
    qtd_str = ler_input(f"  Nova quantidade [{Produto.quantidade}]: ", obrigatorio=False)
    preco_novo = None
    if preco_str:
        ok, msg, preco_novo = validar_preco(preco_str)
        if not ok:
            print(f"  ⚠  {msg} Preço não alterado.")
            preco_novo = None
    qtd_nova = None
    if qtd_str:
        ok, msg, qtd_nova = validar_quantidade(qtd_str)
        if not ok:
            print(f"  ⚠  {msg} Quantidade não alterada.")
            qtd_nova = None
    ok, msg = Estoque.editar_produto(
        codigo,
        nome=nome_novo or None,
        categoria=categoria_nova or None,
        preco=preco_novo,
        quantidade=qtd_nova,
    )
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"EDIÇÃO Produto '{codigo}'")
        print("\n  ✔  Produto atualizado com sucesso!")
    else:
        print(f"\n  ✖  {msg}")


def acao_remover_produto() -> None:
    cabecalho("REMOVER PRODUTO")
    codigo = ler_input("  Código do Produto: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if not Produto:
        print(f"  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto: {Produto.nome} | {Produto.categoria} | R${Produto.preco:.2f}")
    confirmar = ler_input("  Confirmar remoção? (s/n): ").lower()
    if confirmar != "s":
        print("  Operação cancelada.")
        return
    ok, msg = Estoque.remover_produto(codigo)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"REMOÇÃO Produto '{codigo}'")
        print("\n  ✔  Produto removido com sucesso!")
    else:
        print(f"\n  ✖  {msg}")


def acao_buscar_por_codigo() -> None:
    cabecalho("BUSCAR POR CÓDIGO")
    codigo = ler_input("  Código: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if Produto:
        print(f"\n  ✔  Encontrado:")
        print(f"     Código    : {Produto.codigo}")
        print(f"     Nome      : {Produto.nome}")
        print(f"     Categoria : {Produto.categoria}")
        print(f"     Preço     : R${Produto.preco:.2f}")
        print(f"     Quantidade: {Produto.quantidade}")
    else:
        print(f"\n  ✖  Produto '{codigo}' não encontrado.")


def acao_buscar_por_nome() -> None:
    cabecalho("BUSCAR POR NOME")
    termo = ler_input("  Termo de busca: ")
    resultados = Estoque.buscar_por_nome(termo)
    if resultados:
        print(f"\n  {len(resultados)} Produto(s) encontrado(s):")
        paginar(resultados)
    else:
        print(f"  Nenhum Produto encontrado para '{termo}'.")


def acao_registrar_venda() -> None:
    cabecalho("REGISTRAR VENDA")
    codigo = ler_input("  Código do Produto: ").upper()
    Produto = Estoque.buscar_por_codigo(codigo)
    if not Produto:
        print(f"  ✖  Produto '{codigo}' não encontrado.")
        return
    print(f"\n  Produto: {Produto.nome}  |  Estoque atual: {Produto.quantidade}")
    while True:
        qtd_str = ler_input("  Quantidade vendida: ")
        ok, msg, quantidade = validar_quantidade(qtd_str)
        if ok:
            break
        print(f"  ⚠  {msg}")
    ok, msg = Estoque.registrar_venda(codigo, quantidade)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"VENDA Produto '{codigo}' - {quantidade} unidade(s) vendida(s)")
        Produto = Estoque.buscar_por_codigo(codigo)
        print(f"\n  ✔  Venda registrada! Estoque restante: {Produto.quantidade}")
    else:
        print(f"\n  ✖  {msg}")


def acao_listar_por_codigo() -> None:
    cabecalho("PRODUTOS ORDENADOS POR CÓDIGO")
    paginar(Estoque.produtos_ordenados_por_codigo(), "Listagem por código →")


def acao_listar_por_categoria() -> None:
    cabecalho("LISTAR POR CATEGORIA")
    cats = Estoque.categorias_disponiveis()
    if not cats:
        print("  Nenhuma categoria cadastrada.")
        return
    print("  Categorias disponíveis:")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")
    categoria = ler_input("\n  Digite a categoria: ")
    resultados = Estoque.listar_por_categoria(categoria)
    if resultados:
        paginar(resultados, f"Categoria: {categoria} →")
    else:
        print(f"  Nenhum Produto na categoria '{categoria}'.")


def acao_relatorio_estoque_baixo() -> None:
    cabecalho("RELATÓRIO DE ESTOQUE BAIXO")
    limite_str = ler_input(
        f"  Limite de quantidade (padrão {LIMITE_ESTOQUE_BAIXO_PADRAO}): ",
        obrigatorio=False,
    )
    if limite_str:
        ok, msg, limite = validar_quantidade(limite_str)
        if not ok:
            print(f"  ⚠  {msg} Usando padrão ({LIMITE_ESTOQUE_BAIXO_PADRAO}).")
            limite = LIMITE_ESTOQUE_BAIXO_PADRAO
    else:
        limite = LIMITE_ESTOQUE_BAIXO_PADRAO
    produtos = Estoque.relatorio_estoque_baixo(limite)
    if produtos:
        print(f"\n  ⚠  {len(produtos)} Produto(s) com Estoque abaixo de {limite}:")
        paginar(produtos, f"Estoque baixo (< {limite}) →")
    else:
        print(f"\n  ✔  Nenhum Produto com Estoque abaixo de {limite}.")


MENU_OPCOES = [
    ("1", "Cadastrar Produto",                  acao_cadastrar_produto),
    ("2", "Editar Produto",                     acao_editar_produto),
    ("3", "Remover Produto",                    acao_remover_produto),
    ("4", "Buscar por código (bin. O(log n))",  acao_buscar_por_codigo),
    ("5", "Buscar por nome (linear O(n))",      acao_buscar_por_nome),
    ("6", "Registrar venda",                    acao_registrar_venda),
    ("7", "Listar por código (ordenado)",       acao_listar_por_codigo),
    ("8", "Listar por categoria",               acao_listar_por_categoria),
    ("9", "Relatório de Estoque baixo",         acao_relatorio_estoque_baixo),
    ("0", "Sair",                               None),
]


def exibir_menu() -> None:
    limpar_tela()
    print(f"\n{'═' * 54}")
    print("   📦  SISTEMA DE ESTOQUE E VENDAS")
    print(f"{'═' * 54}")
    for opcao, descricao, _ in MENU_OPCOES:
        print(f"  [{opcao}] {descricao}")
    print(f"{'═' * 54}")


def main() -> None:
    produtos_carregados = Arquivos.carregar_dados()
    Estoque.inicializar(produtos_carregados)
    print(f"  ✔  {len(produtos_carregados)} Produto(s) carregado(s).")
    mapa = {opcao: func for opcao, _, func in MENU_OPCOES}
    while True:
        exibir_menu()
        escolha = input("  Escolha uma opção: ").strip()
        if escolha not in mapa:
            print("  ⚠  Opção inválida.")
            pausar()
            continue
        if escolha == "0":
            print("\n  Até logo! 👋\n")
            sys.exit(0)
        mapa[escolha]()
        pausar()


if __name__ == "__main__":
    main()