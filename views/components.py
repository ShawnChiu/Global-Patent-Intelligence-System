# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px
import re
import pandas as pd

# 嘗試匯入設定，若失敗則使用預設值
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

        search_mode = st.radio(
            "選擇搜尋模式",
            ["搜尋布林檢索式", "AI 檢索式推論 (Gemini LLM)"],
        )
        query = ""
        if search_mode == "搜尋布林檢索式":
            query = st.text_input("輸入布林檢索式", value="HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이", type="default")
        else:
            st.markdown("""
            **🧠 AI 自動生成布林檢索式** 系統將根據主題自動生成複雜的布林檢索式
            """)
            query = st.text_input("輸入技術主題", value="HUD 抬頭顯示器", type="default")

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
            if not llm_key:
                st.warning("請輸入 Key 以啟動 AI 功能")
        
        st.divider()
        st.header("🔑 API 設定")

        llm_key = st.text_input("Google Gemini API Key", value=DEFAULT_GEMINI_API, type="password", placeholder="貼上你的 AI Studio Key")
            
        submitted = st.button("🚀 開始分析", type="primary")
        
    return {
        "query": query, 
        "tech_conf": tech_conf, 
        "effect_conf": effect_conf,
        "matrix_mode": matrix_mode, 
        "search_mode": search_mode,
        "llm_key": llm_key,
        "submitted": submitted
    }

# 請將此函式覆蓋 views/components.py 中的 render_charts_from_files

