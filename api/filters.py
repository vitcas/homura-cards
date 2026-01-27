# filters.py
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
