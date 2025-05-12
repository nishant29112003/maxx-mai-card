import os
import json
import yaml  # requires: pip install pyyaml

def recommend_card(spends: dict) -> str:
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, '../models/cards.json')
    yaml_path = os.path.join(base_dir, '../models/cards.yaml')

    if os.path.exists(json_path):
        with open(json_path) as f:
            cards = json.load(f)
    elif os.path.exists(yaml_path):
        with open(yaml_path) as f:
            cards = yaml.safe_load(f)
    else:
        raise FileNotFoundError("No card definition file found (JSON or YAML).")

    best_score = 0
    best_card = ""
    for card in cards:
        score = sum(spends.get(category, 0) * rate for category, rate in card["rewards"].items())
        if score > best_score:
            best_score = score
            best_card = card["name"]
    return best_card
