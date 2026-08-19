# Homura API — Endpoints

Documentação dos endpoints de consulta de cartas da Homura API.

---

# Autenticação

Todos os endpoints da API utilizam autenticação por API Key.

Enviar no header:

```http
Authorization: Bearer SUA_API_KEY
```

Respostas de autenticação:

| Código | Descrição      |
| ------ | -------------- |
| `401`  | Token ausente  |
| `403`  | Token inválido |

---

# Base URL

```text
https://homura-cards.vercel.app
```

---

# Endpoints

| Método | Endpoint                      | Descrição                   |
| ------ | ----------------------------- | --------------------------- |
| `GET`  | `/`                           | Informações da API          |
| `GET`  | `/api/{game}/cards`           | Lista e pesquisa cartas     |
| `GET`  | `/api/{game}/cards/{card_id}` | Busca uma carta por ID      |
| `GET`  | `/api/{game}/cards/lookup?q=` | Busca por nome ou ID        |
| `POST` | `/api/{game}/cards/bulk`      | Busca várias cartas por ID  |
| `GET`  | `/api/{game}/cards/random`    | Retorna uma carta aleatória |
| `GET`  | `/api/magic/cards`            | Consulta Magic via Scryfall |

---

# 1. Informações da API

## `GET /`

Retorna os metadados disponíveis através da configuração da API.

### Exemplo

```http
GET /
```

A estrutura exata da resposta depende do conteúdo retornado por `get_meta()`.

---

# 2. Listar e pesquisar cartas

## `GET /api/{game}/cards`

Endpoint principal para consulta de cartas.

O parâmetro `game` define qual coleção será consultada.

### Jogos disponíveis

| `game`               | Jogo                     |
| -------------------- | ------------------------ |
| `sorcery`            | Sorcery: Contested Realm |
| `pokemon`            | Pokémon                  |
| `digimon`            | Digimon                  |
| `dragon-ball-fusion` | Dragon Ball Fusion World |
| `one-piece`          | One Piece Card Game      |
| `riftbound`          | Riftbound                |
| `fab`                | Flesh and Blood          |
| `yugioh`             | Yu-Gi-Oh!                |
| `star-wars`          | Star Wars Unlimited      |
| `gundam`             | Gundam Card Game         |
| `union-arena`        | Union Arena              |
| `magic`              | Magic: The Gathering     |

Os jogos listados acima são os identificadores registrados atualmente no `GAME_CONFIG`.

---

## Parâmetros gerais

Todos os jogos MongoDB aceitam:

| Parâmetro | Tipo    | Padrão | Descrição                      |
| --------- | ------- | -----: | ------------------------------ |
| `page`    | integer |    `1` | Página                         |
| `limit`   | integer |   `25` | Quantidade de cartas           |
| `sort`    | string  |      — | Campo utilizado para ordenação |
| `order`   | string  |  `asc` | Ordem da ordenação             |

Exemplo:

```http
GET /api/one-piece/cards?page=1&limit=25
```

Ordenando:

```http
GET /api/one-piece/cards?sort=name&order=asc
```

---

# 3. Filtros por jogo

Os parâmetros abaixo são processados pelo filtro específico de cada coleção.

---

## One Piece

### Endpoint

```http
GET /api/one-piece/cards
```

### Filtros

| Parâmetro | Descrição       |
| --------- | --------------- |
| `id`      | ID da carta     |
| `code`    | Código da carta |
| `name`    | Nome            |
| `rarity`  | Raridade        |
| `type`    | Tipo            |
| `color`   | Cor             |
| `cost`    | Custo           |
| `power`   | Poder           |
| `family`  | Família         |
| `set`     | Código do set   |

Exemplos:

```http
GET /api/one-piece/cards?name=luffy
```

```http
GET /api/one-piece/cards?color=Red
```

```http
GET /api/one-piece/cards?set=OP01
```

```http
GET /api/one-piece/cards?name=luffy&color=Red
```

