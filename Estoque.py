import bisect
from Produto import Produto


_vetor_nao_ordenado: list[Produto] = []
_vetor_ordenado: list[Produto] = []


def _codigos_ordenados() -> list[str]:
    return [p.codigo for p in _vetor_ordenado]


def inicializar(produtos: list[Produto]) -> None:
    global _vetor_nao_ordenado, _vetor_ordenado
    _vetor_nao_ordenado = list(produtos)
    _vetor_ordenado = sorted(produtos, key=lambda p: p.codigo)


def todos_os_produtos() -> list[Produto]:
    return list(_vetor_nao_ordenado)


def produtos_ordenados_por_codigo() -> list[Produto]:
    return list(_vetor_ordenado)


def cadastrar_produto(produto: Produto) -> tuple[bool, str]:
    if _busca_binaria_indice(produto.codigo) is not None:
        return False, f"Produto com código '{produto.codigo}' já existe."
    _vetor_nao_ordenado.append(produto)
    bisect.insort(_vetor_ordenado, produto, key=lambda p: p.codigo)
    return True, ""


def editar_produto(codigo: str, nome: str | None, categoria: str | None,
                   preco: float | None, quantidade: int | None
                   ) -> tuple[bool, str]:
    produto = buscar_por_codigo(codigo)
    if produto is None:
        return False, f"Produto '{codigo}' não encontrado."
    if nome is not None:
        produto.nome = nome.strip()
    if categoria is not None:
        produto.categoria = categoria.strip()
    if preco is not None:
        produto.preco = preco
    if quantidade is not None:
        produto.quantidade = quantidade
    return True, ""


def remover_produto(codigo: str) -> tuple[bool, str]:
    codigo = codigo.strip().upper()
    idx_nao_ord = next(
        (i for i, p in enumerate(_vetor_nao_ordenado) if p.codigo == codigo),
        None
    )
    if idx_nao_ord is None:
        return False, f"Produto '{codigo}' não encontrado."
    _vetor_nao_ordenado.pop(idx_nao_ord)
    idx_ord = _busca_binaria_indice(codigo)
    if idx_ord is not None:
        _vetor_ordenado.pop(idx_ord)
    return True, ""


def buscar_por_codigo(codigo: str) -> Produto | None:
    idx = _busca_binaria_indice(codigo.strip().upper())
    return _vetor_ordenado[idx] if idx is not None else None


def _busca_binaria_indice(codigo: str) -> int | None:
    codigos = _codigos_ordenados()
    pos = bisect.bisect_left(codigos, codigo)
    if pos < len(_vetor_ordenado) and _vetor_ordenado[pos].codigo == codigo:
        return pos
    return None


def buscar_por_nome(termo: str) -> list[Produto]:
    termo = termo.strip().lower()
    return [p for p in _vetor_nao_ordenado if termo in p.nome.lower()]


def registrar_venda(codigo: str, quantidade: int) -> tuple[bool, str]:
    produto = buscar_por_codigo(codigo)
    if produto is None:
        return False, f"Produto '{codigo}' não encontrado."
    if quantidade <= 0:
        return False, "A quantidade vendida deve ser maior que zero."
    if produto.quantidade < quantidade:
        return False, f"Estoque insuficiente. Disponível: {produto.quantidade} unidade(s)."
    produto.quantidade -= quantidade
    return True, ""


def listar_por_categoria(categoria: str) -> list[Produto]:
    categoria = categoria.strip().lower()
    return [p for p in _vetor_nao_ordenado if p.categoria.lower() == categoria]


def relatorio_estoque_baixo(limite: int) -> list[Produto]:
    return [p for p in _vetor_nao_ordenado if p.quantidade < limite]


def categorias_disponiveis() -> list[str]:
    return sorted({p.categoria for p in _vetor_nao_ordenado})