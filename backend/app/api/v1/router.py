from fastapi import APIRouter
from app.api.v1.endpoints import subsidies, grants

api_router = APIRouter()

# 補助金関連のエンドポイント
api_router.include_router(
    subsidies.router,
    prefix="/subsidies",
    tags=["subsidies"]
)

# 助成金関連のエンドポイント
api_router.include_router(
    grants.router,
    prefix="/grants",
    tags=["grants"]
)