def render_charts_from_files(files_dict):
    """
    爬蟲模式專用渲染函式 (修正版)
    """
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "技術領域分類分析", 
        "技術領先企業", 
        "主要布局國家", 
        "專利申請趨勢", 
        "技術功效矩陣"
    ])
    
    def parse_html_table(uploaded_file):
        """
        超強固版 HTML 解析器：處理指標重置、編碼與字串型態
        """
        if uploaded_file is None:
            return None

        try:
            html_content = ""

            # 1. 處理字串型態 (已經讀取過的)
            if isinstance(uploaded_file, str):
                html_content = uploaded_file
            
            # 2. 處理 Bytes 型態
            elif isinstance(uploaded_file, bytes):
                html_content = uploaded_file.decode("utf-8")

            # 3. 處理 Streamlit UploadedFile 物件
            elif hasattr(uploaded_file, "read"):
                # 重置指標 (關鍵步驟)
                if hasattr(uploaded_file, "seek"):
                    uploaded_file.seek(0)
                content = uploaded_file.read()
                
                if isinstance(content, bytes):
                    html_content = content.decode("utf-8", errors='ignore') # 忽略無法解碼的字元
                else:
                    html_content = content
            
            # 4. 開始解析
            if html_content:
                # 移除可能的 BOM (Byte Order Mark)
                html_content = html_content.strip()
                
                # 使用 lxml 解析器通常較穩，若失敗則退回預設
                try:
                    dfs = pd.read_html(html_content, header=0, flavor='lxml')
                except:
                    dfs = pd.read_html(html_content, header=0)

                if not dfs:
                    # 如果解析失敗，印出前 500 字 debug
                    st.error(f"解析失敗：HTML 中找不到表格。內容預覽：{html_content[:200]}...")
                    return None
                
                df = dfs[0]
                return df
                
        except Exception as e:
            st.error(f"檔案讀取發生錯誤: {str(e)}")
            return None
        
        return None

    # === Tab 1: IPC 技術分類 ===
    with tab1:
        st.subheader("📊 技術領域分類 (IPC)")
        if files_dict.get("ipc"):
            df_ipc = parse_html_table(files_dict["ipc"])
            
            if df_ipc is not None and len(df_ipc.columns) >= 2:
                # 使用 iloc (位置) 抓取，比欄位名稱更安全
                # 假設：第0欄是分類號，第1欄是數量
                
                # 複製一份以免改到原始資料
                df_plot = df_ipc.copy()
                
                # 重新命名欄位以便操作
                df_plot.columns = ['Category', 'Count'] + list(df_plot.columns[2:])
                
                # 清洗數據：轉字串 -> 去逗號 -> 轉數字
                df_plot['Count'] = pd.to_numeric(
                    df_plot['Count'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
                
                # 排序 (小到大，這樣水平圖才會由上往下排)
                df_plot = df_plot.sort_values('Count', ascending=True).tail(15)
                
                # 製作標籤
                df_plot['label'] = df_plot['Count'].apply(lambda x: f"({int(x)})" if pd.notnull(x) else "")

                fig = px.bar(
                    df_plot, 
                    x='Count', 
                    y='Category', 
                    orientation='h',
                    text='label',
                    color='Category',
                    title="IPC 技術分類 (Top 15)",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                
                fig.update_layout(
                    showlegend=False,
                    # plot_bgcolor="white",
                    margin=dict(l=150)
                )
                fig.update_traces(textposition='outside')
                
                st.plotly_chart(fig, theme="streamlit", width="stretch")
                
                # with st.expander("查看原始數據"):
                #     st.dataframe(df_ipc)
            else:
                st.error("表格讀取失敗或欄位不足")
        else:
            st.info("請上傳 IPC 統計表")

    # === Tab 2: 技術領先企業 (Assignee) ===
    with tab2:
        st.subheader("🏆 技術領先企業 (Assignee)")
        if files_dict.get('assignee'):
            df_assignee = parse_html_table(files_dict['assignee'])
            
            if df_assignee is not None and len(df_assignee.columns) >= 2:
                
                # 除錯：先讓你看一下讀到了什麼
                # with st.expander("查看原始數據 (Debug)", expanded=False):
                #     st.dataframe(df_assignee)
                
                # 使用 iloc 強制抓取前兩欄 (通常是 公司名, 數量)
                df_plot = df_assignee.iloc[:, :2].copy()
                df_plot.columns = ['Name', 'Count'] # 強制重新命名
                
                # === 關鍵修正：處理 "1,234" 這種字串 ===
                df_plot['Count'] = pd.to_numeric(
                    df_plot['Count'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
                
                # 去除空值並排序
                df_plot = df_plot.dropna(subset=['Count'])
                df_plot = df_plot.sort_values('Count', ascending=True).tail(15)
                
                # 檢查是否有資料
                if df_plot.empty:
                    st.error("數據轉換後為空，請檢查表格數值格式是否正確")
                else:
                    fig = px.bar(
                        df_plot, 
                        x='Count', 
                        y='Name', 
                        orientation='h', 
                        title="專利權人排名 (Top 15)", 
                        text='Count', 
                        color='Count', 
                        color_continuous_scale='Blues'
                    )
                    # fig.update_layout(plot_bgcolor="white")
                    st.plotly_chart(fig, theme="streamlit", width="stretch")
            else:
                st.error("表格欄位不足 (需要至少兩欄)")
        else:
            st.info("請上傳 申請人/專利權人 統計表")

    # === Tab 3: 主要布局國家 ===
    with tab3:
        st.subheader("🌍 主要布局國家")
        if files_dict.get("country"):
            df_country = parse_html_table(files_dict["country"])
            if df_country is not None and len(df_country.columns) >= 2:
                df_plot = df_country.iloc[:, :2].copy()
                df_plot.columns = ['Country', 'Count']
                
                # 清洗數據
                df_plot['Count'] = pd.to_numeric(
                    df_plot['Count'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
                
                fig = px.pie(df_plot.head(10), values='Count', names='Country', 
                             title="全球專利佈局佔比", hole=0.4)
                st.plotly_chart(fig, theme="streamlit", width="stretch")
        else:
            st.info("請上傳 國別 統計表")

    # === Tab 4: 專利申請趨勢 ===
    with tab4:
        st.subheader("📈 專利申請趨勢")
        if files_dict.get("trend_range"):
            df_trend = parse_html_table(files_dict["trend_range"])
            if df_trend is not None and len(df_trend.columns) >= 2:
                df_plot = df_trend.iloc[:, :2].copy()
                df_plot.columns = ['Year', 'Count']
                
                # 清洗數據
                df_plot['Count'] = pd.to_numeric(
                    df_plot['Count'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
                
                fig = px.line(df_plot, x='Year', y='Count', markers=True, 
                              title="申請趨勢")
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, theme="streamlit", width="stretch")
        else:
            st.info("請上傳 趨勢 統計表")

    # === Tab 5: 技術功效矩陣 (Bubble Chart) ===
    with tab5:
        st.subheader("💡 技術功效矩陣")
        
        # 1. 檔案讀取 (Result.xls)
        if files_dict.get("matrix"): # 記得在 sidebar 加入 matrix 的上傳
            # 使用我們強大的 robust_read_file (如果是在 class 外，直接用 pd.read_csv 搭配 try-except)
            try:
                # 這裡假設已經有 parse_html_table 或類似的讀取邏輯
                # 針對矩陣檔，通常是 CSV，我們直接讀取
                # 注意：這裡需要處理 header，因為第一列通常是 X 軸標籤
                df_matrix = pd.read_excel(files_dict["matrix"])
                
                # 2. 資料清洗與轉換 (Matrix -> Long Format)
                # 假設結構：
                # Row 0: [Header, Header, Tech_A, Tech_B, Tech_C...] (X軸標籤)
                # Row 1: [Header, Header, Search_A, Search_B...] (搜尋語法，通常忽略)
                # Row 2+: [Efficacy_X, Query_X, 10, 5, 2...] (Y軸標籤 + 數據)
                
                # 定位數據起始點 (這部分可能需要根據實際 CSV 微調)
                # 觀察你的 CSV preview:
                # Row 0: Unnamed, 技術名稱, i1, i2...
                # Row 1: 功效名稱, 檢索條件, ii1, ii2... (這是真正的 Header?)
                # Row 2+: j1, jj1, 0, 0...
                
                # 抓取 X 軸標籤 (技術手段) - 從 Row 0 的第 3 欄開始 (Index 2)
                x_labels = df_matrix.iloc[0, 2:].values.tolist()
                
                # 抓取數據與 Y 軸標籤 (功效) - 從 Row 2 開始
                data_rows = df_matrix.iloc[2:]
                
                plot_data = []
                for _, row in data_rows.iterrows():
                    y_label = str(row[0]) # 第 1 欄是功效名稱 (Y軸)
                    # 第 3 欄開始是數值
                    counts = row[2:].values
                    
                    for x_label, count in zip(x_labels, counts):
                        try:
                            # 轉數字，處理可能的 "1,234" 或空值
                            val = float(str(count).replace(',', ''))
                        except:
                            val = 0
                        
                        if val > 0: # 只記錄有數值的點
                            plot_data.append({
                                'Technology': x_label, # X軸
                                'Efficacy': y_label,   # Y軸
                                'Count': val           # 氣泡大小
                            })
                
                df_plot = pd.DataFrame(plot_data)
                
                if not df_plot.empty:
                    # 3. 繪製泡泡圖
                    fig = px.scatter(
                        df_plot, 
                        x='Technology', 
                        y='Efficacy', 
                        size='Count', 
                        color='Efficacy', # 依據 Y 軸分色，容易辨識
                        hover_name='Count',
                        title="技術功效矩陣分析",
                        size_max=60, # 調整最大氣泡尺寸
                        text='Count' # 在氣泡中顯示數字
                    )
                    
                    # 優化圖表佈局
                    fig.update_layout(
                        xaxis_title="技術手段 (Technology)",
                        yaxis_title="達成功效 (Efficacy)",
                        xaxis={'side': 'top'}, # X軸標籤放到上方，比較像矩陣
                        height=600, # 加高圖表
                        # plot_bgcolor='white',
                        showlegend=False
                    )
                    
                    # 讓氣泡內的文字置中
                    fig.update_traces(textposition='middle center')
                    
                    st.plotly_chart(fig, theme="streamlit", width="stretch")
                    
                    with st.expander("查看原始數據矩陣"):
                        st.dataframe(df_matrix)
                else:
                    st.warning("矩陣中無有效數據 (數值均為 0)")
                    
            except Exception as e:
                st.error(f"矩陣解析失敗: {str(e)}")
        else:
            st.info("請上傳 技術功效矩陣表 (Result.xls)")