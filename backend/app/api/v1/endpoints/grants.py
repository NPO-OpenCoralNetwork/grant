from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.grant import (
    Grant,
    GrantSearchRequest,
    GrantSearchResponse,
    UpdateGrantsResponse
)
from app.services.toyama import toyama_service, CITY_FEEDS

router = APIRouter()


@router.get("/search", response_model=GrantSearchResponse)
async def search_grants(
    keyword: Optional[str] = Query(default=None, description="検索キーワード"),
    cities: Optional[str] = Query(default=None, description="対象自治体（複数の場合はカンマ区切り）"),
    start_date: Optional[str] = Query(default=None, description="開始日（YYYY-MM-DD）"),
    end_date: Optional[str] = Query(default=None, description="終了日（YYYY-MM-DD）"),
):
    """
    富山県の助成金を検索します

    - **keyword**: 検索キーワード
    - **cities**: 対象自治体（カンマ区切り）
    - **start_date**: 開始日（YYYY-MM-DD形式）
    - **end_date**: 終了日（YYYY-MM-DD形式）
    """

    # カンマ区切りの文字列をリストに変換
    cities_list = cities.split(',') if cities else None

    # 助成金を検索
    grants_data = toyama_service.search_grants(
        keyword=keyword,
        cities=cities_list,
        start_date=start_date,
        end_date=end_date
    )

    grants = [Grant(**g) for g in grants_data]

    return GrantSearchResponse(
        count=len(grants),
        grants=grants
    )


@router.get("/", response_model=GrantSearchResponse)
async def get_all_grants():
    """
    富山県のすべての助成金を取得します
    """
    grants_data = toyama_service.load_grants()
    grants = [Grant(**g) for g in grants_data]

    return GrantSearchResponse(
        count=len(grants),
        grants=grants
    )


@router.post("/update", response_model=UpdateGrantsResponse)
async def update_grants():
    """
    助成金情報を更新します（RSSフィードから最新情報を取得）
    """
    result = await toyama_service.update_grants()

    return UpdateGrantsResponse(**result)


@router.get("/cities", response_model=dict)
async def get_cities():
    """
    対応している自治体のリストを取得します
    """
    return {
        "cities": list(CITY_FEEDS.keys())
    }