Os filtros `id`, `code`, `name`, `type` e `family` utilizam busca case-insensitive. `rarity`, `color`, `cost`, `power` e `set` utilizam comparação direta.

---

# Digimon

### Endpoint

```http
GET /api/digimon/cards
```

### Filtros

| Parâmetro | Descrição     |
| --------- | ------------- |
| `id`      | ID            |
| `code`    | Código        |
| `name`    | Nome          |
| `rarity`  | Raridade      |
| `type`    | Tipo          |
| `color`   | Cor           |
| `set`     | Código do set |

Exemplo:

```http
GET /api/digimon/cards?name=Agumon
```

```http
GET /api/digimon/cards?color=Red&rarity=R
```

---

# Pokémon

### Endpoint

```http
GET /api/pokemon/cards
```

### Filtros

| Parâmetro   | Descrição             |
| ----------- | --------------------- |
| `id`        | ID                    |
| `code`      | Código                |
| `name`      | Nome                  |
| `rarity`    | Raridade              |
| `type`      | Tipo                  |
| `set`       | Código do set         |
| `card_type` | Tipo da carta Pokémon |
| `stage`     | Estágio               |
| `artist`    | Artista               |

Exemplo:

```http
GET /api/pokemon/cards?name=Pikachu
```

```http
GET /api/pokemon/cards?stage=Basic
```

```http
GET /api/pokemon/cards?artist=Ken%20Sugimori
```

---

# Dragon Ball Fusion World

### Endpoint

```http
GET /api/dragon-ball-fusion/cards
```

### Filtros

| Parâmetro         | Descrição                     |
| ----------------- | ----------------------------- |
| `id`              | ID                            |
| `code`            | Código                        |
| `name`            | Nome                          |
| `rarity`          | Raridade                      |
| `type`            | Tipo                          |
| `color`           | Cor                           |
| `cost`            | Custo                         |
| `power`           | Poder                         |
| `characterTraits` | Características do personagem |
| `set`             | Código do set                 |

Exemplo:

```http
GET /api/dragon-ball-fusion/cards?name=Goku
```

```http
GET /api/dragon-ball-fusion/cards?color=Red&cost=3
```

---

# Sorcery

### Endpoint

```http
GET /api/sorcery/cards
```

### Filtros

| Parâmetro | Descrição              |
| --------- | ---------------------- |
| `name`    | Nome                   |
| `type`    | Tipo                   |
| `rarity`  | Raridade               |
| `element` | Elemento               |
| `subtype` | Subtipo                |
| `set`     | Set                    |
| `finish`  | Acabamento da variante |
| `product` | Produto da variante    |
| `artist`  | Artista                |

Exemplos:

```http
GET /api/sorcery/cards?name=Fire
```

```http
GET /api/sorcery/cards?element=Fire
```

```http
GET /api/sorcery/cards?finish=Foil
```

---

# Riftbound

### Endpoint

```http
GET /api/riftbound/cards
```

### Filtros

| Parâmetro    | Descrição        |
| ------------ | ---------------- |
| `name`       | Nome             |
| `rarity`     | Raridade         |
| `might`      | Might            |
| `energyCost` | Custo de energia |
| `powerCost`  | Custo de poder   |
| `cardType`   | Tipo da carta    |
| `domain`     | Domínio          |
| `set`        | Nome do set      |

Exemplo:

```http
GET /api/riftbound/cards?name=Jinx
```

```http
GET /api/riftbound/cards?domain=Chaos
```

---

# Flesh and Blood

### Endpoint

```http
GET /api/fab/cards
```

### Filtros

| Parâmetro | Descrição |
| --------- | --------- |
| `name`    | Nome      |
| `set`     | ID do set |

Exemplo:

```http
GET /api/fab/cards?name=Bravo
```

```http
GET /api/fab/cards?set=WTR
```

---

# Yu-Gi-Oh!

### Endpoint

```http
GET /api/yugioh/cards
```

### Filtros

