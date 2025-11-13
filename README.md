# 補助金・助成金検索システム

日本全国の補助金情報と富山県の助成金情報を検索できるWebアプリケーションです。

## プロジェクト構成

```
grant/
├── backend/              # FastAPI バックエンド
│   ├── app/
│   │   ├── api/          # APIエンドポイント
│   │   ├── core/         # コア設定・キャッシュ
│   │   ├── schemas/      # Pydanticスキーマ
│   │   ├── services/     # ビジネスロジック
│   │   └── main.py       # アプリケーションエントリーポイント
│   ├── requirements.txt
│   └── Dockerfile
├── app.py                # 全国補助金検索フロントエンド（Streamlit）
├── toyama-grants/        # 富山県助成金フロントエンド（Streamlit）
└── docker-compose.yml    # Docker環境設定
```

## 機能

### 1. 全国補助金検索（jGrants API連携）
- キーワード検索
- 利用目的・業種・従業員数・地域による絞り込み
- 補助金詳細情報の表示
- Redisキャッシングによる高速化

### 2. 富山県助成金検索
- RSSフィード自動収集
- 自治体別フィルタリング
- 日付範囲指定
- CSVエクスポート

## セットアップ

### 1. Docker Composeを使用（推奨）

```bash
# リポジトリをクローン
git clone <repository-url>
cd grant

# Docker環境を起動
docker-compose up -d

# APIサーバーが起動（http://localhost:8000）
# APIドキュメント: http://localhost:8000/docs
```

### 2. ローカル開発環境

#### バックエンド

```bash
cd backend

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# Playwright（Webスクレイピング用）をセットアップ
playwright install chromium

# 環境変数を設定
cp .env.example .env
# .envファイルを編集

# Redisを起動（別ターミナル）
redis-server

# APIサーバーを起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### フロントエンド（全国補助金検索）

```bash
# 依存関係をインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

#### フロントエンド（富山県助成金）

```bash
cd toyama-grants

# 依存関係をインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

## API エンドポイント

### 補助金（jGrants）

#### `GET /api/v1/subsidies/search`
全国の補助金を検索

**パラメータ:**
- `keyword` (必須): 検索キーワード（2文字以上）
- `sort`: ソート項目（created_date, acceptance_start_datetime, acceptance_end_datetime）
- `order`: ソート順（ASC, DESC）
- `acceptance`: 募集期間内絞込（0: すべて, 1: 募集中のみ）
- `use_purpose`: 利用目的（カンマ区切り）
- `industry`: 業種（カンマ区切り）
- `target_number_of_employees`: 従業員数
- `target_area_search`: 対象地域

**例:**
```bash
curl "http://localhost:8000/api/v1/subsidies/search?keyword=DX&acceptance=1"
```

#### `GET /api/v1/subsidies/{subsidy_id}`
補助金の詳細情報を取得

**例:**
```bash
curl "http://localhost:8000/api/v1/subsidies/S0J0w00wer0wUgr77E"
```

### 助成金（富山県）

#### `GET /api/v1/grants/search`
富山県の助成金を検索

**パラメータ:**
- `keyword`: 検索キーワード
- `cities`: 対象自治体（カンマ区切り）
- `start_date`: 開始日（YYYY-MM-DD）
- `end_date`: 終了日（YYYY-MM-DD）

**例:**
```bash
curl "http://localhost:8000/api/v1/grants/search?keyword=DX&cities=富山市,高岡市"
```

#### `GET /api/v1/grants/`
すべての助成金を取得

#### `POST /api/v1/grants/update`
助成金情報を更新（RSSフィードから最新情報を取得）

#### `GET /api/v1/grants/cities`
対応している自治体のリストを取得

## 技術スタック

### バックエンド
- **FastAPI**: 高速なPython Webフレームワーク
- **Redis**: キャッシュストア
- **PostgreSQL**: データベース（オプション）
- **Pydantic**: データバリデーション
- **httpx**: 非同期HTTPクライアント
- **Playwright**: Webスクレイピング

### フロントエンド
- **Streamlit**: Pythonベースのダッシュボードフレームワーク
- **Pandas**: データ処理
- **Requests**: HTTP通信

## 開発

### APIドキュメント

APIサーバー起動後、以下のURLでドキュメントを確認できます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### テスト

```bash
cd backend
pytest
```

## 環境変数

`.env.example`を参考に`.env`ファイルを作成してください。

主要な環境変数：
- `REDIS_HOST`: Redisホスト（デフォルト: localhost）
- `REDIS_PORT`: Redisポート（デフォルト: 6379）
- `REDIS_CACHE_TTL`: キャッシュ有効期限（秒）
- `JGRANTS_BASE_URL`: jGrants APIのベースURL
- `BACKEND_CORS_ORIGINS`: CORS許可オリジン

## ライセンス

MIT License

## お問い合わせ

問題や要望がある場合は、GitHubのIssuesにご報告ください。
