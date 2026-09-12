# mango.py
# interações com o banco de dados mongo
import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING
from urllib.parse import quote_plus
from datetime import datetime

load_dotenv()

MONGO_USR = os.getenv("MONGO_USR")
MONGO_PWD = os.getenv("MONGO_PWD")
pwd = quote_plus(MONGO_PWD)
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
uri = (f"mongodb+srv://{MONGO_USR}:{pwd}@{MONGO_CLUSTER}/?retryWrites=true&w=majority")
client = MongoClient(
    uri,
    maxPoolSize=20,
    minPoolSize=5,
    serverSelectionTimeoutMS=5000
)
db = client["tcg"]

def get_collection(collection_name):
    return db[collection_name]

def get_meta():
    docs = list(
        db.collection_meta.find({}, {"_id": 0})
    )
    return docs

def touch_collection(collection_name):
    db.collection_meta.update_one(
        {"collection": collection_name},
        {"$set": {"last_update": datetime.utcnow()}},
        upsert=True
    )

def buscar_por_id(collection_name, card_id):
    collection = get_collection(collection_name)

    query = {}

    # Yu-Gi-Oh → id é número
    if collection_name == "yugioh_cards":
        try:
            query["id"] = int(card_id)
        except (ValueError, TypeError):
            return None

    # FAB → usa unique_id
    elif collection_name == "fab_cards":
        query["unique_id"] = card_id

    # SWU → id é Set-Number
    elif collection_name == "swu_cards":
        if "-" in card_id:
            set_code, number = card_id.split("-", 1)
            query["Set"] = set_code
            query["Number"] = number
        else:
            return None

    # Demais jogos → id normal
    else:
        query["id"] = card_id

    return collection.find_one(query, {"_id": 0})

def buscar_por_nome(collection_name, name):
    if not name:
        return None

    collection = get_collection(collection_name)

    field_map = {
        "swu_cards": "Title",
    }

    field = field_map.get(collection_name, "name")

    query = {
        field: {
            "$regex": f"^{re.escape(name.strip())}$",
            "$options": "i",
        }
    }

    return collection.find_one(query, {"_id": 0})

def contar_docs(collection_name, query):
    collection = get_collection(collection_name)
    return collection.count_documents(query)

def buscar_docs(collection_name,query,page,limit,sort=None,order="asc"):
    collection = get_collection(collection_name)
    cursor = collection.find(query, {"_id": 0})
    if sort:
        direction = (
            ASCENDING
            if order.lower() == "asc"
            else DESCENDING
        )
        cursor = cursor.sort(sort, direction)
    cursor = (
        cursor
        .skip((page - 1) * limit)
        .limit(limit)
    )
    return [
        format_card(collection_name, card)
        for card in cursor
    ]

def random_doc(collection_name):
    collection = get_collection(collection_name)
    docs = list(
        collection.aggregate([
            {"$sample": {"size": 1}},
            {"$project": {"_id": 0}}
        ])
    )
    return (
        format_card(collection_name, docs[0])
        if docs
        else None
    )

def format_card(collec, card):
    if collec == "yugioh":
        return format_yugi(card)
    if collec == "fab":
        return format_fab(card)
    if collec == "star-wars":
        return format_swu(card)
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

def get_variant_min_price(card):
    variants = card.get("variants") or []
    prices = []
    for variant in variants:
        price = variant.get("price")
        if isinstance(price, (int, float)) and price > 0:
            prices.append(price)
    return min(prices) if prices else None

def select_card_by_lowest_price(cards):
    """
    Escolhe o card que possui o menor preço válido em variants.

    Considera apenas preços:
    - numéricos
    - maiores que zero

    Se nenhum card tiver preço válido, retorna o primeiro
    de forma determinística.
    """
    if not cards:
        return None
    best_card = cards[0]
    best_price = get_variant_min_price(best_card)
    for card in cards[1:]:
        price = get_variant_min_price(card)
        if price is None:
            continue
        if best_price is None or price < best_price:
            best_card = card
            best_price = price
    return best_card