| Parâmetro   | Descrição             |
| ----------- | --------------------- |
| `id`        | ID numérico           |
| `konami_id` | ID da Konami          |
| `effect`    | Texto/efeito da carta |
| `name`      | Nome                  |
| `attribute` | Atributo              |
| `type`      | Tipo                  |
| `frameType` | Tipo de frame         |
| `set`       | Código do set         |
| `rarity`    | Raridade              |

Exemplos:

```http
GET /api/yugioh/cards?name=Dark%20Magician
```

```http
GET /api/yugioh/cards?attribute=DARK
```

```http
GET /api/yugioh/cards?effect=draw
```

Os parâmetros `id` e `konami_id` são convertidos para inteiros antes da consulta.

---

# Star Wars Unlimited

### Endpoint

```http
GET /api/star-wars/cards
```

### Filtros

| Parâmetro | Descrição |
| --------- | --------- |
| `name`    | Nome      |
| `set`     | Set       |

Exemplo:

```http
GET /api/star-wars/cards?name=Luke
```

---

# Gundam

### Endpoint

```http
GET /api/gundam/cards
```

### Filtros

| Parâmetro | Descrição |
| --------- | --------- |
| `id`      | ID        |
| `code`    | Código    |
| `name`    | Nome      |
| `rarity`  | Raridade  |

Exemplo:

```http
GET /api/gundam/cards?name=Gundam
```

---

# Union Arena

### Endpoint

```http
GET /api/union-arena/cards
```

### Filtros

| Parâmetro | Descrição |
| --------- | --------- |
| `id`      | ID        |
| `code`    | Código    |
| `name`    | Nome      |
| `rarity`  | Raridade  |

Exemplo:

```http
GET /api/union-arena/cards?name=Goku
```

---

# 4. Buscar por ID

## `GET /api/{game}/cards/{card_id}`

Retorna uma carta específica.

### Exemplo

```http
GET /api/one-piece/cards/OP01-001
```

Se a carta existir:

```json
{
    "data": {
        "...": "..."
    }
}
```

Se não existir:

```json
{
    "detail": "Card não encontrado"
}
```

O endpoint retorna `404` quando o jogo não existe ou quando a carta não é encontrada.

---

# 5. Lookup

## `GET /api/{game}/cards/lookup?q={query}`

Permite pesquisar uma carta utilizando uma única string.

O endpoint tenta localizar a carta e retorna:

```json
{
    "data": {
        "...": "..."
    }
}
```

### Por nome

```http
GET /api/one-piece/cards/lookup?q=Luffy
```

### Por ID

```http
GET /api/one-piece/cards/lookup?q=OP01-001
```

Se nenhuma carta for encontrada:

```json
{
    "detail": "Card não encontrado"
}
```

---

# 6. Busca em lote

## `POST /api/{game}/cards/bulk`

Permite buscar várias cartas por ID em uma única requisição.

### Request

```http
POST /api/one-piece/cards/bulk
Content-Type: application/json
```

Body:

```json
{
    "ids": [
        "OP01-001",
        "OP01-002",
        "OP01-003"
    ]
}
```

### Response

```json
{
    "count": 3,
    "data": [
        {},
        {},
        {}
    ]
}
```

O campo `count` representa a quantidade de cartas encontradas.

IDs que não forem encontrados não aparecem em `data`.

---

# 7. Carta aleatória

## `GET /api/{game}/cards/random`

Retorna uma carta aleatória da coleção.

### Exemplo

```http
GET /api/one-piece/cards/random
```

### Response

```json
{
    "data": {
        "...": "..."
    }
}
```

---

# 8. Magic: The Gathering

Magic utiliza um endpoint separado:

```http
GET /api/magic/cards
```

A consulta é realizada através do Scryfall.

### Parâmetros

