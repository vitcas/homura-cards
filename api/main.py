import os, math, requests
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from api.security import api_key_guard
from api.magic import fetch_mtg_cards
from api.mango import (buscar_por_nome, contar_docs, buscar_docs, random_doc, buscar_por_id, get_meta)
from api.filters import (
    apply_sorcery_filters,
    apply_onepiece_filters,
    apply_riftbound_filters,
    apply_fab_filters,
    apply_yugioh_filters,
    apply_swu_filters,
    apply_unionarena_filters,
    apply_gundam_filters
)

load_dotenv()

APITCG_API_KEY = os.getenv("APITCG_API_KEY")

app = FastAPI(title="Cards API", version="1.0.0", dependencies=[Depends(api_key_guard)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GAME_SRC = {
    "apitcg": ["digimon", "pokemon", "dragon-ball-fusion"],
    "mahou": [
        "sorcery", "one-piece", "riftbound",
        "star-wars", "fab", "yugioh",
        "magic", "gundam", "union-arena"
    ]
}

GAME_CONFIG = {
    "sorcery": {"collection": "sorcery", "filter_fn": apply_sorcery_filters},
    "one-piece": {"collection": "one-piece", "filter_fn": apply_onepiece_filters},
    "riftbound": {"collection": "riftbound", "filter_fn": apply_riftbound_filters},
    "fab": {"collection": "fab", "filter_fn": apply_fab_filters},
    "yugioh": {"collection": "yugioh", "filter_fn": apply_yugioh_filters},
    "star-wars": {"collection": "star-wars", "filter_fn": apply_swu_filters},
    "gundam": {"collection": "gundam", "filter_fn": apply_gundam_filters},
    "union-arena": {"collection": "union-arena", "filter_fn": apply_unionarena_filters},
}

def has_game(game: str) -> bool:
    return any(game in games for games in GAME_SRC.values())

def has_game_mahou(game: str) -> bool:
    return game in GAME_SRC["mahou"]

def get_apitcg_cards(game: str, request: Request):
    if not APITCG_API_KEY:
        raise RuntimeError("APITCG_API_KEY não configurada")
    url = f"https://apitcg.com/api/{game}/cards"
    params = dict(request.query_params)
    try:
        r = requests.get(
            url,
            headers={"x-api-key": APITCG_API_KEY},
            params=params,
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(502, detail=str(e))

def paginated_response(data, page, limit, total):
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": math.ceil(total / limit),
        "data": data
    }

@app.get("/")
def root():
    return get_meta()

@app.get("/api/magic/cards")
def get_mtg_cards(
    limit: int = 25,
    page: int = 1,
    name: str | None = None,
    set: str | None = None,
    colors: str | None = None,
    rarity: str | None = None,
    layout: str | None = None,
    cmc: str | None = None,
    language: str | None = None,
    id: str | None = None,
):
    try:
        return fetch_mtg_cards(
            limit=limit,
            page=page,
            name=name,
            set=set,
            colors=colors,
            rarity=rarity,
            layout=layout,
            cmc=cmc,
            language=language,
            id=id,
        )
    except requests.HTTPError as e:
        raise HTTPException(502, detail=f"Falha ao consultar Scryfall: {e}")

@app.get("/api/{game}/cards")
def get_cards(game: str, request: Request, limit: int = 25, page: int = 1):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    if not has_game_mahou(game):
        return get_apitcg_cards(game, request)
    if game == "magic":
        return get_mtg_cards(limit=limit, page=page)
    config = GAME_CONFIG[game]
    query = config["filter_fn"](request.query_params)
    total = contar_docs(config["collection"], query)
    data = buscar_docs(config["collection"], query, page, limit)
    return paginated_response(data, page, limit, total)

@app.post("/api/{game}/cards/bulk")
def get_cards_bulk(game: str, body: dict = Body(...)):
    if not has_game_mahou(game):
        raise HTTPException(404, "Jogo não habilitado")

    ids = body.get("ids")
    if not isinstance(ids, list):
        raise HTTPException(400, "Envie um JSON com lista 'ids'")

    collection = GAME_CONFIG[game]["collection"]
    result = [buscar_por_id(collection, cid) for cid in ids]
    result = [c for c in result if c]

    return {"count": len(result), "data": result}

@app.get("/api/{game}/cards/random")
def get_random_card(game: str):
    if not has_game_mahou(game):
        raise HTTPException(404, "Jogo não habilitado")
    data = random_doc(GAME_CONFIG[game]["collection"])
    return {"data": data}

@app.get("/api/{game}/cards/lookup")
def get_card_by_id_or_name(game: str, q: str):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    if not has_game_mahou(game):
        raise HTTPException(404, "Jogo não habilitado")
    collection = GAME_CONFIG[game]["collection"]
    # tenta ID primeiro
    card = buscar_por_nome(collection, q)
    if card:
        return {"data": card}
    # fallback para nome
    card = buscar_por_id(collection, q)
    if not card:
        raise HTTPException(404, "Card não encontrado")
    return {"data": card}

@app.get("/api/{game}/cards/{card_id}")
def get_card_by_id(game: str, card_id: str):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    if not has_game_mahou(game):
        raise HTTPException(404, "Jogo não habilitado")
    card = buscar_por_id(GAME_CONFIG[game]["collection"], card_id)
    if not card:
        raise HTTPException(404, "Card não encontrado")
    return {"data": card}

@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate=600"
    return response
