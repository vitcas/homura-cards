import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime

load_dotenv()

MONGO_USR = os.getenv("MONGO_USR")
MONGO_PWD = os.getenv("MONGO_PWD")
pwd = quote_plus(MONGO_PWD)
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
uri = f"mongodb+srv://{MONGO_USR}:{pwd}@{MONGO_CLUSTER}/?retryWrites=true&w=majority"
client = MongoClient(
    uri,
    maxPoolSize=20,
    minPoolSize=5,
    serverSelectionTimeoutMS=5000
)

db = client["tcg"]

collections = {
    "yugioh": db["yugioh_cards"],
    "fab": db["fab_cards"],
    "one-piece": db["onepiece_cards"],
    "sorcery": db["sorcery_cards"],
    "star-wars": db["swu_cards"],
    "riftbound": db["riftbound_cards"],
    "gundam": db["gundam_cards"],
    "union-arena": db["unionarena_cards"]
}

def touch_collection(collection_name):
    db.collection_meta.update_one(
        {"collection": collection_name},
        {"$set": {"last_update": datetime.utcnow()}},
        upsert=True
    )

def get_meta():
    docs = list(db.collection_meta.find({}, {"_id": 0}))
    return docs

def buscar_por_id(collec, card_id):
    query = {}
    # yugioh → id é número
    if collec == "yugioh":
        try:
            query["id"] = int(card_id)
        except ValueError:
            return None
    # fab → usa unique_id
    elif collec == "fab":
        query["unique_id"] = card_id
    # swu → id é Set-Number, mas você gera isso no formatador
    elif collec == "star-wars":
        # exemplo: SWH-002 → separa set e number
        if "-" in card_id:
            set_code, number = card_id.split("-", 1)
            query["Set"] = set_code
            query["Number"] = number
        else:
            return None
    # one-piece, riftbound, sorcery → usam id string normal
    else:
        query["id"] = card_id
    return collections[collec].find_one(query, {"_id": 0})

def contar_docs(collec, query):
    return collections[collec].count_documents(query)

def buscar_docs(collec, query, page, limit):
    cursor = (
        collections[collec]
        .find(query, {"_id": 0})
        .skip((page - 1) * limit)
        .limit(limit)
    )
    return [format_card(collec, c) for c in cursor]

def random_doc(collec):
    docs = list(collections[collec].aggregate([{"$sample": {"size": 1}},{"$project": {"_id": 0}}]))
    return format_card(collec, docs[0]) if docs else None

def format_card(collec, card):
    if collec == "yugioh":
        return format_yugi(card)
    if collec == "fab":
        return format_fab(card)
    if collec == "sorcery":
        return format_sorcery(card)
    if collec == "riftbound":
        return format_rift(card)
    if collec == "one-piece":
        return format_op(card)
    if collec == "star-wars":
        return format_swu(card)
    if collec == "gundam":
        return format_gundam(card)
    if collec == "union-arena":
        return format_uniona(card)
    return card  # fallback

def format_yugi(card):
    formatted = {
        "id": str(card.get("id")),
        "name": card.get("name"),
        "type": card.get("type"), #Effect Monster
        "frameType": card.get("frameType"), #effect, spell
        "attribute": card.get("attribute"),
        "race": card.get("race"),
        "level": card.get("level"),
        "atk": card.get("atk"),
        "def": card.get("def"),
        "archetype": card.get("archetype"),
        "effect": card.get("desc"),
        "images": {"small": None, "large": None},
        "variants": []
    }
    imgs = card.get("card_images", [])
    if imgs:
        formatted["images"] = {
            "small": imgs[0].get("image_url_small"),
            "large": imgs[0].get("image_url")
        }
    for s in card.get("card_sets", []):
        formatted["variants"].append({
            "set_code": s.get("set_code"),
            "set_rarity": s.get("set_rarity"),
            "set_price": s.get("set_price"),
            "tcgplayerId": s.get("tcgplayerId"),
            "juSTname": s.get("juSTname"),
            "condition": s.get("condition"),
            "language": s.get("language"),
            "lowPrice": s.get("lowPrice"),
            "midPrice": s.get("midPrice"),
            "marketPrice": s.get("marketPrice"),
            "highPrice": s.get("highPrice")
        })
    return formatted

def format_fab(card):
    formatted = {
        "id": card.get("unique_id"),
        "code": card.get("unique_id"),
        "name": card.get("name"),
        "color": card.get("color"),
        "type": card.get("type_text"),
        "types": card.get("types", []),
        "traits": card.get("traits", []),
        "keywords": card.get("card_keywords", []),
        "cost": card.get("cost"),
        "pitch": card.get("pitch"),
        "power": card.get("power"),
        "defense": card.get("defense"),
        "hp": card.get("health"),
        "intelligence": card.get("intelligence"),
        "functional_text": card.get("functional_text"),
        "functional_text_plain": card.get("functional_text_plain"),
        "playedHorizontally": card.get("played_horizontally", False),
        "legalities": {
            "blitz": card.get("blitz_legal", False),
            "classicConstructed": card.get("cc_legal", False),
            "commoner": card.get("commoner_legal", False),
            "upfBanned": card.get("upf_banned", False)
        },
        "variants": []
    }
    for p in card.get("printings", []):
        formatted["variants"].append({
            "set_code": p.get("set_id"),
            "rarity": p.get("rarity"),
            "foiling": p.get("foiling"),
            "edition": p.get("edition"),
            "artist": (p.get("artists") or [None])[0],
            "image": p.get("image_url"),
            "tcgplayerId": p.get("tcgplayer_product_id"),
        })
    img = formatted["variants"][0]["image"] if formatted["variants"] else None
    formatted["images"] = {"small": img, "large": img}
    return formatted

