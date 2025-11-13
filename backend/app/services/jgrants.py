import httpx
from typing import Optional
from app.core.config import settings
from app.core.cache import cache


class JGrantsService:
    """jGrants API サービス"""

    def __init__(self):
        self.base_url = settings.JGRANTS_BASE_URL

    async def search_subsidies(
        self,
        keyword: str,
        sort: str = "created_date",
        order: str = "DESC",
        acceptance: str = "1",
        use_purpose: Optional[list[str]] = None,
        industry: Optional[list[str]] = None,
        target_number_of_employees: Optional[str] = None,
        target_area_search: Optional[str] = None
    ) -> Optional[dict]:
        """補助金検索"""

        # キャッシュキーの生成
        cache_key = f"subsidies:{keyword}:{sort}:{order}:{acceptance}"
        if use_purpose:
            cache_key += f":{','.join(use_purpose)}"
        if industry:
            cache_key += f":{','.join(industry)}"
        if target_number_of_employees:
            cache_key += f":{target_number_of_employees}"
        if target_area_search:
            cache_key += f":{target_area_search}"

        # キャッシュから取得を試みる
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # APIリクエストパラメータの構築
        params = {
            "keyword": keyword,
            "sort": sort,
            "order": order,
            "acceptance": acceptance
        }

        if use_purpose:
            params["use_purpose"] = " / ".join(use_purpose)
        if industry:
            params["industry"] = " / ".join(industry)
        if target_number_of_employees:
            params["target_number_of_employees"] = target_number_of_employees
        if target_area_search:
            params["target_area_search"] = target_area_search

        # API呼び出し
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/subsidies",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                # キャッシュに保存
                cache.set(cache_key, data)

                return data
        except httpx.HTTPError as e:
            print(f"jGrants API error: {e}")
            return None

    async def get_subsidy_detail(self, subsidy_id: str) -> Optional[dict]:
        """補助金詳細取得"""

        # キャッシュキーの生成
        cache_key = f"subsidy_detail:{subsidy_id}"

        # キャッシュから取得を試みる
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # API呼び出し
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/subsidies/id/{subsidy_id}"
                )
                response.raise_for_status()
                data = response.json()

                # キャッシュに保存
                cache.set(cache_key, data)

                return data
        except httpx.HTTPError as e:
            print(f"jGrants API error: {e}")
            return None


# Singleton instance
jgrants_service = JGrantsService()
