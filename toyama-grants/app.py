import streamlit as st
import pandas as pd
from datetime import datetime
from utils import update_grants, load_grants, CITY_FEEDS
from config import load_config, save_config, get_keywords

st.set_page_config(
    page_title="富山県助成金情報",
    page_icon="💰",
    layout="wide"
)

def load_data():
    """データを読み込み、DataFrameに変換します"""
    grants = load_grants()
    if not grants:
        grants = update_grants()
    
    df = pd.DataFrame(grants)
    if not df.empty:
        df['published'] = pd.to_datetime(df['published'])
    return df

def filter_data(df, keyword='', start_date=None, end_date=None, selected_cities=None):
    """データをフィルタリングします"""
    if df.empty:
        return df
    
    # キーワードフィルター
    if keyword:
        df = df[df['title'].str.contains(keyword, case=False) | 
                df['description'].str.contains(keyword, case=False)]
    
    # 日付フィルター
    if start_date:
        df = df[df['published'].dt.date >= start_date]
    if end_date:
        df = df[df['published'].dt.date <= end_date]
    
    # 自治体フィルター
    if selected_cities and len(selected_cities) > 0:
        df = df[df['city'].isin(selected_cities)]
    
    return df

def main():
    st.title("助成金情報")
    
    # サイドバー: フィルター
    with st.sidebar:
        st.header("フィルター")
        
        # キーワード設定
        st.subheader("キーワード設定")
        config = load_config()
        keywords = st.text_area(
            "検索キーワード (1行に1つ)",
            value="\n".join(config["keywords"])
        )
        
        # キーワードの保存
        if st.button("キーワードを保存"):
            new_keywords = [k.strip() for k in keywords.split("\n") if k.strip()]
            config["keywords"] = new_keywords
            save_config(config)
            st.success("キーワードを保存しました")
        
        st.markdown("---")
        
        # データ更新ボタン
        if st.button("データを更新"):
            update_grants()
            st.success("データを更新しました")
        
        # 自治体選択
        st.subheader("自治体")
        selected_cities = st.multiselect(
            "表示する自治体を選択",
            options=list(CITY_FEEDS.keys()),
            default=list(CITY_FEEDS.keys())
        )
        
        # キーワード検索
        st.subheader("キーワード")
        keyword = st.text_input("キーワード検索", "")
        
        # 日付フィルター
        st.subheader("期間")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("開始日", None)
        with col2:
            end_date = st.date_input("終了日", None)
    
    # データ読み込み
    df = load_data()
    
    if df.empty:
        st.warning("助成金情報が見つかりませんでした。")
        return
    
    # データのフィルタリング
    filtered_df = filter_data(df, keyword, start_date, end_date)
    
    # 結果の表示
    st.subheader(f"助成金情報一覧（{len(filtered_df)}件）")
    
    # CSVダウンロードボタン
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSVダウンロード",
            data=csv,
            file_name="toyama_grants.csv",
            mime="text/csv"
        )
    
    # 助成金情報の表示
    for _, row in filtered_df.iterrows():
        with st.expander(f"📢 [{row['city']}] {row['title']}"):
            published_date = row['published']
            if isinstance(published_date, str):
                st.write(f"**公開日**: {published_date}")
            elif pd.isna(published_date):
                st.write(f"**公開日**: 未設定")
            else:
                st.write(f"**公開日**: {published_date.strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**自治体**: {row['city']}")
            st.write(f"**概要**: {row['description']}")
            st.markdown(f"[詳細を見る]({row['link']})")

if __name__ == "__main__":
    main()
