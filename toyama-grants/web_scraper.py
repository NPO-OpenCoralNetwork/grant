from datetime import datetime
import json
from typing import List, Dict
from playwright.sync_api import sync_playwright
from config import get_keywords

class WebScraper:
    def __init__(self):
        self.scrapers = {
            "高岡市": self.scrape_takaoka,
            "砺波市": self.scrape_tonami,
            "富山県": self.scrape_toyama_pref,
            # 他の自治体のスクレイパーをここに追加
        }

    def scrape_all(self) -> List[Dict]:
        """全ての登録された自治体のWebページをスクレイピング"""
        all_entries = []
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            for city, scraper in self.scrapers.items():
                try:
                    entries = scraper(page)
                    all_entries.extend(entries)
                except Exception as e:
                    print(f"Error scraping {city}: {str(e)}")
            
            browser.close()
        return all_entries

    def scrape_takaoka(self, page) -> List[Dict]:
        """高岡市の助成金情報をスクレイピング"""
        url = "https://www.city.takaoka.toyama.jp/gyosei/index.html"
        page.goto(url)
        
        items = []
        elements = page.query_selector_all(".pageEntity")
        
        for element in elements:
            try:
                title_el = element.query_selector(".title-text")
                if not title_el:
                    continue
                
                title = title_el.inner_text()
                link_el = element.query_selector(".pageLink")
                link = link_el.get_attribute("href") if link_el else ""
                
                date_el = element.query_selector(".pageDate")
                published = date_el.inner_text() if date_el else ""
                
                if self._is_grant_related(title):
                    description = f"【タイトル】{title}\n【詳細リンク】{link}"
                    items.append({
                        "title": title,
                        "link": link,
                        "published": self._parse_date(published),
                        "description": description,
                        "city": "高岡市"
                    })
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue
                
        return items

    def scrape_toyama_pref(self, page) -> List[Dict]:
        """富山県の助成金情報をスクレイピング"""
        url = "https://www.pref.toyama.jp/mokutekibetsu/joseiyushi/index.html"
        page.goto(url)
        
        items = []
        # 全てのテーブルから情報を取得
        tables = page.query_selector_all("table.list_table")
        
        try:
            for table in tables:
                rows = table.query_selector_all("tr")
                for row in rows:
                    try:
                        date_el = row.query_selector(".date p")
                        link_el = row.query_selector("td:not(.date) a")
                        
                        if not date_el or not link_el:
                            continue
                        
                        title = link_el.inner_text().strip()
                        link = link_el.get_attribute("href")
                        date_str = date_el.inner_text().strip()

                        if not link.startswith("http"):
                            link = f"https://www.pref.toyama.jp{link}"

                        # 日付を処理（"3月13日" → "2024年3月13日"のように現在の年を追加）
                        current_year = datetime.now().year
                        date_str = f"{current_year}年{date_str}"
                        
                        if self._is_grant_related(title):
                            description = f"【タイトル】{title}\n【詳細リンク】{link}\n【公開日】{date_str}"
                            items.append({
                                "title": title,
                                "link": link,
                                "published": self._parse_date(date_str),
                                "description": description,
                                "city": "富山県"
                            })
                    except Exception as e:
                        print(f"Error processing item: {str(e)}")
                        continue
        except Exception as e:
            print(f"Error processing table: {str(e)}")
                
        return items

    def scrape_tonami(self, page) -> List[Dict]:
        """砺波市の助成金情報をスクレイピング"""
        url = "https://www.city.tonami.lg.jp/info/"
        page.goto(url)
        
        items = []
        elements = page.query_selector_all(".pageLinkList_item")
        
        for element in elements:
            try:
                link_el = element.query_selector(".pageLinkList_item_inner")
                if not link_el:
                    continue
                    
                title_el = element.query_selector(".pageLinkList_item_title")
                if not title_el:
                    continue
                
                title = title_el.inner_text()
                link = link_el.get_attribute("href")
                
                date_el = element.query_selector("time")
                published = date_el.get_attribute("datetime") if date_el else ""
                
                department_el = element.query_selector(".pageLinkList_item_text")
                department = department_el.inner_text() if department_el else ""
                
                if self._is_grant_related(title):
                    description = f"【タイトル】{title}\n【担当部署】{department}\n【詳細リンク】{link}"
                    items.append({
                        "title": title,
                        "link": link,
                        "published": self._parse_date(published),
                        "description": description,
                        "city": "砺波市"
                    })
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue
                
        return items

    def _is_grant_related(self, title: str) -> bool:
        """タイトルが助成金関連かどうかを判定"""
        keywords = get_keywords()
        return any(keyword in title for keyword in keywords)

    def _parse_date(self, date_str: str) -> str:
        """日付文字列をパース"""
        try:
            # ISO形式の日付文字列の場合（例: "2025-03-14"）
            if "-" in date_str:
                date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
            # 日本語形式の日付文字列の場合（例: "2024年3月15日"）
            else:
                date = datetime.strptime(date_str.strip(), "%Y年%m月%d日")
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_str  # パースできない場合は元の文字列を返す
