class Produto:
    def __init__(self, codigo: str, nome: str, categoria: str,
                 preco: float, quantidade: int):
        self.codigo = codigo.strip().upper()
        self.nome = nome.strip()
        self.categoria = categoria.strip()
        self.preco = preco
        self.quantidade = quantidade

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
        }

    @staticmethod
    def from_dict(data: dict) -> "Produto":
        return Produto(
            codigo=data["codigo"],
            nome=data["nome"],
            categoria=data["categoria"],
            preco=float(data["preco"]),
            quantidade=int(data["quantidade"]),
        )

    def __repr__(self) -> str:
        return (
            f"Produto(codigo={self.codigo!r}, nome={self.nome!r}, "
            f"categoria={self.categoria!r}, preco={self.preco:.2f}, "
            f"quantidade={self.quantidade})"
        )


def validar_codigo(codigo: str) -> tuple[bool, str]:
    codigo = codigo.strip()
    if not codigo:
        return False, "O código não pode ser vazio."
    if len(codigo) > 20:
        return False, "O código deve ter no máximo 20 caracteres."
    return True, ""


def validar_nome(nome: str) -> tuple[bool, str]:
    nome = nome.strip()
    if not nome:
        return False, "O nome não pode ser vazio."
    if len(nome) > 100:
        return False, "O nome deve ter no máximo 100 caracteres."
    return True, ""


def validar_categoria(categoria: str) -> tuple[bool, str]:
    categoria = categoria.strip()
    if not categoria:
        return False, "A categoria não pode ser vazia."
    return True, ""


def validar_preco(preco_str: str) -> tuple[bool, str, float]:
    try:
        preco = float(preco_str.replace(",", "."))
    except ValueError:
        return False, "Preço inválido. Use um número (ex: 19.90).", 0.0
    if preco <= 0:
        return False, "O preço deve ser maior que zero.", 0.0
    return True, "", preco


def validar_quantidade(qtd_str: str) -> tuple[bool, str, int]:
    try:
        qtd = int(qtd_str)
    except ValueError:
        return False, "Quantidade inválida. Use um número inteiro.", 0
    if qtd < 0:
        return False, "A quantidade não pode ser negativa.", 0
    return True, "", qtd