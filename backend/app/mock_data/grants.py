"""
モックデータ: 富山県助成金情報
"""

MOCK_TOYAMA_GRANTS = [
    {
        "title": "【モック】富山県中小企業DX推進支援事業",
        "link": "https://example.com/toyama/grant001",
        "published": "2024-10-15 10:00:00",
        "description": "富山県内の中小企業がDXを推進するための設備投資やシステム導入に対する支援金です。",
        "city": "富山県"
    },
    {
        "title": "【モック】高岡市地域産業活性化助成金",
        "link": "https://example.com/takaoka/grant001",
        "published": "2024-11-01 09:00:00",
        "description": "高岡市内の事業者が新規事業を開始する際の初期投資費用を補助します。",
        "city": "高岡市"
    },
    {
        "title": "【モック】富山市スタートアップ支援事業",
        "link": "https://example.com/toyama-city/grant001",
        "published": "2024-10-20 14:30:00",
        "description": "富山市内で新たに事業を始める起業家を対象とした助成金制度です。",
        "city": "富山市"
    },
    {
        "title": "【モック】砺波市IT導入補助事業",
        "link": "https://example.com/tonami/grant001",
        "published": "2024-09-30 11:00:00",
        "description": "砺波市内の事業者がITシステムやソフトウェアを導入する際の費用を補助します。",
        "city": "砺波市"
    },
    {
        "title": "【モック】富山県事業承継支援補助金",
        "link": "https://example.com/toyama/grant002",
        "published": "2024-11-10 13:00:00",
        "description": "後継者不足に悩む県内企業の事業承継を円滑に進めるための支援制度です。",
        "city": "富山県"
    }
]


def get_mock_grants() -> list:
    """モック助成金リストを取得"""
    return MOCK_TOYAMA_GRANTS
