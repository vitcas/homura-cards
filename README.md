# Homura API

> API unificada para consulta de cartas de Trading Card Games (TCGs).

A Homura API é uma API desenvolvida em **FastAPI** cujo objetivo é disponibilizar uma interface única para consulta de cartas de diversos jogos, independentemente da origem dos dados.

Atualmente a API é capaz de consumir informações provenientes de:

- MongoDB próprio (coleções normalizadas)
- Scryfall (Magic: The Gathering)
- APIs terceiras (APITCG)

Toda essa complexidade fica transparente para quem consome a API.

---

# Objetivo

A Homura nasceu para resolver um problema simples:

Cada TCG possui uma estrutura de dados diferente.

Ao invés de obrigar cada aplicação a entender o formato de cada jogo, a Homura centraliza essa responsabilidade e entrega um formato consistente para todos eles.

Dessa forma aplicações como **Cardumy** precisam conhecer apenas a Homura.

---

# Tecnologias

- Python
- FastAPI
- MongoDB
- PyMongo
- Requests
- python-dotenv

---

# Jogos suportados

## MongoDB (Homura)

- One Piece Card Game
- Sorcery Contested Realm
- Riftbound
- Flesh and Blood
- Yu-Gi-Oh!
- Star Wars Unlimited
- Gundam Card Game
- Union Arena

## Scryfall

- Magic: The Gathering

## APITCG

- Pokémon
- Digimon
- Dragon Ball Fusion World

---

# Arquitetura

A aplicação possui uma arquitetura simples e modular.

```
Cliente
    │
    ▼
 FastAPI (main.py)
    │
    ├──────────────┐
    │              │
    ▼              ▼
security.py     magic.py
    │
    ▼
filters.py
    │
    ▼
mango.py
    │
    ▼
MongoDB
```

Cada módulo possui apenas uma responsabilidade.

---

# Estrutura do projeto

```
api/

├── main.py
├── security.py
├── filters.py
├── mango.py
└── magic.py
```

---

# Responsabilidade dos módulos

## main.py

É o ponto de entrada da API.

Responsável por:

- iniciar o FastAPI
- configurar CORS
- registrar rotas
- escolher o provider correto
- controlar paginação
- retornar as respostas

Não contém regras específicas de nenhum jogo.

---

## security.py

Responsável pela autenticação.

Toda requisição deve enviar:

```
Authorization: Bearer SUA_API_KEY
```

Caso a chave seja inválida:

- 401 → Token ausente
- 403 → Token inválido

---

## filters.py

Converte parâmetros da URL em filtros do MongoDB.

Exemplo:

```
GET /api/one-piece/cards?name=luffy&color=Red
```

vira

```python
{
    "name": {"$regex": "luffy", "$options": "i"},
    "color": "Red"
}
```

Cada jogo possui sua própria função de filtros.

Exemplo:

- apply_onepiece_filters()
- apply_sorcery_filters()
- apply_yugioh_filters()
- apply_fab_filters()

---

## mango.py

É o módulo responsável pela comunicação com o MongoDB.

Possui três responsabilidades:

### Conexão

Gerencia o MongoClient e as coleções.

### Consultas

- buscar_docs()
- buscar_por_id()
- buscar_por_nome()
- contar_docs()
- random_doc()

### Normalização

Cada coleção possui um formato diferente.

Antes de devolver qualquer resultado, a Homura converte o documento para um formato padronizado através de:

- format_op()
- format_fab()
- format_yugi()
- format_sorcery()
- format_swu()
- format_rift()
- format_gundam()
- format_uniona()

Isso garante estabilidade para quem consome a API.

---

## magic.py

Responsável pela integração com o Scryfall.

Magic não utiliza o banco Mongo da Homura.

O módulo consulta diretamente a API oficial do Scryfall e adapta o retorno para o formato utilizado pela Homura.

---

# Providers

Atualmente existem três providers de dados.

## Mongo

```
Cliente

↓

FastAPI

↓

MongoDB

↓

Normalização

↓

Resposta
```

---

## Scryfall

```
Cliente

↓

FastAPI

↓

Scryfall

↓

Resposta
```

---

## APITCG

```
Cliente

↓

FastAPI

↓

APITCG

↓

Resposta
```

---

# Fluxo de uma requisição

Exemplo:

```
GET /api/one-piece/cards?name=luffy
```

Fluxo interno:

```
Cliente

↓

FastAPI

↓

Validação da API Key

↓

Identificação do provider

↓

Construção do filtro

↓

Consulta ao banco

↓

Normalização

↓

Resposta JSON
```

---

# Endpoints

## Informações da API

```
GET /
```

Retorna informações das coleções.

---

## Buscar cartas

```
GET /api/{game}/cards
```

Possui paginação.

Parâmetros variam conforme cada jogo.

---

## Buscar por ID

```
GET /api/{game}/cards/{id}
```

---

## Buscar por nome ou ID

```
GET /api/{game}/cards/lookup?q=
```

---

## Buscar várias cartas

```
POST /api/{game}/cards/bulk
```

Body:

```json
{
    "ids": [
        "...",
        "...",
        "..."
    ]
}
```

---

## Carta aleatória

```
GET /api/{game}/cards/random
```

---

## Magic

```
GET /api/magic/cards
```

Consulta diretamente o Scryfall.

---

# Paginação

As consultas retornam:

```json
{
    "page": 1,
    "limit": 25,
    "total": 100,
    "totalPages": 4,
    "data": []
}
```

---

# Cache

Todas as respostas recebem:

```
Cache-Control

s-maxage=300
stale-while-revalidate=600
```

Permitindo cache em CDNs como a Vercel.

---

# Variáveis de ambiente

Exemplo:

```
API_KEY=

MONGO_USR=

MONGO_PWD=

MONGO_CLUSTER=

APITCG_API_KEY=
```

---

# Como adicionar um novo jogo

A arquitetura foi pensada para facilitar a inclusão de novos jogos.

Os passos normalmente são:

1. Criar a coleção Mongo.
2. Criar um formatador em `mango.py`.
3. Criar um filtro em `filters.py`.
4. Registrar no `GAME_CONFIG`.
5. Registrar o provider em `GAME_SRC`.

Nenhuma rota nova precisa ser criada.

---

# Filosofia do projeto

A Homura **não é apenas um banco de dados de cartas**.

Ela atua como uma camada de abstração entre diversas fontes de dados e as aplicações consumidoras.

Seu principal objetivo é fornecer uma API consistente, independente da origem das informações.

Isso permite que aplicações como o Cardumy trabalhem sempre com uma interface única, sem precisar conhecer as diferenças entre cada TCG ou provider.

---

# Roadmap

Algumas melhorias planejadas para versões futuras:

- Versionamento da API (`/v1`, `/v2`)
- Schemas Pydantic para todas as respostas
- Documentação completa de filtros por jogo
- Providers independentes para Mongo, Scryfall e APITCG
- Testes automatizados
- Cache inteligente
- Rate limiting
- Métricas e observabilidade
- Documentação OpenAPI expandida

---

# Licença

Projeto privado.