def format_sorcery(card):
    formatted = {
        "id": str(card.get("id")),
        "name": card.get("name"),   
        "guardian": card.get("guardian", {}),
        "elements": card.get("elements"),
        "subTypes": card.get("subTypes", []),
        "images": card.get("images", {}),
        "variants": []
    }
    variants = []
    for s in card.get("sets", []):
        set_name = s.get("name")
        for v in s.get("variants", []):
            variants.append({
                "set": set_name,
                "finish": v.get("finish"),
                "product": v.get("product"),
                "tcgplayerId": v.get("tcgplayerId"),
                "marketPrice": v.get("marketPrice"),
            })
    formatted["variants"] = variants
    return formatted

def format_rift(card):
    formatted = {
        "id": card.get("id"),
        "number": card.get("number"),
        "name": card.get("cleanName"),
        "cardType": card.get("cardType"),
        "rarity": card.get("rarity"),
        "domain": card.get("domain"),
        "energyCost": card.get("energyCost"),
        "powerCost": card.get("powerCost"),
        "might": card.get("might"),
        "description": card.get("description"),
        "flavorText": card.get("flavorText"),
        "images": card.get("images", {}),
        "set": card.get("set", {}),
        "variants": card.get("variants", [])
    }
    return formatted

def format_gundam(card):
    formatted = {
        "id": card.get("id"),
        "code": card.get("code"),
        "rarity": card.get("rarity"),
        "name": card.get("name"),
        "images": card.get("images", {}),
        "level": card.get("level"),
        "cost": card.get("cost"),
        "color": card.get("color"),
        "cardType": card.get("cardType"),
        "effect": card.get("effect", {}),
        "zone": card.get("zone"),
        "trait": card.get("trait"),
        "link": card.get("link"),
        "ap": card.get("ap"),
        "hp": card.get("hp"),
        "sourceTitle": card.get("sourceTitle"),
        "getIt": card.get("getIt"),
        "set": card.get("set", {})
    }
    return formatted

def format_op(card):
    formatted = {
        "id": card.get("id"),
        "code": card.get("code"),
        "name": card.get("name"),
        "type": card.get("type"),
        "rarity": card.get("rarity"),
        "color": card.get("color"),
        "family": card.get("family"),
        "attribute": card.get("attribute", {}),
        "cost": card.get("cost"),
        "power": card.get("power"),
        "counter": card.get("counter"),
        "ability": card.get("ability"),
        "trigger": card.get("trigger"),
        "images": card.get("images", {}),
        "set": card.get("set", {}),
        "variants": card.get("variants", [])
    }
    return formatted

def format_uniona(card):
    formatted = {
        "id": card.get("id"),
        "code": card.get("code"),
        "url": card.get("url"),
        "name": card.get("name"),
        "rarity": card.get("rarity"),
        "ap": card.get("ap"),
        "type": card.get("type"),
        "bp": card.get("bp"),
        "affinity": card.get("affinity"),
        "effect": card.get("effect"),
        "trigger": card.get("trigger"),
        "images": card.get("images", {}),
        "set": card.get("set", {})
    }
    return formatted

def format_swu(card):
    formatted = {
        "id": None,
        "name": card.get("Name"),
        "subtitle": card.get("Subtitle"),
        "type": card.get("Type"),
        "aspects": card.get("Aspects"),
        "traits": card.get("Traits"),
        "arenas": card.get("Arenas"),
        "cost": card.get("Cost"),
        "power": card.get("Power"),
        "hp": card.get("HP"),
        "frontText": card.get("FrontText"),
        "epicAction": card.get("EpicAction"),
        "doubleSided": card.get("DoubleSided"),
        "backText": card.get("BackText"),
        "rarity": card.get("Rarity"),
        "unique": card.get("Unique"),
        "artist": card.get("Artist"),
        "images": {},
        "set": card.get("Set"),
        "variants": []
    }

    # imagens
    front = card.get("FrontArt")
    back = card.get("BackArt")
    if front:
        formatted["images"] = {
            "front": front,
            "back": back,
            "small": front,
            "large": front
        }

    # variantes
    variant = {
        "type": card.get("VariantType"),
        "marketPrice": card.get("MarketPrice"),
        "lowPrice": card.get("LowPrice"),
        "foilPrice": card.get("FoilPrice"),
    }
    variant = {k: v for k, v in variant.items() if v is not None}
    if variant:
        formatted["variants"] = [variant]

    # id/code
    set_code = card.get("Set")
    number = card.get("Number")
    if set_code and number:
        formatted["id"] = f"{set_code}-{number}"

    return formatted
