import sys
import os
import Estoque
import Arquivos
from Produto import (Produto, validar_codigo, validar_nome,
                     validar_categoria, validar_preco, validar_quantidade)

SEPARADOR = "─" * 54
ITENS_POR_PAGINA = 10


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para continuar...")


def cabecalho(titulo):
    print(f"\n{SEPARADOR}\n  {titulo}\n{SEPARADOR}")


def ler_input(prompt, obrigatorio=True):
    while True:
        v = input(prompt).strip()
        if obrigatorio and not v:
            print("  ⚠  Obrigatório.")
            continue
        return v


def paginar(lista, titulo=""):
    if not lista:
        print("  Nenhum Produto.")
        return
    total = len(lista)
    pagina = 0
    total_pags = (total + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA
    while True:
        ini = pagina * ITENS_POR_PAGINA
        fim = min(ini + ITENS_POR_PAGINA, total)
        print(f"\n{titulo}  (Pág {pagina + 1}/{total_pags}  |  {total} Produto(s))")
        print(f"{'CÓD':<12} {'NOME':<28} {'CATEGORIA':<15} {'PREÇO':>8} {'QTD':>5}")
        print("─" * 72)
        for p in lista[ini:fim]:
            print(f"{p.codigo:<12} {p.nome[:28]:<28} {p.categoria[:15]:<15} R${p.preco:>7.2f} {p.quantidade:>5}")
        if total_pags == 1:
            break
        nav = input("\n[P] Próxima  [A] Anterior  [Q] Sair → ").strip().upper()
        if nav == "P" and pagina < total_pags - 1:
            pagina += 1
        elif nav == "A" and pagina > 0:
            pagina -= 1
        elif nav == "Q":
            break


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
        cat = ler_input("  Categoria: ")
        ok, msg = validar_categoria(cat)
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        ok, msg, preco = validar_preco(ler_input("  Preço: "))
        if ok:
            break
        print(f"  ⚠  {msg}")
    while True:
        ok, msg, qtd = validar_quantidade(ler_input("  Quantidade: "))
        if ok:
            break
        print(f"  ⚠  {msg}")
    ok, msg = Estoque.cadastrar_produto(Produto(codigo, nome, cat, preco, qtd))
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"CADASTRO '{codigo}'")
        print(f"\n  ✔  Produto '{nome}' cadastrado!")
    else:
        print(f"\n  ✖  {msg}")


def acao_editar_produto():
    cabecalho("EDITAR PRODUTO")
    codigo = ler_input("  Código: ").upper()
    p = Estoque.buscar_por_codigo(codigo)
    if not p:
        print(f"  ✖  Não encontrado.")
        return
    nome_novo = ler_input(f"  Nome [{p.nome}]: ", obrigatorio=False)
    cat_nova  = ler_input(f"  Categoria [{p.categoria}]: ", obrigatorio=False)
    preco_str = ler_input(f"  Preço [{p.preco:.2f}]: ", obrigatorio=False)
    qtd_str   = ler_input(f"  Quantidade [{p.quantidade}]: ", obrigatorio=False)
    preco_novo = None
    if preco_str:
        ok, _, preco_novo = validar_preco(preco_str)
        if not ok:
            preco_novo = None
    qtd_nova = None
    if qtd_str:
        ok, _, qtd_nova = validar_quantidade(qtd_str)
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
    p = Estoque.buscar_por_codigo(codigo)
    if not p:
        print(f"  ✖  Não encontrado.")
        return
    print(f"\n  Produto: {p.nome} | R${p.preco:.2f}")
    if ler_input("  Confirmar? (s/n): ").lower() != "s":
        print("  Cancelado.")
        return
    ok, msg = Estoque.remover_produto(codigo)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"REMOÇÃO '{codigo}'")
        print("\n  ✔  Removido!")
    else:
        print(f"\n  ✖  {msg}")


def acao_buscar_por_codigo():
    cabecalho("BUSCAR POR CÓDIGO")
    codigo = ler_input("  Código: ").upper()
    p = Estoque.buscar_por_codigo(codigo)
    if p:
        print(f"\n  ✔  {p.codigo} | {p.nome} | {p.categoria} | R${p.preco:.2f} | Qtd: {p.quantidade}")
    else:
        print(f"\n  ✖  Não encontrado.")


def acao_buscar_por_nome():
    cabecalho("BUSCAR POR NOME")
    termo = ler_input("  Termo: ")
    res = Estoque.buscar_por_nome(termo)
    if res:
        paginar(res, f"Resultados para '{termo}' →")
    else:
        print(f"  Nenhum Produto encontrado.")


def acao_registrar_venda():
    cabecalho("REGISTRAR VENDA")
    codigo = ler_input("  Código: ").upper()
    p = Estoque.buscar_por_codigo(codigo)
    if not p:
        print(f"  ✖  Não encontrado.")
        return
    print(f"\n  Produto: {p.nome}  |  Estoque: {p.quantidade}")
    while True:
        ok, msg, qtd = validar_quantidade(ler_input("  Quantidade: "))
        if ok:
            break
        print(f"  ⚠  {msg}")
    ok, msg = Estoque.registrar_venda(codigo, qtd)
    if ok:
        Arquivos.salvar_dados(Estoque.todos_os_produtos())
        Arquivos.registrar_log(f"VENDA '{codigo}' - {qtd} un.")
        p2 = Estoque.buscar_por_codigo(codigo)
        print(f"\n  ✔  Venda registrada! Restante: {p2.quantidade}")
    else:
        print(f"\n  ✖  {msg}")


def acao_listar_por_codigo():
    cabecalho("PRODUTOS ORDENADOS POR CÓDIGO")
    paginar(Estoque.produtos_ordenados_por_codigo(), "Listagem por código →")


def acao_listar_por_categoria():
    cabecalho("LISTAR POR CATEGORIA")
    cats = Estoque.categorias_disponiveis()
    if not cats:
        print("  Nenhuma categoria.")
        return
    print("  Categorias:")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")
    cat = ler_input("\n  Categoria: ")
    res = Estoque.listar_por_categoria(cat)
    if res:
        paginar(res, f"Categoria: {cat} →")
    else:
        print(f"  Nenhum Produto na categoria '{cat}'.")


MENU = [
    ("1", "Cadastrar Produto",                 acao_cadastrar_produto),
    ("2", "Editar Produto",                    acao_editar_produto),
    ("3", "Remover Produto",                   acao_remover_produto),
    ("4", "Buscar por código (bin. O(log n))", acao_buscar_por_codigo),
    ("5", "Buscar por nome (linear O(n))",     acao_buscar_por_nome),
    ("6", "Registrar venda",                   acao_registrar_venda),
    ("7", "Listar por código (ordenado)",      acao_listar_por_codigo),
    ("8", "Listar por categoria",              acao_listar_por_categoria),
    ("0", "Sair",                              None),
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