from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Grant(BaseModel):
    """助成金情報"""
    title: str
    link: str
    published: str
    description: str
    city: str


class GrantSearchRequest(BaseModel):
    """助成金検索リクエスト"""
    keyword: Optional[str] = Field(default=None, description="検索キーワード")
    cities: Optional[list[str]] = Field(default=None, description="対象自治体リスト")
    start_date: Optional[str] = Field(default=None, description="開始日（YYYY-MM-DD）")
    end_date: Optional[str] = Field(default=None, description="終了日（YYYY-MM-DD）")


class GrantSearchResponse(BaseModel):
    """助成金検索レスポンス"""
    count: int
    grants: list[Grant]


class UpdateGrantsResponse(BaseModel):
    """助成金更新レスポンス"""
    success: bool
    count: int
    message: str
