# main.py
import math
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from api.security import api_key_guard
from api.mango import (buscar_por_nome, contar_docs, buscar_docs, random_doc, buscar_por_id, buscar_bulk, get_meta)
import api.filters as filters

GAME_CONFIG = {
    "altered": {"collection": "altered_cards", "filter_fn": filters.apply_altered_filters},
    "cardfight-vanguard": {"collection": "vanguard_cards", "filter_fn": filters.apply_vanguard_filters},
    "cyberpunk": {"collection": "cyberpunk_cards", "filter_fn": filters.apply_cyberpunk_filters},
    "digimon": {"collection": "digimon_cards", "filter_fn": filters.apply_digimon_filters},
    "dragon-ball-fusion": {"collection": "dragonball_cards", "filter_fn": filters.apply_dbs_filters},
    "fab": {"collection": "fab_cards", "filter_fn": filters.apply_fab_filters},
    "godzilla": {"collection": "godzilla_cards", "filter_fn": filters.apply_godzilla_filters},
    "grand-archive": { "collection": "grandarchive_cards", "filter_fn": filters.apply_grandarchive_filters},
    "gundam": {"collection": "gundam_cards", "filter_fn": filters.apply_gundam_filters},
    "hololive": {"collection": "hololive_cards", "filter_fn": filters.apply_hololive_filters},
    "lorcana": {"collection": "lorcana_cards", "filter_fn": filters.apply_lorcana_filters},
    "one-piece": {"collection": "onepiece_cards", "filter_fn": filters.apply_onepiece_filters},
    "pokemon": {"collection": "pokemon_cards", "filter_fn": filters.apply_pokemon_filters},
    "riftbound": {"collection": "riftbound_cards", "filter_fn": filters.apply_riftbound_filters},
    "sorcery": {"collection": "sorcery_cards", "filter_fn": filters.apply_sorcery_filters},
    "star-wars": {"collection": "swu_cards", "filter_fn": filters.apply_swu_filters},
    "universus": {"collection": "universus_cards", "filter_fn": filters.apply_universus_filters},
    "union-arena": {"collection": "unionarena_cards", "filter_fn": filters.apply_unionarena_filters},
    "yugioh": {"collection": "yugioh_cards", "filter_fn": filters.apply_yugioh_filters}, 
}

app = FastAPI(title="Homura Cards API", version="1.0.4", dependencies=[Depends(api_key_guard)])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Muitas requisições. Aguarde um momento."},
        headers={"Retry-After": "60"},
    )

@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate=600"
    return response

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

@app.get("/api/{game}/cards")
@limiter.limit("30/minute")
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
    invalid_filters = filters.validate_filter_params(game, request.query_params)
    if invalid_filters:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Filtro não suportado para este jogo",
                "filters": sorted(invalid_filters)
            }
        )
    config = GAME_CONFIG[game]
    query = config["filter_fn"](request.query_params)
    total = contar_docs(config["collection"], query)
    data = buscar_docs(config["collection"], query, page, limit, sort, order)
    return paginated_response(data, page, limit, total)

@app.post("/api/{game}/cards/bulk")
@limiter.limit("10/minute")
def get_cards_bulk(request: Request, game: str, body: dict = Body(...)):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    method = body.get("method")
    values = body.get("values")
    # Validação do método
    allowed_methods = {"id", "code", "name"}
    if method not in allowed_methods:
        raise HTTPException(
            400,
            {
                "message": "Método de busca inválido",
                "allowed": sorted(allowed_methods)
            }
        )
    # Validação da lista
    if not isinstance(values, list):
        raise HTTPException(
            400,
            "Envie um JSON com lista 'values'"
        )
    if not values:
        return {
            "method": method,
            "count": 0,
            "found": 0,
            "not_found": [],
            "data": []
        }
    # Todos os valores precisam ser strings
    if not all(isinstance(value, str) for value in values):
        raise HTTPException(
            400,
            "Todos os valores de 'values' devem ser strings"
        )
    # Remove espaços e valores vazios
    values = [
        value.strip()
        for value in values
        if value.strip()
    ]
    if not values:
        return {
            "method": method,
            "count": 0,
            "found": 0,
            "not_found": [],
            "data": []
        }
    collection = GAME_CONFIG[game]["collection"]
    result = buscar_bulk(
        collection,
        method,
        values
    )
    return {
        "method": method,
        **result
    }

@app.get("/api/{game}/cards/random")
@limiter.limit("60/minute")
def get_random_card(game: str, request: Request):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    data = random_doc(GAME_CONFIG[game]["collection"])
    return {"data": data}

@app.get("/api/{game}/cards/lookup")
@limiter.limit("60/minute")
def get_card_by_id_or_name(game: str, q: str, request: Request):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    collection = GAME_CONFIG[game]["collection"]
    # tenta ID primeiro
    card = buscar_por_id(collection, q)
    if card:
        return {"data": card}
    # fallback para nome
    card = buscar_por_nome(collection, q)
    if not card:
        raise HTTPException(404, "Card não encontrado")
    return {"data": card}

@app.get("/api/{game}/cards/{card_id}")
@limiter.limit("60/minute")
def get_card_by_id(game: str, card_id: str, request: Request):
    if not has_game(game):
        raise HTTPException(404, "Jogo não encontrado")
    card = buscar_por_id(GAME_CONFIG[game]["collection"], card_id)
    if not card:
        raise HTTPException(404, "Card não encontrado")
    return {"data": card}