def buscar_bulk(collection_name, method, values):
    """
    Busca vários cards em uma única consulta MongoDB.
    - method: id, code ou name
    - preserva a ordem de values
    - escolhe o documento com menor variants[].price
    """
    collection = get_collection(collection_name)
    # Monta a query
    if method == "code":
        query = {
            "code": {
                "$in": values
            }
        }
    elif method == "name":
        field = "Title" if collection_name == "swu_cards" else "name"

        query = {
            "$or": [
                {
                    field: {
                        "$regex": f"^{re.escape(value.strip())}$",
                        "$options": "i"
                    }
                }
                for value in values
            ]
        }

    elif method == "id":

        # Yu-Gi-Oh → id numérico
        if collection_name == "yugioh_cards":
            numeric_ids = []

            for value in values:
                try:
                    numeric_ids.append(int(value))
                except (ValueError, TypeError):
                    pass

            if not numeric_ids:
                return {
                    "count": len(values),
                    "found": 0,
                    "not_found": values,
                    "data": [
                        {
                            "query": value,
                            "data": None
                        }
                        for value in values
                    ]
                }

            query = {
                "id": {
                    "$in": numeric_ids
                }
            }

        # FAB → unique_id
        elif collection_name == "fab_cards":
            query = {
                "unique_id": {
                    "$in": values
                }
            }

        # SWU → Set + Number
        elif collection_name == "swu_cards":
            conditions = []

            for value in values:
                if "-" not in value:
                    continue

                set_code, number = value.split("-", 1)

                conditions.append({
                    "Set": set_code,
                    "Number": number
                })

            if not conditions:
                return {
                    "count": len(values),
                    "found": 0,
                    "not_found": values,
                    "data": [
                        {
                            "query": value,
                            "data": None
                        }
                        for value in values
                    ]
                }

            query = {
                "$or": conditions
            }

        # Demais jogos → id normal
        else:
            query = {
                "id": {
                    "$in": values
                }
            }

    else:
        raise ValueError(f"Método de busca inválido: {method}")

    # UMA consulta ao Mongo
    docs = list(
        collection.find(
            query,
            {"_id": 0}
        )
    )

    # Agrupa documentos pelo valor pesquisado
    grouped = {}

    for doc in docs:

        if method == "code":
            key = doc.get("code")

        elif method == "name":
            field = "Title" if collection_name == "swu_cards" else "name"
            key = doc.get(field)

        elif method == "id":

            if collection_name == "yugioh_cards":
                key = str(doc.get("id"))

            elif collection_name == "fab_cards":
                key = doc.get("unique_id")

            elif collection_name == "swu_cards":
                key = f"{doc.get('Set')}-{doc.get('Number')}"

            else:
                key = doc.get("id")

        if key is not None:
            grouped.setdefault(
                str(key).strip().lower(),
                []
            ).append(doc)

    # Monta resultado na ordem original
    data = []
    not_found = []

    for value in values:
        key = value.strip().lower()

        matches = grouped.get(key, [])

        if not matches:
            not_found.append(value)

            data.append({
                "query": value,
                "data": None
            })

            continue

        # Escolhe o menor preço válido
        card = select_card_by_lowest_price(matches)

        data.append({
            "query": value,
            "data": format_card(
                collection_name,
                card
            )
        })

    return {
        "count": len(values),
        "found": len(values) - len(not_found),
        "not_found": not_found,
        "data": data
    }

