# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px
import re
import pandas as pd

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

def render_sidebar():

    with st.sidebar:
        st.header("🔍 搜尋條件")
        query = st.text_input("輸入布林檢索式", value="HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이", type="default")

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
        "query": query, 
        "tech_conf": tech_conf, 
        "effect_conf": effect_conf,
        "matrix_mode": matrix_mode, # 回傳模式
        "llm_key": llm_key,         # 回傳 LLM Key
        "submitted": submitted
    }

def render_charts_from_files(files_dict):
    """
    爬蟲模式專用渲染函式
    :param files_dict: 包含上傳檔案的字典 {'ipc': file, 'country': file, 'trend_range': file, 'trend_year': file}
    """
    # 建立 5 個分頁 (目前先做前 4 個)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "技術領域分類分析", 
        "技術領先企業", 
        "主要布局國家", 
        "專利申請趨勢", 
        "技術功效矩陣"
    ])
    
    def parse_html_table(uploaded_file):
        """
        通用解析器：讀取 GPSS 的 HTML 表格並自動處理轉置
        """
        if uploaded_file is None:
            return None
        try:
            # 讀取 HTML，這會回傳一個 DataFrame 的 list
            dfs = pd.read_html(uploaded_file, encoding='utf-8')
            if not dfs: return None
            
            df = dfs[0] # 取第一個表格
            
            # --- 自動轉置判斷 (針對 diagram_1.html 這種橫向表) ---
            # 特徵：第一格是 "公開/公告年" 或 "申請年"，但它不在 columns 裡 (而是被當成資料)
            first_cell = str(df.iloc[0, 0])
            if ("年" in first_cell) and (first_cell not in df.columns):
                # 轉置矩陣
                df = df.T
                # 將第一列設為標題
                df.columns = df.iloc[0]
                df = df[1:]
                df.reset_index(drop=True, inplace=True)
                
            return df
        except Exception as e:
            st.error(f"解析失敗: {e}")
            return None
    
    # --- Tab 1: 技術領域 (IPC) - 對應 diagram_3.html ---
    with tab1:
        st.subheader("📊 技術領域分類 (IPC)")
        if files_dict.get('ipc'):
            df = parse_html_table(files_dict['ipc'])
            if df is not None:
                # 欄位通常是: IPC-3階, 專利數量
                x_col = df.columns[1] # 數量
                y_col = df.columns[0] # IPC
                
                # 轉成數字以確保排序正確
                df[x_col] = pd.to_numeric(df[x_col], errors='coerce')
                df = df.sort_values(x_col, ascending=True).tail(15) # 取前 15 大
                
                fig = px.bar(df, x=x_col, y=y_col, orientation='h', 
                             title="IPC 技術分類統計", text=x_col, 
                             color=x_col, color_continuous_scale='Reds')
                st.plotly_chart(fig, theme="streamlit", width="stretch")
        else:
            st.info("請上傳 IPC 統計表 (diagram_3.html)")

    # --- Tab 2: 技術領先企業 - (這部分你的檔案似乎沒提供對應的 html? 暫時留白或用 diagram_1 的第一申請人?) ---
    with tab2:
        st.subheader("🏆 技術領先企業")
        st.warning("目前無對應的 HTML 檔案 (需上傳申請人統計表)")
        # 如果未來有檔案，邏輯同 Tab 1，只是畫長條圖

    # --- Tab 3: 主要布局國家 - 對應 diagram_4.html ---
    with tab3:
        st.subheader("🌍 主要布局國家")
        if files_dict.get('country'):
            df = parse_html_table(files_dict['country'])
            if df is not None:
                # 欄位: 申請人國別, 專利數量
                val_col = df.columns[1]
                name_col = df.columns[0]
                
                fig = px.pie(df.head(10), values=val_col, names=name_col, 
                             title="全球專利佈局佔比", hole=0.4)
                st.plotly_chart(fig, theme="streamlit", width="stretch")
        else:
            st.info("請上傳 國別 統計表 (diagram_4.html)")

    # --- Tab 4: 專利申請趨勢 - 對應 diagram_1.html (詳細) & diagram_2.html (區間) ---
    with tab4:
        st.subheader("📈 專利申請趨勢")
        
        # 1. 詳細年度趨勢 (diagram_1)
        if files_dict.get('trend_year'):
            df = parse_html_table(files_dict['trend_year'])
            if df is not None:
                # 轉換數值
                # 欄位: 公開/公告年, 第一申請人, 專利數量
                year_col = df.columns[0]
                
                # 嘗試把所有數值欄位轉成數字
                for col in df.columns[1:]:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # 使用 melt 將寬表格轉長表格，以便畫多條線
                df_long = df.melt(id_vars=[year_col], var_name='指標', value_name='數量')
                
                fig = px.line(df_long, x=year_col, y='數量', color='指標', markers=True, 
                              title="詳細年度申請趨勢")
                st.plotly_chart(fig, theme="streamlit", width="stretch")
        else:
            st.info("請上傳 詳細年度表 (diagram_1.html)")
            
        st.divider()
        
        # 2. 區間趨勢 (diagram_2)
        if files_dict.get('trend_range'):
            df = parse_html_table(files_dict['trend_range'])
            if df is not None:
                x_col = df.columns[0] # 申請年 (區間)
                y_col = df.columns[1] # 數量
                
                fig = px.bar(df, x=x_col, y=y_col, text=y_col, 
                             title="年代區間統計", color=y_col)
                st.plotly_chart(fig, theme="streamlit", width="stretch")

    # --- Tab 5: 技術功效矩陣 (暫時保留，之後再做) ---
    with tab5:
        st.subheader("💡 技術功效矩陣")
        st.info("🚧 此功能尚未實作 (需要原始專利清單)")