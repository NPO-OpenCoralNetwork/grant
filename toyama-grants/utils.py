import feedparser
from datetime import datetime
import json
import os
from web_scraper import WebScraper
from config import get_keywords

# 自治体のRSSフィード設定
CITY_FEEDS = {
    "富山市": "https://www.city.toyama.lg.jp/news.rss",
    "砺波市": "https://www.city.tonami.lg.jp/feed/?post_type=info",
    "富山県": "https://www.pref.toyama.jp/shinchaku/shinchaku.xml",
    "射水市": "https://www.city.imizu.toyama.jp/feed/service.ashx?srv=news",
    "氷見市": "https://www.city.himi.toyama.jp/cgi-bin/feed.php?siteNew=1",
    "滑川市": "https://www.city.namerikawa.toyama.jp/cgi-bin/feed.php?siteNew=1&displayRange=90",
    "東京都": "https://www.metro.tokyo.lg.jp/rss/rss_sm.xml",
    "総務省": "http://soumu.go.jp/news.rdf",
    "高岡市": "https://www.city.takaoka.toyama.jp/cgi-bin/feed.php?siteNew=1&displayRange=90",
}

# Webスクレイピング対象の自治体を管理
web_scraper = WebScraper()

def fetch_rss_feed(url: str, city: str):
    """RSSフィードを取得して解析します"""
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        entry_dict = parse_entry(entry)
        entry_dict['city'] = city  # 自治体名を追加
        entries.append(entry_dict)
    return entries

def fetch_all_feeds(feeds_dict: dict):
    """全ての自治体のRSSフィードとWebページを取得します"""
    all_entries = []
    
    # RSSフィードからの取得
    for city, url in feeds_dict.items():
        entries = fetch_rss_feed(url, city)
        all_entries.extend([e for e in entries if is_grant_related(e['title'])])
    
    # Webスクレイピングからの取得
    web_entries = web_scraper.scrape_all()
    all_entries.extend(web_entries)
    
    return all_entries

def is_grant_related(title: str) -> bool:
    """タイトルが助成金関連かどうかを判定します"""
    keywords = get_keywords()
    return any(keyword in title for keyword in keywords)
def parse_entry(entry) -> dict:
    """フィードエントリーを解析して必要な情報を抽出します"""
    published = entry.get('published', '')
    try:
        published_date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z')
        published_str = published_date.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        published_str = published

    return {
        "title": entry.get('title', ''),
        "link": entry.get('link', ''),
        "published": published_str,
        "description": entry.get('description', ''),
    }

def save_grants(grants: list, file_path: str = "data/grants.json"):
    """助成金情報をJSONファイルに保存します"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"grants": grants}, f, ensure_ascii=False, indent=2)

def load_grants(file_path: str = "data/grants.json") -> list:
    """保存された助成金情報を読み込みます"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("grants", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def update_grants():
    """助成金情報を更新します"""
    grants = fetch_all_feeds(CITY_FEEDS)
    save_grants(grants)
    return grants
