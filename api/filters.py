import re


def _values(args, key):
    """Lê parâmetros repetidos e valores separados por vírgula."""
    if hasattr(args, "getlist"):
        raw = args.getlist(key)
    else:
        raw = args.get(key, [])
        if not isinstance(raw, (list, tuple)):
            raw = [raw]

    values = []
    for item in raw:
        if item is None:
            continue
        values.extend(part.strip() for part in str(item).split(",") if part.strip())

    return list(dict.fromkeys(values))


def _regex(values):
    pattern = "|".join(f"(?:{value})" for value in values)
    return {"$regex": pattern, "$options": "i"}


def _build_filters(args, fields, set_fields=None):
    """
    fields: {parametro: (campo_mongo, tipo)}
    tipo: regex, array ou exact
    """
    q = {}
    and_conditions = []

    for param, (field, kind) in fields.items():
        values = _values(args, param)
        all_values = _values(args, f"{param}__all")

        if not values and not all_values:
            continue

        if kind == "array":
            if values:
                q[field] = {"$in": [re.compile(value, re.I) for value in values]}
            if all_values:
                and_conditions.append({
                    field: {"$all": [re.compile(value, re.I) for value in all_values]}
                })
        elif all_values:
            # __all é reservado para campos de array.
            continue
        elif kind == "exact":
            q[field] = values[0] if len(values) == 1 else {"$in": values}
        else:
            q[field] = _regex(values)

    if set_fields:
        set_values = _values(args, "set")
        if set_values:
            and_conditions.append({
                "$or": [{field: _regex(set_values)} for field in set_fields]
            })

    if and_conditions:
        q["$and"] = and_conditions

    return q


def apply_altered_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "faction": ("faction.name", "regex"),
        "faction_code": ("faction.code", "regex"),
        "product": ("product.name", "regex"),
        "illustrator": ("illustrator", "regex"),
    }, ["variants.set.set_code", "variants.set.set_name",
        "variants.set.set_internal_code"])


def apply_cyberpunk_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "color": ("color", "regex"), "card_type": ("card_type", "regex"),
        "artist": ("artist", "regex"),
        "classification": ("classifications", "array"),
    }, ["variants.set.code", "variants.set.name"])


def apply_dbs_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "exact"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "cost": ("cost", "exact"), "power": ("power", "exact"),
        "characterTraits": ("characterTraits", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_digimon_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "artist": ("artist", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_fab_filters(args):
    return _build_filters(args, {
        "name": ("name", "regex"), "color": ("color", "regex"),
        "type": ("types", "array"), "set": ("variants.set.set_code", "regex"),
    })


def apply_godzilla_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "grade": ("grade", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_grandarchive_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "exact"),
        "element": ("element", "regex"), "type": ("types", "array"),
        "subtype": ("subtypes", "array"), "class": ("classes", "array"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_gundam_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "cardType": ("cardType", "regex"), "color": ("color", "regex"),
        "zone": ("zone", "regex"), "trait": ("trait", "regex"),
        "source_title": ("source_title", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_hololive_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "bloomLevel": ("bloomLevel", "regex"), "tag": ("tags", "array"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_lorcana_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "classification": ("classifications", "array"),
        "franchise": ("franchise", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_onepiece_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "color": ("color", "regex"),
        "cost": ("cost", "exact"), "power": ("power", "exact"),
        "family": ("family", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_pokemon_filters(args):
    q = _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "pokemonType": ("pokemonType", "regex"),
        "stage": ("stage", "regex"), "illustrator": ("illustrator", "regex"),
        "category": ("category", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])

    hp = _values(args, "hp")
    if hp:
        q["hp"] = int(hp[0]) if len(hp) == 1 else {"$in": [int(v) for v in hp]}
    return q


def apply_riftbound_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "super": ("super", "regex"),
        "energy": ("energy", "exact"), "power": ("power", "exact"),
        "might": ("might", "exact"), "color": ("colors.name", "array"),
        "artist": ("artist", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_sorcery_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "name": ("name", "regex"),
        "elements": ("elements", "array"), "subTypes": ("subTypes", "array"),
        "rarity": ("guardian.rarity", "regex"),
        "type": ("guardian.type", "regex"),
        "category": ("guardian.category", "regex"),
        "slot": ("guardian.slot", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_swu_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "name": ("name", "regex"),
        "type": ("type", "regex"), "rarity": ("rarity", "regex"),
        "artist": ("artist", "regex"),
    }, ["variants.set.set_code", "variants.set.set_name"])


def apply_unionarena_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_universus_filters(args):
    return _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "category": ("category", "regex"),
    }, ["variants.set.set_code", "variants.set.name"])


def apply_vanguard_filters(args):
    q = _build_filters(args, {
        "id": ("id", "regex"), "code": ("code", "regex"),
        "name": ("name", "regex"), "rarity": ("rarity", "regex"),
        "type": ("type", "regex"), "nation": ("nation", "regex"),
        "grade": ("grade", "exact"),
    }, ["variants.set.set_code", "variants.set.name"])
    return q


def apply_yugioh_filters(args):
    q = _build_filters(args, {
        "effect": ("desc", "regex"), "name": ("name", "regex"),
        "attribute": ("attribute", "regex"), "type": ("type", "regex"),
        "frameType": ("frameType", "regex"),
        "code": ("variants.variant_code", "regex"),
        "rarity": ("variants.rarity", "regex"),
    }, ["variants.set.set_code", "variants.set.set_name"])

    for field in ("id", "konami_id"):
        values = _values(args, field)
        if values:
            numbers = [int(value) for value in values]
            q[field] = numbers[0] if len(numbers) == 1 else {"$in": numbers}
    return q
