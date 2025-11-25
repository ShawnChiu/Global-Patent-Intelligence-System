# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px
import re

try:
    from config import DEFAULT_USER_CODE, DEFAULT_TECH_CONFIG, DEFAULT_EFFECT_CONFIG, DEFAULT_GEMINI_API
except ImportError:
    DEFAULT_USER_CODE = ""
    DEFAULT_TECH_CONFIG = "PGU: projector\nCombiner: waveguide"
    DEFAULT_EFFECT_CONFIG = "FOV: fov\nVID: vid"
    DEFAULT_GEMINI_API = ""

FIELD_OPTS = {
    "TI/AB/CL": "標題/摘要/範圍 (複合)",
    "TI": "標題 (Title)", "AB": "摘要 (Abstract)", "CL": "專利範圍 (Claims)",
    "CI": "IPC 分類號", "PR": "優先權 (Priority)", "PN": "公告號",
    "PA": "申請人", "IN": "發明人"
}

def parse_advanced_query(raw_query):
    """將 GPSS 網頁版的複雜檢索式拆解為 API 可用的參數"""
    if not raw_query: return "", ""
    ipc_pattern = r"IC=([A-Z0-9]+)\*?"
    ipcs = re.findall(ipc_pattern, raw_query)
    clean_ipc = ",".join(sorted(list(set(ipcs))))
    temp = re.sub(r"\$?IC=[A-Z0-9\*]+", "", raw_query)
    temp = re.sub(r"\$?ID=:?[0-9\$\*]+", "", temp)
    temp = re.sub(r"@[A-Z,]+", "", temp)
    temp = re.sub(r"\)\s*AND\s*$", ")", temp.strip())
    temp = re.sub(r"^\s*AND\s*", "", temp)
    clean_keywords = re.sub(r"\s+", " ", temp).strip()
    return clean_keywords, clean_ipc

def render_sidebar():

    with st.sidebar:
        st.header("⚙️ 參數設定")
        api_key = st.text_input("GPSS API Key", value=DEFAULT_USER_CODE, type="password")
        qty = st.slider("抓取數量", 10, 5000, 100)

        st.divider()
        st.header("🔍 搜尋條件")
        expression = st.text_input("輸入布林檢索式", value="HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이", type="default")

        st.divider()
        st.header("🤖 分析設定")
        
        matrix_mode = st.radio(
            "選擇矩陣分析模式",
            ["關鍵字規則 (Rule-based)", "AI 語意推論 (Gemini LLM)"],
            captions=["快速、免費，需定義關鍵字", "精準、自動分類，需 Google API Key"]
        )
        
        tech_conf = ""
        effect_conf = ""
        llm_key = ""

        if matrix_mode == "關鍵字規則 (Rule-based)":
            with st.expander("定義關鍵字規則", expanded=True):
                tech_conf = st.text_area("技術手段 (X軸)", value=DEFAULT_TECH_CONFIG, height=150)
                effect_conf = st.text_area("達成功效 (Y軸)", value=DEFAULT_EFFECT_CONFIG, height=150)
                
        else: # AI Mode
            st.markdown("""
            **🧠 AI 全自動分類** 系統將自動閱讀專利摘要並分析功效定義
            """)
            llm_key = st.text_input("Google Gemini API Key", value=DEFAULT_GEMINI_API, type="password", placeholder="貼上你的 AI Studio Key")
            if not llm_key:
                st.warning("請輸入 Key 以啟動 AI 功能")
        
        submitted = st.button("🚀 開始分析", type="primary")
        
    return {
        "api_key": api_key, 
        "expression": expression, 
        "qty": qty,
        "tech_conf": tech_conf, 
        "effect_conf": effect_conf,
        "matrix_mode": matrix_mode, # 回傳模式
        "llm_key": llm_key,         # 回傳 LLM Key
        "submitted": submitted
    }

def render_charts(df, matrix_df):
    # 渲染所有圖表
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["技術領域分類分析", "技術領先企業", "主要布局國家", "專利申請趨勢", "技術功效矩陣"])
    
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