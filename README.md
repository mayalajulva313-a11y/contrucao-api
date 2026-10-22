# Catalogo de Produtos

API REST e interface web para consultar e gerenciar produtos. O catalogo inclui imagem, caracteristicas, sabor, cores, preco e data de vencimento.
![](https://github.com/mayalajulva313-a11y/contrucao-api/blob/main/Screenshots/tela%206.png)
![](https://github.com/mayalajulva313-a11y/contrucao-api/blob/main/Screenshots/tela%205.png)
![](https://github.com/mayalajulva313-a11y/contrucao-api/blob/main/Screenshots/tela%204.png)
![](https://github.com/mayalajulva313-a11y/contrucao-api/blob/main/Screenshots/tela%203.png)
![](https://github.com/mayalajulva313-a11y/contrucao-api/blob/main/Screenshots/tela%202.png)

## Executar

Instale as dependencias e inicie a aplicacao:

```bash
python -m pip install "fastapi>=0.100" "uvicorn[standard]"
uvicorn app:app --reload
```

Abra `http://localhost:8000` para usar a interface ou `http://localhost:8000/docs` para explorar a API pelo Swagger.

## Interface

- **Buscar produtos**: filtra por nome, sabor, caracteristicas, cor, ID ou vencimento. A tabela e ordenada pelo menor preco.
- **Cadastrar produto**: cria produtos com todos os campos obrigatorios.
- **Editar** e **Excluir**: acoes disponiveis na tabela.
- **Vencimento**: sinaliza produtos vencidos e os que vencem nos proximos sete dias.

## Endpoints

| Metodo | Caminho | Funcao |
| --- | --- | --- |
| `GET` | `/produtos` | Lista os produtos em ordem crescente de preco. |
| `GET` | `/produtos/{produto_id}` | Busca um produto pelo ID. |
| `POST` | `/produtos` | Cadastra um produto e retorna HTTP 201. |
| `PUT` | `/produtos/{produto_id}` | Substitui todos os dados de um produto existente. |
| `DELETE` | `/produtos/{produto_id}` | Exclui um produto existente. |

Produtos inexistentes retornam HTTP 404. Dados invalidos ou campos obrigatorios ausentes retornam HTTP 422.

### Exemplo de cadastro

Envie todos os campos abaixo no corpo JSON de `POST /produtos` ou `PUT /produtos/{produto_id}`. A data deve usar o formato ISO `AAAA-MM-DD`, o preco deve ser maior que zero e `imagem` deve ser uma URL HTTP ou HTTPS valida.

```json
{
  "descricao": "Pera",
  "caracteristicas": "Polpa macia e suculenta.",
  "sabor": "Doce.",
  "cores": ["Verde", "Amarela"],
  "preco": 3.25,
  "data_vencimento": "2026-11-10",
  "imagem": "https://example.com/pera.jpg"
}
```

Exemplo para listar os produtos:

```bash
curl http://localhost:8000/produtos
```

## Dados de exemplo

O catalogo inicial contem maca, abacate, melancia, kiwi e abacaxi. Os precos e vencimentos iniciais sao ilustrativos; substitua-os pelos dados reais dos produtos ou lotes.

Os dados sao guardados em memoria e reiniciam com a aplicacao. Para uso permanente, conecte a API a um banco de dados.
