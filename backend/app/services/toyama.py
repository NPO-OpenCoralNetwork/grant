try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    print("⚠ feedparser not available. Toyama grants RSS feed parsing will be disabled.")

import json
import os
from datetime import datetime
from typing import Optional
from app.core.cache import cache


# 自治体のRSSフィード設定
CITY_FEEDS = {
    "富山市": "https://www.city.toyama.lg.jp/news.rss",
    "砺波市": "https://www.city.tonami.lg.jp/feed/?post_type=info",
    "富山県": "https://www.pref.toyama.jp/shinchaku/shinchaku.xml",
    "射水市": "https://www.city.imizu.toyama.jp/feed/service.ashx?srv=news",
    "氷見市": "https://www.city.himi.toyama.jp/cgi-bin/feed.php?siteNew=1",
    "滑川市": "https://www.city.namerikawa.toyama.jp/cgi-bin/feed.php?siteNew=1&displayRange=90",
    "高岡市": "https://www.city.takaoka.toyama.jp/cgi-bin/feed.php?siteNew=1&displayRange=90",
}

# デフォルトキーワード
DEFAULT_KEYWORDS = ["助成金", "DX", "助成金募集", "助成金公募", "支援", "補助"]


class ToyamaGrantsService:
    """富山県助成金サービス"""

    def __init__(self):
        self.data_file = "data/grants.json"
        self.keywords = DEFAULT_KEYWORDS

    def fetch_rss_feed(self, url: str, city: str) -> list[dict]:
        """RSSフィードを取得して解析"""
        if not FEEDPARSER_AVAILABLE:
            print(f"⚠ Cannot fetch RSS feed for {city}: feedparser not available")
            return []

        feed = feedparser.parse(url)
        entries = []

        for entry in feed.entries:
            entry_dict = self._parse_entry(entry)
            entry_dict['city'] = city

            # キーワードフィルタリング
            if self._is_grant_related(entry_dict['title']):
                entries.append(entry_dict)

        return entries

    def fetch_all_feeds(self) -> list[dict]:
        """全ての自治体のRSSフィードを取得"""
        all_entries = []

        for city, url in CITY_FEEDS.items():
            try:
                entries = self.fetch_rss_feed(url, city)
                all_entries.extend(entries)
            except Exception as e:
                print(f"Error fetching {city} feed: {e}")
                continue

        return all_entries

    def _parse_entry(self, entry) -> dict:
        """フィードエントリーを解析"""
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

    def _is_grant_related(self, title: str) -> bool:
        """タイトルが助成金関連かどうかを判定"""
        return any(keyword in title for keyword in self.keywords)

    def save_grants(self, grants: list[dict]) -> bool:
        """助成金情報をJSONファイルに保存"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({"grants": grants}, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving grants: {e}")
            return False

    def load_grants(self) -> list[dict]:
        """保存された助成金情報を読み込み"""

        # キャッシュから取得を試みる
        cache_key = "toyama_grants"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # ファイルから読み込み
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                grants = data.get("grants", [])

                # キャッシュに保存
                cache.set(cache_key, grants, ttl=1800)  # 30分

                return grants
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    async def update_grants(self) -> dict:
        """助成金情報を更新"""
        grants = self.fetch_all_feeds()
        success = self.save_grants(grants)

        if success:
            # キャッシュを更新
            cache.set("toyama_grants", grants, ttl=1800)

        return {
            "success": success,
            "count": len(grants),
            "message": f"Updated {len(grants)} grants" if success else "Failed to update grants"
        }

    def search_grants(
        self,
        keyword: Optional[str] = None,
        cities: Optional[list[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> list[dict]:
        """助成金を検索"""
        grants = self.load_grants()

        # キーワードフィルター
        if keyword:
            grants = [
                g for g in grants
                if keyword.lower() in g['title'].lower() or keyword.lower() in g['description'].lower()
            ]

        # 自治体フィルター
        if cities:
            grants = [g for g in grants if g['city'] in cities]

        # 日付フィルター
        if start_date or end_date:
            filtered_grants = []
            for g in grants:
                try:
                    pub_date = datetime.strptime(g['published'], '%Y-%m-%d %H:%M:%S').date()

                    if start_date:
                        start = datetime.strptime(start_date, '%Y-%m-%d').date()
                        if pub_date < start:
                            continue

                    if end_date:
                        end = datetime.strptime(end_date, '%Y-%m-%d').date()
                        if pub_date > end:
                            continue

                    filtered_grants.append(g)
                except (ValueError, TypeError):
                    # 日付のパースに失敗した場合はスキップ
                    continue

            grants = filtered_grants

        return grants


# Singleton instance
toyama_service = ToyamaGrantsService()
