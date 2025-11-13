from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.subsidy import (
    SubsidySearchRequest,
    SubsidySearchResponse,
    SubsidySummary,
    SubsidyDetail,
    SubsidyDetailResponse
)
from app.services.jgrants import jgrants_service

router = APIRouter()


@router.get("/search", response_model=SubsidySearchResponse)
async def search_subsidies(
    keyword: str = Query(..., min_length=2, max_length=255, description="検索キーワード（2文字以上）"),
    sort: str = Query(default="created_date", description="ソート項目"),
    order: str = Query(default="DESC", description="ソート順"),
    acceptance: str = Query(default="1", description="募集期間内絞込要否"),
    use_purpose: Optional[str] = Query(default=None, description="利用目的（複数の場合はカンマ区切り）"),
    industry: Optional[str] = Query(default=None, description="業種（複数の場合はカンマ区切り）"),
    target_number_of_employees: Optional[str] = Query(default=None, description="従業員数"),
    target_area_search: Optional[str] = Query(default=None, description="対象地域"),
):
    """
    補助金を検索します

    - **keyword**: 検索キーワード（2文字以上必須）
    - **sort**: ソート項目（created_date, acceptance_start_datetime, acceptance_end_datetime）
    - **order**: ソート順（ASC, DESC）
    - **acceptance**: 募集期間内絞込（0: すべて, 1: 募集中のみ）
    """

    # カンマ区切りの文字列をリストに変換
    use_purpose_list = use_purpose.split(',') if use_purpose else None
    industry_list = industry.split(',') if industry else None

    # jGrants APIを呼び出し
    result = await jgrants_service.search_subsidies(
        keyword=keyword,
        sort=sort,
        order=order,
        acceptance=acceptance,
        use_purpose=use_purpose_list,
        industry=industry_list,
        target_number_of_employees=target_number_of_employees,
        target_area_search=target_area_search
    )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to fetch subsidies from jGrants API")

    # レスポンスを整形
    subsidies_data = result.get('result', [])
    subsidies = [SubsidySummary(**s) for s in subsidies_data]

    return SubsidySearchResponse(
        count=len(subsidies),
        subsidies=subsidies
    )


@router.get("/{subsidy_id}", response_model=SubsidyDetailResponse)
async def get_subsidy_detail(subsidy_id: str):
    """
    補助金の詳細情報を取得します

    - **subsidy_id**: 補助金ID
    """

    # jGrants APIを呼び出し
    result = await jgrants_service.get_subsidy_detail(subsidy_id)

    if not result:
        raise HTTPException(status_code=404, detail="Subsidy not found")

    # レスポンスを整形
    subsidy_data = result.get('result', [])
    if not subsidy_data:
        raise HTTPException(status_code=404, detail="Subsidy not found")

    subsidy = SubsidyDetail(**subsidy_data[0])

    return SubsidyDetailResponse(subsidy=subsidy)
