# filters.py
ALLOWED_FILTERS = {
    "sorcery": {
        "name", "type", "rarity", "element",
        "subtype", "set", "finish", "product", "artist"
    },

    "one-piece": {
        "id", "code", "name", "rarity",
        "type", "color", "cost", "power", "family", "set"
    },

    "gundam": {
        "id", "code", "name", "rarity"
    },

    "union-arena": {
        "id", "code", "name", "rarity"
    },

    "riftbound": {
        "name", "rarity", "might", "energyCost",
        "powerCost", "cardType", "domain", "set"
    },

    "fab": {
        "name", "set"
    },

    "yugioh": {
        "id", "konami_id", "effect", "name",
        "attribute", "type", "frameType", "set", "rarity"
    },

    "star-wars": {
        "name", "set"
    },

    "digimon": {
        "id", "code", "name", "rarity",
        "type", "color", "set"
    },

    "pokemon": {
        "id", "code", "name", "rarity",
        "type", "set", "card_type", "stage", "artist"
    },

    "dragon-ball-fusion": {
        "id", "code", "name", "rarity",
        "type", "color", "cost", "power",
        "characterTraits", "set"
    },

    "lorcana": {
        "id", "code", "name", "rarity", "set"
    },

    "cardfight-vanguard": {
        "id", "code", "name", "set"
    },

    "universus": {
        "id", "code", "name", "set"
    },

    "grand-archive": {
        "id", "code", "name", "set"
    },

    "altered": {
        "id", "code", "name", "set"
    },
}

def validate_filter_params(game, args):
    allowed = ALLOWED_FILTERS.get(game, set())
    ignored = {
        key
        for key in args.keys()
        if key not in {
            "page",
            "limit",
            "sort",
            "order"
        }
        and key not in allowed
    }
    return ignored

def apply_sorcery_filters(args):
    q = {}
    # Busca por nome da carta
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    # Tipo da carta → vem de guardian.type
    if args.get("type"):
        q["guardian.type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("rarity"):
        q["guardian.rarity"] = {"$regex": args["rarity"], "$options": "i"}
    # Elemento (Air, Fire, Water, etc) → raiz
    if args.get("element"):
        q["elements"] = {"$regex": args["element"], "$options": "i"}
    # Subtipo (Mortal, etc)
    if args.get("subtype"):
        q["subTypes"] = {"$regex": args["subtype"], "$options": "i"}
    # Buscar por SET ex: Alpha, Beta
    if args.get("set"):
        q["sets.name"] = {"$regex": args["set"], "$options": "i"}
    # Variant → finish (Standard, Foil)
    if args.get("finish"):
        q["sets.variants.finish"] = args["finish"]
    # Variant → product (Booster / Preconstructed_Deck)
    if args.get("product"):
        q["sets.variants.product"] = {"$regex": args["product"], "$options": "i"}
    # Variant → artist
    if args.get("artist"):
        q["sets.variants.artist"] = {"$regex": args["artist"], "$options": "i"}
    return q

def apply_onepiece_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("color"):
        q["color"] = args["color"]
    if args.get("cost"):
        q["cost"] = args["cost"]
    if args.get("power"):
        q["power"] = args["power"]
    if args.get("family"):
        q["family"] = {"$regex": args["family"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_gundam_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    return q

def apply_unionarena_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    return q

def apply_riftbound_filters(args):
    q = {}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("might"):
        q["might"] = args["might"]
    if args.get("energyCost"):
        q["energyCost"] = args["energyCost"]
    if args.get("powerCost"):
        q["powerCost"] = args["powerCost"]
    if args.get("cardType"):
        q["cardType"] = {"$regex": args["cardType"], "$options": "i"}
    if args.get("domain"):
        q["domain"] = {"$regex": args["domain"], "$options": "i"}
    if args.get("set"):
        q["set.name"] = {"$regex": args["set"], "$options": "i"}
    return q

def apply_fab_filters(args):
    q = {}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["printings.set_id"] = args["set"]
    return q

def apply_yugioh_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = int(args["id"])
    if args.get("konami_id"):
        q["konami_id"] = int(args["konami_id"])
    if args.get("effect"):
        q["desc"] = {"$regex": args["effect"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("attribute"):
        q["attribute"] = {"$regex": args["attribute"], "$options": "i"}
    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("frameType"):
        q["frameType"] = {"$regex": args["frameType"], "$options": "i"}
    if args.get("set"):
        q["card_sets.set_code"] = {"$regex": args["set"], "$options": "i"}
    if args.get("rarity"):
        q["card_sets.set_rarity"] = args["rarity"]
    return q

def apply_swu_filters(args):
    q = {}
    if args.get("name"):
        q["Name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["Set"] = {"$regex": args["set"], "$options": "i"}
    return q

def apply_digimon_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_pokemon_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    if args.get("card_type"):
        q["pokemon.card_type"] = {
            "$regex": args["card_type"],
            "$options": "i"
        }
    if args.get("stage"):
        q["pokemon.stage"] = {
            "$regex": args["stage"],
            "$options": "i"
        }
    if args.get("artist"):
        q["pokemon.artist"] = {
            "$regex": args["artist"],
            "$options": "i"
        }
    return q

def apply_dbs_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}
    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}
    if args.get("cost"):
        q["cost"] = args["cost"]
    if args.get("power"):
        q["power"] = args["power"]
    if args.get("characterTraits"):
        q["characterTraits"] = {
            "$regex": args["characterTraits"],
            "$options": "i"
        }
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_lorcana_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("rarity"):
        q["rarity"] = args["rarity"]
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_vanguard_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_universus_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_grandarchive_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_altered_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_cyberpunk_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_hololive_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q

def apply_godzilla_filters(args):
    q = {}
    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}
    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}
    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}
    if args.get("set"):
        q["set.set_code"] = args["set"]
    return q