def buscar_bulk_v2(collection_name, criteria_list):
    """
    Bulk V2 genérico e seguro.

    Cada item de criteria_list representa uma busca independente.

    Exemplo:

    {
        "name": {
            "regex": "^Charmander$",
            "options": "i"
        },
        "set.set_code": "MEW",
        "code": {
            "regex": "004$"
        }
    }

    Regras permitidas:

    Valor simples:
        "name": "Charmander"

    Regex:
        "name": {
            "regex": "^Charmander$",
            "options": "i"
        }

    Nenhum operador MongoDB é aceito diretamente.

    Todos os critérios do mesmo objeto são combinados
    com AND.

    Todas as buscas são executadas em uma única consulta MongoDB.
    """

    collection = get_collection(collection_name)

    # ---------------------------------------------------------
    # Converte um critério recebido para uma condição MongoDB
    # ---------------------------------------------------------

    def build_condition(value):

        # Valor simples
        if isinstance(value, (str, int, float, bool)):
            if isinstance(value, str):
                value = value.strip()

            return value

        # Critério especial de regex
        if isinstance(value, dict):

            allowed_keys = {"regex", "options"}

            # Não permite nenhuma outra chave
            if not set(value.keys()).issubset(allowed_keys):
                raise ValueError(
                    "Critério de objeto inválido. "
                    "Use apenas 'regex' e 'options'."
                )

            regex = value.get("regex")

            if not isinstance(regex, str):
                raise ValueError(
                    "'regex' deve ser uma string."
                )

            options = value.get("options", "")

            if not isinstance(options, str):
                raise ValueError(
                    "'options' deve ser uma string."
                )

            # Só permite opções do Mongo que fazem sentido aqui
            allowed_options = set("imsx")

            if any(option not in allowed_options for option in options):
                raise ValueError(
                    "Opção de regex inválida. "
                    "Use apenas: i, m, s, x."
                )

            return {
                "$regex": regex,
                "$options": options
            }

        raise ValueError(
            "Valor de critério inválido."
        )

    # ---------------------------------------------------------
    # Monta uma query para cada item
    # ---------------------------------------------------------

    queries = []

    for criteria in criteria_list:

        if not criteria:
            raise ValueError(
                "Cada item de 'values' deve possuir pelo menos "
                "um critério."
            )

        if not isinstance(criteria, dict):
            raise ValueError(
                "Cada item de 'values' deve ser um objeto."
            )

        query = {}

        for field, value in criteria.items():

            if not isinstance(field, str):
                raise ValueError(
                    "Os nomes dos campos devem ser strings."
                )

            field = field.strip()

            if not field:
                raise ValueError(
                    "Nome de campo não pode ser vazio."
                )

            # Impede tentativa de injetar operador Mongo
            if field.startswith("$") or ".$" in field:
                raise ValueError(
                    f"Campo inválido: {field}"
                )

            if value is None:
                continue

            query[field] = build_condition(value)

        if not query:
            raise ValueError(
                "Nenhum critério válido foi informado."
            )

        queries.append(query)

    # ---------------------------------------------------------
    # Uma única consulta ao MongoDB
    # ---------------------------------------------------------

    mongo_query = {
        "$or": queries
    }

    docs = list(
        collection.find(
            mongo_query,
            {"_id": 0}
        )
    )

    # ---------------------------------------------------------
    # Verifica se um documento corresponde a um critério
    # ---------------------------------------------------------

    def get_nested_value(doc, field):
        """
        Resolve campos como:

        set.set_code
        pokemon.stage
        card.data.code
        """

        current = doc

        for part in field.split("."):

            if not isinstance(current, dict):
                return None

            current = current.get(part)

        return current

    def matches_criteria(doc, criteria):

        for field, expected in criteria.items():

            if expected is None:
                continue

            current = get_nested_value(
                doc,
                field
            )

            # Regex controlado
            if isinstance(expected, dict):

                regex = expected.get("regex")
                options = expected.get("options", "")

                if current is None:
                    return False

                flags = 0

                if "i" in options:
                    flags |= re.IGNORECASE

                if "m" in options:
                    flags |= re.MULTILINE

                if "s" in options:
                    flags |= re.DOTALL

                if "x" in options:
                    flags |= re.VERBOSE

                try:
                    if not re.search(
                        regex,
                        str(current),
                        flags
                    ):
                        return False

                except re.error:
                    return False

            # Valor simples
            else:

                if isinstance(expected, str):

                    if current is None:
                        return False

                    if (
                        str(current).strip().lower()
                        != expected.strip().lower()
                    ):
                        return False

                else:

                    if current != expected:
                        return False

        return True

    # ---------------------------------------------------------
    # Agrupa os documentos encontrados por query
    # ---------------------------------------------------------

    grouped = {
        index: []
        for index in range(len(criteria_list))
    }

    for doc in docs:

        for index, criteria in enumerate(criteria_list):

            if matches_criteria(
                doc,
                criteria
            ):
                grouped[index].append(doc)

    # ---------------------------------------------------------
    # Resultado preservando a ordem original
    # ---------------------------------------------------------

    data = []
    not_found = []

    for index, criteria in enumerate(criteria_list):

        matches = grouped[index]

        if not matches:

            not_found.append(criteria)

            data.append({
                "query": criteria,
                "data": None
            })

            continue

        # Mantém a lógica existente:
        # seleciona a variante com menor preço
        card = select_card_by_lowest_price(
            matches
        )

        data.append({
            "query": criteria,
            "data": format_card(
                collection_name,
                card
            )
        })

    return {
        "count": len(criteria_list),
        "found": len(criteria_list) - len(not_found),
        "not_found": not_found,
        "data": data
    }