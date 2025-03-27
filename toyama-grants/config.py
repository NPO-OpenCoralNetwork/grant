import json
import os

CONFIG_FILE = "data/config.json"

def load_config():
    """設定を読み込みます"""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # デフォルト設定
        default_config = {
            "keywords": ["助成金", "DX", "助成金募集", "助成金公募", "支援", "補助"]
        }
        save_config(default_config)
        return default_config

def save_config(config):
    """設定を保存します"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_keywords():
    """キーワードリストを取得します"""
    config = load_config()
    return config.get("keywords", [])