| Parâmetro  | Tipo    | Padrão |
| ---------- | ------- | ------ |
| `limit`    | integer | `25`   |
| `page`     | integer | `1`    |
| `name`     | string  | —      |
| `set`      | string  | —      |
| `colors`   | string  | —      |
| `rarity`   | string  | —      |
| `layout`   | string  | —      |
| `cmc`      | string  | —      |
| `language` | string  | —      |
| `id`       | string  | —      |

Esses são os parâmetros explicitamente recebidos pelo endpoint no `main.py`.

### Exemplo

```http
GET /api/magic/cards?name=Black%20Lotus
```

Com filtros:

```http
GET /api/magic/cards?set=lea&rarity=rare
```

Se houver uma falha HTTP na consulta ao Scryfall, a API retorna `502`.

---

# 9. Paginação

Os endpoints que retornam listas utilizam paginação.

### Exemplo

```http
GET /api/one-piece/cards?page=2&limit=50
```

A resposta possui:

```json
{
    "page": 2,
    "limit": 50,
    "total": 100,
    "totalPages": 2,
    "data": []
}
```

### Campos

| Campo        | Descrição             |
| ------------ | --------------------- |
| `page`       | Página atual          |
| `limit`      | Quantidade solicitada |
| `total`      | Total de resultados   |
| `totalPages` | Total de páginas      |
| `data`       | Cartas encontradas    |

A quantidade padrão é `25` cartas por página.

---

# 10. Ordenação

O endpoint de listagem aceita:

```text
sort
order
```

### Exemplo

```http
GET /api/one-piece/cards?sort=name&order=asc
```

Ou:

```http
GET /api/one-piece/cards?sort=name&order=desc
```

O valor padrão de `order` é:

```text
asc
```

---

# 11. Combinação de filtros

Os filtros podem ser combinados na mesma requisição.

Exemplo:

```http
GET /api/one-piece/cards?name=luffy&color=Red&rarity=SR&page=1&limit=25
```

A API transforma os parâmetros recebidos em uma consulta específica para a coleção correspondente.

Parâmetros que não fazem parte dos filtros definidos para aquele jogo são simplesmente ignorados pelo respectivo `filter_fn`.

---

# 12. Cache

Todas as respostas passam pelo middleware de cache da aplicação.

O header retornado é:

```http
Cache-Control: s-maxage=300, stale-while-revalidate=600
```

Isso permite que a infraestrutura da Vercel faça cache das respostas.

---

# 13. Exemplos de integração

## JavaScript

```javascript
const response = await fetch(
    "https://homura-cards.vercel.app/api/one-piece/cards?name=luffy",
    {
        headers: {
            Authorization: "Bearer SUA_API_KEY"
        }
    }
);

const result = await response.json();

console.log(result);
```

## Python

```python
import requests

response = requests.get(
    "https://homura-cards.vercel.app/api/one-piece/cards",
    headers={
        "Authorization": "Bearer SUA_API_KEY"
    },
    params={
        "name": "luffy",
        "limit": 25
    }
)

result = response.json()

print(result)
```

## cURL

```bash
curl \
  -H "Authorization: Bearer SUA_API_KEY" \
  "https://homura-cards.vercel.app/api/one-piece/cards?name=luffy"
```

---

# 14. Códigos HTTP

| Código | Significado                      |
| -----: | -------------------------------- |
|  `200` | Requisição realizada com sucesso |
|  `400` | Dados da requisição inválidos    |
|  `401` | Token ausente                    |
|  `403` | Token inválido                   |
|  `404` | Jogo ou carta não encontrada     |
|  `502` | Falha ao consultar o Scryfall    |
|  `422` | Erro de validação do FastAPI     |

---

# Observações

A API utiliza uma rota genérica para os jogos armazenados no MongoDB:

```text
/api/{game}/cards
```

Isso permite adicionar novos jogos sem criar uma nova rota específica para cada coleção.

Os filtros são definidos individualmente em `filters.py`, enquanto as consultas e a normalização dos documentos são realizadas por `mango.py`.

Magic possui tratamento separado porque utiliza o Scryfall como fonte de dados.
