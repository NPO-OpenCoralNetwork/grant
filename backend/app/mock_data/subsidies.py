"""
モックデータ: jGrants補助金情報
"""

MOCK_SUBSIDIES_SEARCH = {
    "metadata": {
        "type": "https://api.jgrants-portal.go.jp/",
        "resultset": {
            "count": 3
        }
    },
    "result": [
        {
            "id": "MOCK001",
            "name": "S-12345678",
            "title": "DX推進補助金（モックデータ）",
            "target_area_search": "全国",
            "subsidy_max_limit": 10000000,
            "acceptance_start_datetime": "2024-04-01T00:00:00Z",
            "acceptance_end_datetime": "2025-03-31T23:59:59Z",
            "target_number_of_employees": "300名以下"
        },
        {
            "id": "MOCK002",
            "name": "S-87654321",
            "title": "中小企業デジタル化支援事業（モックデータ）",
            "target_area_search": "東京都 / 大阪府 / 愛知県",
            "subsidy_max_limit": 5000000,
            "acceptance_start_datetime": "2024-06-01T00:00:00Z",
            "acceptance_end_datetime": "2025-05-31T23:59:59Z",
            "target_number_of_employees": "100名以下"
        },
        {
            "id": "MOCK003",
            "name": "S-11223344",
            "title": "IT導入補助金2024（モックデータ）",
            "target_area_search": "全国",
            "subsidy_max_limit": 3000000,
            "acceptance_start_datetime": "2024-05-01T00:00:00Z",
            "acceptance_end_datetime": "2025-02-28T23:59:59Z",
            "target_number_of_employees": "従業員の制約なし"
        }
    ]
}

MOCK_SUBSIDY_DETAILS = {
    "MOCK001": {
        "metadata": {
            "type": "https://api.jgrants-portal.go.jp/",
            "resultset": {
                "count": 1
            }
        },
        "result": [
            {
                "id": "MOCK001",
                "name": "S-12345678",
                "title": "DX推進補助金（モックデータ）",
                "subsidy_catch_phrase": "中小企業のデジタルトランスフォーメーションを支援します",
                "detail": "本補助金は、中小企業がDXを推進するために必要なシステム導入、業務プロセス改革、人材育成などの取組を支援することを目的としています。補助対象となる経費は、ソフトウェア購入費、クラウドサービス利用料、コンサルティング費用、研修費用などです。",
                "use_purpose": "新たな事業を行いたい / 設備整備・IT導入したい",
                "industry": "情報通信業 / 製造業 / 卸売業，小売業",
                "target_area_search": "全国",
                "target_area_detail": "日本全国",
                "target_number_of_employees": "300名以下",
                "subsidy_rate": "2/3以内",
                "subsidy_max_limit": 10000000,
                "acceptance_start_datetime": "2024-04-01T00:00:00Z",
                "acceptance_end_datetime": "2025-03-31T23:59:59Z",
                "project_end_deadline": "2025-12-31T23:59:59Z",
                "request_reception_presence": "有",
                "is_enable_multiple_request": False,
                "front_subsidy_detail_page_url": "https://example.com/subsidy/MOCK001"
            }
        ]
    },
    "MOCK002": {
        "metadata": {
            "type": "https://api.jgrants-portal.go.jp/",
            "resultset": {
                "count": 1
            }
        },
        "result": [
            {
                "id": "MOCK002",
                "name": "S-87654321",
                "title": "中小企業デジタル化支援事業（モックデータ）",
                "subsidy_catch_phrase": "中小企業のデジタル化を加速させます",
                "detail": "デジタル技術を活用した業務効率化やビジネスモデル変革を目指す中小企業を支援します。クラウドサービスの導入、ウェブサイトのリニューアル、ECサイトの構築など、幅広いデジタル化の取組が補助対象となります。",
                "use_purpose": "販路拡大・海外展開をしたい / 設備整備・IT導入したい",
                "industry": "卸売業，小売業 / 宿泊業，飲食サービス業 / サービス業（他に分類されないもの）",
                "target_area_search": "東京都 / 大阪府 / 愛知県",
                "target_area_detail": "東京都、大阪府、愛知県に本社または主たる事業所を有する事業者",
                "target_number_of_employees": "100名以下",
                "subsidy_rate": "1/2以内",
                "subsidy_max_limit": 5000000,
                "acceptance_start_datetime": "2024-06-01T00:00:00Z",
                "acceptance_end_datetime": "2025-05-31T23:59:59Z",
                "project_end_deadline": "2026-03-31T23:59:59Z",
                "request_reception_presence": "有",
                "is_enable_multiple_request": True,
                "front_subsidy_detail_page_url": "https://example.com/subsidy/MOCK002"
            }
        ]
    },
    "MOCK003": {
        "metadata": {
            "type": "https://api.jgrants-portal.go.jp/",
            "resultset": {
                "count": 1
            }
        },
        "result": [
            {
                "id": "MOCK003",
                "name": "S-11223344",
                "title": "IT導入補助金2024（モックデータ）",
                "subsidy_catch_phrase": "ITツール導入で生産性向上を実現",
                "detail": "業務効率化や売上向上につながるITツール（ソフトウェア、サービス等）の導入を支援します。会計ソフト、勤怠管理システム、ECサイト構築、MA/CRMツールなど、様々なITツールが補助対象となります。",
                "use_purpose": "設備整備・IT導入したい / 資金繰りを改善したい",
                "industry": "製造業 / 建設業 / 情報通信業 / 卸売業，小売業 / 宿泊業，飲食サービス業",
                "target_area_search": "全国",
                "target_area_detail": "全国（離島含む）",
                "target_number_of_employees": "従業員の制約なし",
                "subsidy_rate": "1/2以内（一部3/4以内）",
                "subsidy_max_limit": 3000000,
                "acceptance_start_datetime": "2024-05-01T00:00:00Z",
                "acceptance_end_datetime": "2025-02-28T23:59:59Z",
                "project_end_deadline": "2025-11-30T23:59:59Z",
                "request_reception_presence": "有",
                "is_enable_multiple_request": False,
                "front_subsidy_detail_page_url": "https://example.com/subsidy/MOCK003"
            }
        ]
    }
}


def get_mock_search_result(keyword: str = None) -> dict:
    """モック検索結果を取得"""
    # キーワードでフィルタリング（簡易実装）
    if keyword:
        filtered_results = [
            s for s in MOCK_SUBSIDIES_SEARCH["result"]
            if keyword.lower() in s["title"].lower()
        ]
        return {
            "metadata": {
                "type": "https://api.jgrants-portal.go.jp/",
                "resultset": {
                    "count": len(filtered_results)
                }
            },
            "result": filtered_results
        }
    return MOCK_SUBSIDIES_SEARCH


def get_mock_subsidy_detail(subsidy_id: str) -> dict:
    """モック補助金詳細を取得"""
    return MOCK_SUBSIDY_DETAILS.get(subsidy_id, {
        "metadata": {
            "type": "https://api.jgrants-portal.go.jp/",
            "resultset": {
                "count": 0
            }
        },
        "result": []
    })
