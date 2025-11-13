from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SubsidySearchRequest(BaseModel):
    """補助金検索リクエスト"""
    keyword: str = Field(..., min_length=2, max_length=255, description="検索キーワード（2文字以上）")
    sort: str = Field(default="created_date", description="ソート項目")
    order: str = Field(default="DESC", description="ソート順")
    acceptance: str = Field(default="1", description="募集期間内絞込要否")
    use_purpose: Optional[list[str]] = Field(default=None, description="利用目的")
    industry: Optional[list[str]] = Field(default=None, description="業種")
    target_number_of_employees: Optional[str] = Field(default=None, description="従業員数")
    target_area_search: Optional[str] = Field(default=None, description="対象地域")


class SubsidySummary(BaseModel):
    """補助金サマリー情報"""
    id: str
    name: str
    title: Optional[str] = None
    target_area_search: Optional[str] = None
    subsidy_max_limit: Optional[float] = None
    acceptance_start_datetime: Optional[str] = None
    acceptance_end_datetime: Optional[str] = None
    target_number_of_employees: Optional[str] = None


class SubsidyDetail(BaseModel):
    """補助金詳細情報"""
    id: str
    name: str
    title: Optional[str] = None
    subsidy_catch_phrase: Optional[str] = None
    detail: Optional[str] = None
    use_purpose: Optional[str] = None
    industry: Optional[str] = None
    target_area_search: Optional[str] = None
    target_area_detail: Optional[str] = None
    target_number_of_employees: Optional[str] = None
    subsidy_rate: Optional[str] = None
    subsidy_max_limit: Optional[float] = None
    acceptance_start_datetime: Optional[str] = None
    acceptance_end_datetime: Optional[str] = None
    project_end_deadline: Optional[str] = None
    request_reception_presence: Optional[str] = None
    is_enable_multiple_request: Optional[bool] = None
    front_subsidy_detail_page_url: Optional[str] = None


class SubsidySearchResponse(BaseModel):
    """補助金検索レスポンス"""
    count: int
    subsidies: list[SubsidySummary]


class SubsidyDetailResponse(BaseModel):
    """補助金詳細レスポンス"""
    subsidy: Optional[SubsidyDetail] = None
