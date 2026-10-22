from pathlib import Path
from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, HttpUrl, field_validator

app = FastAPI(
    title="Catalogo de Produtos SENAI",
    description=(
        "API para consultar e gerenciar produtos. Os itens incluem descricao, "
        "caracteristicas, sabor, cores, preco, imagem e data de vencimento. "
        "A listagem retorna os produtos ordenados pelo menor preco. As datas "
        "devem usar o formato ISO (AAAA-MM-DD)."
    ),
    version="1.0.0",
)

produtos = {
    1: {
        "descricao": "Maca",
        "caracteristicas": "Polpa firme e rica em fibras.",
        "sabor": "Doce com leve acidez.",
        "cores": ["Vermelho", "Verde"],
        "preco": 2.50,
        "data_vencimento": date(2026, 10, 29),
        "imagem": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=900&q=85",
    },
    2: {
        "descricao": "Abacate",
        "caracteristicas": "Polpa cremosa e fonte de gorduras boas.",
        "sabor": "Suave e amanteigado.",
        "cores": ["Verde"],
        "preco": 6.00,
        "data_vencimento": date(2026, 10, 25),
        "imagem": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=900&q=85",
    },
    3: {
        "descricao": "Melancia",
        "caracteristicas": "Fruta hidratante, com polpa suculenta.",
        "sabor": "Doce e refrescante.",
        "cores": ["Verde", "Vermelho"],
        "preco": 4.50,
        "data_vencimento": date(2026, 10, 30),
        "imagem": "https://images.unsplash.com/photo-1587049352851-8d4e89133924?auto=format&fit=crop&w=900&q=85",
    },
    4: {
        "descricao": "Kiwi",
        "caracteristicas": "Polpa macia e pequena quantidade de sementes.",
        "sabor": "Agridoce e refrescante.",
        "cores": ["Marrom", "Verde"],
        "preco": 1.80,
        "data_vencimento": date(2026, 10, 26),
        "imagem": "https://images.unsplash.com/photo-1585059895524-72359e06133a?auto=format&fit=crop&w=900&q=85",
    },
    5: {
        "descricao": "Abacaxi",
        "caracteristicas": "Polpa fibrosa e aroma tropical.",
        "sabor": "Doce com acidez marcante.",
        "cores": ["Amarelo", "Verde"],
        "preco": 5.00,
        "data_vencimento": date(2026, 11, 2),
        "imagem": "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=900&q=85",
    },
}
proximo_id = 6


class ProdutoEntrada(BaseModel):
    descricao: str = Field(min_length=1, max_length=100, description="Nome do produto.")
    caracteristicas: str = Field(min_length=1, max_length=250, description="Caracteristicas do produto.")
    sabor: str = Field(min_length=1, max_length=120, description="Perfil de sabor.")
    cores: list[str] = Field(min_length=1, max_length=5, description="Uma a cinco cores do produto.")
    preco: float = Field(gt=0, le=1000000, description="Preco em reais, maior que zero.")
    data_vencimento: date = Field(description="Data de validade no formato AAAA-MM-DD.")
    imagem: HttpUrl = Field(description="URL HTTP ou HTTPS da imagem do produto.")

    @field_validator("descricao", "caracteristicas", "sabor")
    @classmethod
    def limpar_texto(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O campo nao pode ficar vazio.")
        return valor

    @field_validator("cores")
    @classmethod
    def limpar_cores(cls, cores: list[str]) -> list[str]:
        cores = [cor.strip() for cor in cores if cor.strip()]
        if not cores:
            raise ValueError("Informe ao menos uma cor.")
        return cores


class ProdutoResposta(BaseModel):
    id: int
    descricao: str
    caracteristicas: str
    sabor: str
    cores: list[str]
    preco: float
    data_vencimento: date
    imagem: HttpUrl


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get(
    "/produtos",
    response_model=list[ProdutoResposta],
    tags=["Produtos"],
    summary="Listar produtos",
    description="Retorna todos os produtos em ordem crescente de preco.",
)
def listar_produtos():
    return [
        {"id": produto_id, **produto}
        for produto_id, produto in sorted(
            produtos.items(), key=lambda item: (item[1]["preco"], item[0])
        )
    ]


@app.get(
    "/produtos/{produto_id}",
    response_model=ProdutoResposta,
    tags=["Produtos"],
    summary="Buscar produto por ID",
    description="Retorna os detalhes de um produto. Retorna 404 se o ID nao existir.",
    responses={404: {"description": "Produto nao encontrado."}},
)
def buscar_produto(produto_id: int):
    if produto_id not in produtos:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")

    return {"id": produto_id, **produtos[produto_id]}


@app.post(
    "/produtos",
    response_model=ProdutoResposta,
    status_code=201,
    tags=["Produtos"],
    summary="Cadastrar produto",
    description="Cadastra um produto. Todos os campos de ProdutoEntrada sao obrigatorios.",
)
def criar_produto(novo_produto: ProdutoEntrada):
    global proximo_id
    produto_id = proximo_id
    proximo_id += 1
    produtos[produto_id] = novo_produto.model_dump()
    return {"id": produto_id, **produtos[produto_id]}


@app.put(
    "/produtos/{produto_id}",
    response_model=ProdutoResposta,
    tags=["Produtos"],
    summary="Atualizar produto",
    description="Substitui todos os campos de um produto existente. Retorna 404 se o ID nao existir.",
    responses={404: {"description": "Produto nao encontrado."}},
)
def atualizar_produto(produto_id: int, produto_atualizado: ProdutoEntrada):
    if produto_id not in produtos:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")

    produtos[produto_id] = produto_atualizado.model_dump()
    return {"id": produto_id, **produtos[produto_id]}


@app.delete(
    "/produtos/{produto_id}",
    tags=["Produtos"],
    summary="Excluir produto",
    description="Remove um produto pelo ID. Retorna 404 se o ID nao existir.",
    responses={404: {"description": "Produto nao encontrado."}},
)
def deletar_produto(produto_id: int):
    if produto_id not in produtos:
        raise HTTPException(status_code=404, detail="Produto nao encontrado.")

    descricao = produtos.pop(produto_id)["descricao"]
    return {"mensagem": f"O produto {descricao} foi removido com sucesso."}