import math
import requests

def fetch_mtg_cards(limit=25, page=1, **filters):
    # Sanitização
    limit = min(int(limit), 100)
    page = max(int(page), 1)
    # Montagem do q=
    mapping = {
        "name": "name:",
        "set": "set:",
        "colors": "color:",
        "rarity": "rarity:",
        "layout": "layout:",
        "cmc": "cmc:",
        "language": "lang:",
        "id": "scryfallid:",
    }
    q_parts = []
    for old_key, prefix in mapping.items():
        val = filters.get(old_key)
        if val:
            q_parts.append(f'{prefix}"{val}"')
    q = " ".join(q_parts) if q_parts else "*"
    # Request
    url = "https://api.scryfall.com/cards/search"
    params = {
        "q": q,
        "page": page,
        "unique": "cards",
        "order": "name"
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    resp_json = r.json()
    cards = resp_json.get("data", [])
    total = resp_json.get("total_cards", len(cards))
    data = []
    for c in cards:
        images = c.get("image_uris") or (
            (c.get("card_faces")[0].get("image_uris") if c.get("card_faces") else None)
        )
        if images:
            images = {
                "small": images.get("small"),
                "normal": images.get("normal"),
                "large": images.get("large"),
            }
            images = {k: v for k, v in images.items() if v}
        set_obj = {
            "set_code": c.get("set"),
            "name": c.get("set_name"),
        }
        set_obj = {k: v for k, v in set_obj.items() if v}
        multiverse_id = (c.get("multiverse_ids") or [None])[0]
        out = {
            "id": c.get("id"),
            "name": c.get("name"),
            "manaCost": c.get("mana_cost"),
            "cmc": c.get("cmc"),
            "colors": c.get("colors"),
            "colorIdentity": c.get("color_identity"),
            "typeline": c.get("type_line"),
            "rarity": c.get("rarity"),
            "effect": c.get("oracle_text"),
            "artist": c.get("artist"),
            "number": c.get("collector_number"),
            "power": c.get("power"),
            "toughness": c.get("toughness"),
            "layout": c.get("layout"),
            "multiverseid": multiverse_id,
            "printings": c.get("prints_search_uri"),
            "legalities": c.get("legalities"),
        }
        if images:
            out["images"] = images
        if set_obj:
            out["set"] = set_obj
        data.append({k: v for k, v in out.items() if v is not None})
    total_pages = math.ceil(total / limit) if limit > 0 else 1
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": total_pages,
        "data": data,
    }
