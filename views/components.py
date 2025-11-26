# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px

try:
    from config import DEFAULT_USER_CODE, DEFAULT_TECH_CONFIG, DEFAULT_EFFECT_CONFIG
except ImportError:
    DEFAULT_USER_CODE = ""
    DEFAULT_TECH_CONFIG = "PGU: projector\nCombiner: waveguide"
    DEFAULT_EFFECT_CONFIG = "FOV: fov\nVID: vid"

def render_sidebar():
    # 渲染側邊欄並回傳使用者的輸入
    with st.sidebar:
        st.header("⚙️ 參數設定")
        # 預設值改為符合你報告的設定
        query = st.text_input("檢索關鍵字", value="(HUD OR 抬頭顯示器) AND (AR OR 擴增實境)")
        ipc = st.text_input("IPC 分類號", value="G02B,B60K")
        qty = st.slider("抓取數量", 10, 10000, 100)
        
        st.header("📊 矩陣定義")
        tech_conf = st.text_area("技術手段定義", value=DEFAULT_TECH_CONFIG, height=200)
        effect_conf = st.text_area("功效定義", value=DEFAULT_EFFECT_CONFIG, height=150)
        
        submitted = st.button("🚀 開始分析", type="primary")
        
    return {
        "query": query, "ipc": ipc, "qty": qty,
        "tech_conf": tech_conf, "effect_conf": effect_conf, "submitted": submitted
    }

def render_charts(df, matrix_df):
    # 渲染所有圖表
    tab1, tab2, tab3, tab4 = st.tabs(["技術領域", "布局戰場", "申請趨勢", "技術功效矩陣"])
    
    with tab1:
        if 'IPC' in df.columns:
            counts = df['IPC'].value_counts().head(10).reset_index()
            counts.columns = ['IPC', 'Count']
            # 修正點 1: 移除 use_container_width，改用 theme 設定自動適應
            st.plotly_chart(px.bar(counts, x='Count', y='IPC', orientation='h', title="前十大技術領域 (IPC)", text='Count'), theme="streamlit")
        else:
            st.warning("資料中無 IPC 欄位")

    with tab2:
        if 'Country' in df.columns:
            counts = df['Country'].value_counts().head(10).reset_index()
            counts.columns = ['Country', 'Count']
            # 修正點 2
            st.plotly_chart(px.pie(counts, values='Count', names='Country', title="全球布局佔比"), theme="streamlit")
        else:
            st.warning("資料中無 Country 欄位")

    with tab3:
        if 'Year' in df.columns:
            valid_years = df[df['Year'].astype(str).str.isnumeric()]
            trend = valid_years.groupby('Year').size().reset_index(name='Count')
            # 修正點 3
            st.plotly_chart(px.line(trend, x='Year', y='Count', markers=True, title="歷年申請趨勢"), theme="streamlit")
        else:
            st.warning("資料中無 Year 欄位")

    with tab4:
        if matrix_df is not None and not matrix_df.empty:
            counts = matrix_df.groupby(['Technology', 'Efficacy']).size().reset_index(name='Count')
            fig = px.scatter(
                counts, 
                x="Technology", 
                y="Efficacy", 
                size="Count", 
                color="Efficacy", 
                size_max=60, 
                title="技術功效矩陣"
            )
            fig.update_layout(xaxis_title="技術手段", yaxis_title="達成功效")
            # 修正點 4
            st.plotly_chart(fig, theme="streamlit")
        else:
            st.warning("⚠️ 無法產生矩陣：未匹配到任何關鍵字，請檢查左側定義。")