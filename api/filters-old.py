# filters.py
def apply_altered_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("faction"):
        q["faction.name"] = {"$regex": args["faction"], "$options": "i"}

    if args.get("faction_code"):
        q["faction.code"] = {"$regex": args["faction_code"], "$options": "i"}

    if args.get("product"):
        q["product.name"] = {"$regex": args["product"], "$options": "i"}

    if args.get("illustrator"):
        q["illustrator"] = {"$regex": args["illustrator"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.set_name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.set_internal_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_cyberpunk_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("card_type"):
        q["card_type"] = {"$regex": args["card_type"], "$options": "i"}

    if args.get("artist"):
        q["artist"] = {"$regex": args["artist"], "$options": "i"}

    if args.get("classification"):
        q["classifications"] = {
            "$regex": args["classification"],
            "$options": "i"
        }

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("artist"):
        q["artist"] = {"$regex": args["artist"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_fab_filters(args):
    q = {}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("type"):
        q["types"] = {"$regex": args["type"], "$options": "i"}

    if args.get("set"):
        q["variants.set.set_code"] = {
            "$regex": args["set"],
            "$options": "i"
        }

    return q

def apply_godzilla_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("grade"):
        q["grade"] = {"$regex": args["grade"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_grandarchive_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = args["rarity"]

    if args.get("element"):
        q["element"] = {"$regex": args["element"], "$options": "i"}

    if args.get("type"):
        q["types"] = {"$regex": args["type"], "$options": "i"}

    if args.get("subtype"):
        q["subtypes"] = {"$regex": args["subtype"], "$options": "i"}

    if args.get("class"):
        q["classes"] = {"$regex": args["class"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("cardType"):
        q["cardType"] = {"$regex": args["cardType"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("zone"):
        q["zone"] = {"$regex": args["zone"], "$options": "i"}

    if args.get("trait"):
        q["trait"] = {"$regex": args["trait"], "$options": "i"}

    if args.get("source_title"):
        q["source_title"] = {
            "$regex": args["source_title"],
            "$options": "i"
        }

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_hololive_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("bloomLevel"):
        q["bloomLevel"] = {
            "$regex": args["bloomLevel"],
            "$options": "i"
        }

    if args.get("tag"):
        q["tags"] = {
            "$regex": args["tag"],
            "$options": "i"
        }

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("classification"):
        q["classifications"] = {
            "$regex": args["classification"],
            "$options": "i"
        }

    if args.get("franchise"):
        q["franchise"] = {
            "$regex": args["franchise"],
            "$options": "i"
        }

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("color"):
        q["color"] = {"$regex": args["color"], "$options": "i"}

    if args.get("cost"):
        q["cost"] = args["cost"]

    if args.get("power"):
        q["power"] = args["power"]

    if args.get("family"):
        q["family"] = {"$regex": args["family"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("pokemonType"):
        q["pokemonType"] = {"$regex": args["pokemonType"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    if args.get("stage"):
        q["stage"] = {"$regex": args["stage"], "$options": "i"}

    if args.get("illustrator"):
        q["illustrator"] = {
            "$regex": args["illustrator"],
            "$options": "i"
        }

    if args.get("hp"):
        q["hp"] = int(args["hp"])

    if args.get("category"):
        q["category"] = {
            "$regex": args["category"],
            "$options": "i"
        }

    return q

def apply_riftbound_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("super"):
        q["super"] = {"$regex": args["super"], "$options": "i"}

    if args.get("energy"):
        q["energy"] = args["energy"]

    if args.get("power"):
        q["power"] = args["power"]

    if args.get("might"):
        q["might"] = args["might"]

    if args.get("color"):
        q["colors.name"] = {"$regex": args["color"], "$options": "i"}

    if args.get("artist"):
        q["artist"] = {"$regex": args["artist"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {"variants.set.set_code": {"$regex": args["set"], "$options": "i"}},
            {"variants.set.name": {"$regex": args["set"], "$options": "i"}}
        ]

    return q

def apply_sorcery_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("elements"):
        q["elements"] = {"$regex": args["elements"], "$options": "i"}

    if args.get("subTypes"):
        q["subTypes"] = {"$regex": args["subTypes"], "$options": "i"}

    if args.get("rarity"):
        q["guardian.rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["guardian.type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("category"):
        q["guardian.category"] = {"$regex": args["category"], "$options": "i"}

    if args.get("slot"):
        q["guardian.slot"] = {"$regex": args["slot"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_swu_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("artist"):
        q["artist"] = {"$regex": args["artist"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.set_name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

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
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_universus_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("category"):
        q["category"] = {"$regex": args["category"], "$options": "i"}

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    return q

def apply_vanguard_filters(args):
    q = {}

    if args.get("id"):
        q["id"] = {"$regex": args["id"], "$options": "i"}

    if args.get("code"):
        q["code"] = {"$regex": args["code"], "$options": "i"}

    if args.get("name"):
        q["name"] = {"$regex": args["name"], "$options": "i"}

    if args.get("rarity"):
        q["rarity"] = {"$regex": args["rarity"], "$options": "i"}

    if args.get("type"):
        q["type"] = {"$regex": args["type"], "$options": "i"}

    if args.get("nation"):
        q["nation"] = {"$regex": args["nation"], "$options": "i"}

    if args.get("grade"):
        q["grade"] = args["grade"]

    if args.get("set"):
        q["$or"] = [
            {"variants.set.set_code": {"$regex": args["set"], "$options": "i"}},
            {"variants.set.name": {"$regex": args["set"], "$options": "i"}}
        ]

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

    if args.get("code"):
        q["variants.variant_code"] = {
            "$regex": args["code"],
            "$options": "i"
        }

    if args.get("set"):
        q["$or"] = [
            {
                "variants.set.set_code": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            },
            {
                "variants.set.set_name": {
                    "$regex": args["set"],
                    "$options": "i"
                }
            }
        ]

    if args.get("rarity"):
        q["variants.rarity"] = {
            "$regex": args["rarity"],
            "$options": "i"
        }

    return q
