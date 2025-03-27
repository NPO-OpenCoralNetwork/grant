import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
from dotenv import load_dotenv
import os

# 環境変数のロード
load_dotenv()

# APIのベースURL
BASE_URL = "https://api.jgrants-portal.go.jp/exp/v1/public"

# 定数の定義
USE_PURPOSES = [
    "新たな事業を行いたい",
    "販路拡大・海外展開をしたい",
    "イベント・事業運営支援がほしい",
    "事業を引き継ぎたい",
    "研究開発・実証事業を行いたい",
    "人材育成を行いたい",
    "資金繰りを改善したい",
    "設備整備・IT導入したい",
    "雇用・職場環境を改善したい",
    "エコ・SDG's活動支援がほしい",
    "災害（自然災害、感染症等）支援がほしい",
    "教育・子育て・少子化への支援がほしい",
    "スポーツ・文化への支援がほしい",
    "安全・防災対策支援がほしい",
    "まちづくり・地域振興支援がほしい"
]

INDUSTRIES = [
    "農業，林業",
    "漁業",
    "鉱業，採石業，砂利採取業",
    "建設業",
    "製造業",
    "電気・ガス・熱供給・水道業",
    "情報通信業",
    "運輸業，郵便業",
    "卸売業，小売業",
    "金融業，保険業",
    "不動産業，物品賃貸業",
    "学術研究，専門・技術サービス業",
    "宿泊業，飲食サービス業",
    "生活関連サービス業，娯楽業",
    "教育，学習支援業",
    "医療，福祉",
    "複合サービス事業",
    "サービス業（他に分類されないもの）",
    "公務（他に分類されるものを除く）",
    "分類不能の産業"
]

EMPLOYEE_NUMBERS = [
    "従業員の制約なし",
    "5名以下",
    "20名以下",
    "50名以下",
    "100名以下",
    "300名以下",
    "900名以下",
    "901名以上"
]

AREAS = [
    "全国",
    "北海道地方", "東北地方", "関東・甲信越地方", "東海・北陸地方",
    "近畿地方", "中国地方", "四国地方", "九州・沖縄地方",
    "北海道",
    "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

def format_datetime(dt_str):
    if dt_str:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y/%m/%d %H:%M')
    return ''

def search_subsidies(keyword, sort='created_date', order='DESC', acceptance='1',
                    use_purpose=None, industry=None, target_number_of_employees=None,
                    target_area_search=None):
    params = {
        'keyword': keyword,
        'sort': sort,
        'order': order,
        'acceptance': acceptance
    }
    
    if use_purpose:
        params['use_purpose'] = ' / '.join(use_purpose)
    if industry:
        params['industry'] = ' / '.join(industry)
    if target_number_of_employees:
        params['target_number_of_employees'] = target_number_of_employees
    if target_area_search:
        params['target_area_search'] = target_area_search

    try:
        response = requests.get(f"{BASE_URL}/subsidies", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"APIリクエストエラー: {str(e)}")
        return None

# 新しい関数: 補助金詳細の取得
@st.cache_data(ttl=3600)
def get_subsidy_details(subsidy_id):
    try:
        response = requests.get(f"{BASE_URL}/subsidies/id/{subsidy_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"補助金詳細の取得エラー: {str(e)}")
        return None

def main():
    st.title("補助金検索アプリ")
    st.write("jGrantsの補助金情報を検索できます")

    with st.sidebar:
        keyword = st.text_input("キーワード検索（2文字以上）", "")
        
        st.subheader("検索オプション")
        sort_option = st.selectbox(
            "ソート項目",
            [
                ("created_date", "作成日時"),
                ("acceptance_start_datetime", "募集開始日時"),
                ("acceptance_end_datetime", "募集終了日時")
            ],
            format_func=lambda x: x[1]
        )
        
        order = st.selectbox(
            "ソート順",
            [("DESC", "降順"), ("ASC", "昇順")],
            format_func=lambda x: x[1]
        )
        
        acceptance = st.selectbox(
            "募集期間",
            [("1", "募集中のみ"), ("0", "すべて")],
            format_func=lambda x: x[1]
        )
        
        use_purpose = st.multiselect("利用目的", USE_PURPOSES)
        industry = st.multiselect("業種", INDUSTRIES)
        target_number_of_employees = st.selectbox("従業員数", [""] + EMPLOYEE_NUMBERS)
        target_area_search = st.selectbox("対象地域", [""] + AREAS)

        search_button = st.button("検索")

    if search_button and len(keyword) >= 2:
        with st.spinner("検索中..."):
            results = search_subsidies(
                keyword,
                sort=sort_option[0],
                order=order[0],
                acceptance=acceptance[0],
                use_purpose=use_purpose,
                industry=industry,
                target_number_of_employees=target_number_of_employees if target_number_of_employees else None,
                target_area_search=target_area_search if target_area_search else None
            )

        if results and 'result' in results:
            subsidies = results['result']
            if not subsidies:
                st.warning("検索結果が見つかりませんでした。")
            else:
                st.success(f"{len(subsidies)}件の補助金が見つかりました。")
                for subsidy in subsidies:
                    with st.expander(f"🏢 {subsidy.get('title', '無題')}"):
                        # 基本情報を表示
                        cols = st.columns([2, 1])
                        with cols[0]:
                            st.write("**補助金番号:**", subsidy.get('name', '不明'))
                            st.write("**対象地域:**", subsidy.get('target_area_search', '不明'))
                            if subsidy.get('subsidy_max_limit'):
                                st.write("**補助額上限:**", f"¥{subsidy['subsidy_max_limit']:,}")
                            st.write("**従業員数制限:**", subsidy.get('target_number_of_employees', '不明'))
                        
                        with cols[1]:
                            st.write("**募集期間**")
                            st.write("開始:", format_datetime(subsidy.get('acceptance_start_datetime')))
                            st.write("終了:", format_datetime(subsidy.get('acceptance_end_datetime')))
                        
                        # 詳細情報を取得して表示
                        if subsidy.get('id'):
                            with st.spinner("詳細情報を取得中..."):
                                details = get_subsidy_details(subsidy['id'])
                                
                            if details and 'result' in details and details['result']:
                                detail_data = details['result'][0]
                                
                                # 補助率を表示
                                if detail_data.get('subsidy_rate'):
                                    st.write("**補助率:**", detail_data['subsidy_rate'])
                                
                                # 詳細説明を表示
                                if detail_data.get('detail'):
                                    st.write("**補助金の概要:**")
                                    st.write(detail_data['detail'])
                                
                                # キャッチフレーズを表示
                                if detail_data.get('subsidy_catch_phrase'):
                                    st.write("**キャッチフレーズ:**", detail_data['subsidy_catch_phrase'])
                                
                                # 事業終了期限を表示
                                if detail_data.get('project_end_deadline'):
                                    st.write("**事業終了期限:**", format_datetime(detail_data['project_end_deadline']))
                                
                                # 詳細ページへのリンクを表示
                                if detail_data.get('front_subsidy_detail_page_url'):
                                    st.write("**詳細ページ:**")
                                    st.markdown(f"[jGrants補助金詳細ページ]({detail_data['front_subsidy_detail_page_url']})")
    elif search_button and len(keyword) < 2:
        st.error("検索キーワードは2文字以上入力してください。")

if __name__ == "__main__":
    main()