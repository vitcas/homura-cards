# main.py
import os, math, requests
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from api.security import api_key_guard
from api.magic import fetch_mtg_cards
from api.mango import (buscar_por_nome, contar_docs, buscar_docs, random_doc, buscar_por_id, get_meta)
import api.filters as filters

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Cards API", version="1.0.1", dependencies=[Depends(api_key_guard)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GAME_CONFIG = {
    "sorcery": {"collection": "sorcery", "filter_fn": filters.apply_sorcery_filters},
    "pokemon": {"collection": "pokemon", "filter_fn": filters.apply_pokemon_filters},
    "digimon": {"collection": "digimon", "filter_fn": filters.apply_digimon_filters},
    "dragon-ball-fusion": {"collection": "dragon-ball-fusion", "filter_fn": filters.apply_dbs_filters},
    "one-piece": {"collection": "one-piece", "filter_fn": filters.apply_onepiece_filters},
    "riftbound": {"collection": "riftbound", "filter_fn": filters.apply_riftbound_filters},
    "fab": {"collection": "fab", "filter_fn": filters.apply_fab_filters},
    "yugioh": {"collection": "yugioh", "filter_fn": filters.apply_yugioh_filters},
    "star-wars": {"collection": "star-wars", "filter_fn": filters.apply_swu_filters},
    "gundam": {"collection": "gundam", "filter_fn": filters.apply_gundam_filters},
    "union-arena": {"collection": "union-arena", "filter_fn": filters.apply_unionarena_filters},
    "magic": { "collection": None, "filter_fn": None}
}

def has_game(game: str) -> bool:
    return game in GAME_CONFIG

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
def get_cards(
    game: str,
    request: Request,
    limit: int = 25,
    page: int = 1,
    sort: str | None = None,
    order: str = "asc"
    ):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    if game == "magic":
        return get_mtg_cards(limit=limit, page=page)
    config = GAME_CONFIG[game]
    query = config["filter_fn"](request.query_params)
    total = contar_docs(config["collection"], query)
    data = buscar_docs(
    config["collection"],
    query,
    page,
    limit,
    sort,
    order)
    return paginated_response(data, page, limit, total)

@app.post("/api/{game}/cards/bulk")
def get_cards_bulk(game: str, body: dict = Body(...)):
    ids = body.get("ids")
    if not isinstance(ids, list):
        raise HTTPException(400, "Envie um JSON com lista 'ids'")
    collection = GAME_CONFIG[game]["collection"]
    result = [buscar_por_id(collection, cid) for cid in ids]
    result = [c for c in result if c]
    return {"count": len(result), "data": result}

@app.get("/api/{game}/cards/random")
def get_random_card(game: str):
    data = random_doc(GAME_CONFIG[game]["collection"])
    return {"data": data}

@app.get("/api/{game}/cards/lookup")
def get_card_by_id_or_name(game: str, q: str):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
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
    card = buscar_por_id(GAME_CONFIG[game]["collection"], card_id)
    if not card:
        raise HTTPException(404, "Card não encontrado")
    return {"data": card}

@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate=600"
    return response
