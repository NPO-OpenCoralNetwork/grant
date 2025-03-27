import asyncio
from web_scraper import WebScraper
from utils import save_grants, load_grants

def test_web_scraping():
    """Webスクレイピングのテスト"""
    print("\n=== Webスクレイピングのテスト ===")
    scraper = WebScraper()
    results = scraper.scrape_all()
    
    print(f"\n取得された情報: {len(results)}件\n")
    for item in results:
        print(f"タイトル: {item['title']}")
        print(f"リンク: {item['link']}")
        print(f"公開日: {item['published']}")
        print(f"自治体: {item['city']}")
        print("-" * 50)

def test_json_storage():
    """JSON保存のテスト"""
    print("\n=== JSON保存のテスト ===")
    scraper = WebScraper()
    results = scraper.scrape_all()
    
    # 結果を保存
    save_grants(results)
    print("データを保存しました")
    
    # 保存したデータを読み込み
    loaded_results = load_grants()
    print(f"読み込んだデータ: {len(loaded_results)}件")

if __name__ == "__main__":
    test_web_scraping()
    test_json_storage()
