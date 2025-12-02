# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px
import re
import pandas as pd

from services.settings_manager import setmgr

FIELD_OPTS = {
    "TI/AB/CL": "標題/摘要/範圍 (複合)",
    "TI": "標題 (Title)", "AB": "摘要 (Abstract)", "CL": "專利範圍 (Claims)",
    "CI": "IPC 分類號", "PR": "優先權 (Priority)", "PN": "公告號",
    "PA": "申請人", "IN": "發明人"
}

def render_sidebar():
    with st.sidebar:
        st.header("🍬 專利主題")
        topic = st.text_input("輸入技術主題", value="", type="default", placeholder="輸入你的專利技術主題")

        st.header("🎓 學生資料")
        name = st.text_input("姓名", value="", type="default", placeholder="輸入你的姓名")
        student_id = st.text_input("學號", value="", type="default", placeholder="輸入你的學號")
        

        st.header("🌸 GPSS 帳號密碼")

        user = st.text_input("GPSS 使用者代碼", value=setmgr.settings.user_id, type="default", placeholder="輸入你的 GPSS 使用者代碼")
        password = st.text_input("GPSS 密碼", value=setmgr.settings.user_pw, type="password", placeholder="輸入你的 GPSS 密碼")

        st.header("🔍 搜尋條件")

        search_mode = st.radio(
            "選擇搜尋模式",
            ["搜尋布林檢索式", "AI 檢索式推論 (Gemini LLM)"],
        )
        query = ""
        source = ""
        if search_mode == "搜尋布林檢索式":
            query = st.text_input("輸入布林檢索式", value="(IGS OR \"International Games System\" OR 鈊象 OR \"インターナショナル ゲーム システム\" OR \"인터내셔널 게임 시스템\")@TI,AB,CL,DE AND ID=:20241231 AND (IC=A63F* OR IC=G07F* OR IC=G06F*)"
            "", type="default")
            source = st.text_input("來源說明 (選填)", value="", type="default", placeholder="輸入來源")

        else:
            st.markdown("""
            **🧠 AI 自動生成布林檢索式** 系統將根據主題自動生成複雜的布林檢索式
            """)

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
        conf_source = ""

        if matrix_mode == "關鍵字規則 (Rule-based)":
            with st.expander("定義關鍵字規則", expanded=True):
                tech_conf = st.text_area("技術手段 (X軸)", value=setmgr.settings.tech_config, height=150)
                effect_conf = st.text_area("達成功效 (Y軸)", value=setmgr.settings.effect_config, height=150)
            conf_source = st.text_input("關鍵字來源說明 (選填)", value="", type="default", placeholder="輸入關鍵字來源")
                
        else: # AI Mode
            st.markdown("""
            **🧠 AI 全自動分類** 系統將自動閱讀專利摘要並分析功效定義
            """)
            if not llm_key:
                st.warning("請輸入 Key 以啟動 AI 功能")
        
        st.divider()
        st.header("🔑 API 設定")

        llm_key = st.text_input("Google Gemini API Key", value=setmgr.settings.gemini_api_key, type="password", placeholder="貼上你的 AI Studio Key")
            
        submitted = st.button("🚀 開始分析", type="primary")
        
    return {
        "name": name,
        "student_id": student_id,
        "user": user,
        "password": password,
        "source": source,
        "query": query, 
        "tech_conf": tech_conf,
        "effect_conf": effect_conf,
        "matrix_mode": matrix_mode, 
        "search_mode": search_mode,
        "llm_key": llm_key,
        "submitted": submitted,
        "conf_source": conf_source,
        "topic": topic
    }

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

                fig.write_image(".data\/chart1.png", format="png", width=1200, height=800, scale=2)
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

                    fig.write_image(".data\/chart2.png", format="png", width=1200, height=800, scale=2)
            else:
                st.error("表格欄位不足 (需要至少兩欄)")
        else:
            st.info("請上傳 申請人/專利權人 統計表")

    # === Tab 3: 主要布局國家 (橫條圖版) ===
    with tab3:
        st.subheader("🌍 主要布局國家")
        if files_dict.get("country"):
            df_country = parse_html_table(files_dict["country"])
            if df_country is not None and len(df_country.columns) >= 2:
                df_plot = df_country.iloc[:, :2].copy()
                df_plot.columns = ['Country', 'Count']
                
                # 1. 清洗數據
                df_plot['Count'] = pd.to_numeric(
                    df_plot['Count'].astype(str).str.replace(',', ''), 
                    errors='coerce'
                )
                
                # 2. 準備繪圖數據 (取前 10 名)
                # 注意：為了讓長條圖中「數量最多」的排在「最上面」，
                # 我們需要先將數據「由小到大」排序 (因為 Plotly 預設是從下畫到上)
                df_vis = df_plot.head(10).sort_values(by='Count', ascending=True)

                # 3. 繪製橫條圖 (orientation='h')
                fig = px.bar(
                    df_vis, 
                    x='Count', 
                    y='Country', 
                    orientation='h',  # 設定為橫向
                    title="全球專利佈局 (Top 10)",
                    text='Count',     # 在條形上顯示數字
                    color='Count',    # 依數值深淺上色
                    color_continuous_scale='Viridis' # 設定漸層色系 (例如 Blues, Viridis, Teal)
                )
                
                # 優化版面
                fig.update_layout(
                    xaxis_title="專利數量",
                    yaxis_title="", # 移除 Y 軸標題 (因為國家名稱很明顯)
                    showlegend=False,
                    height=500 # 設定高度
                )
                
                # 讓數字顯示在條形圖的右側或內部
                fig.update_traces(textposition='outside') 

                # 4. 顯示與存檔
                st.plotly_chart(fig, theme="streamlit", width="stretch")

                # 確保資料夾存在
                import os
                if not os.path.exists(".data"):
                    os.makedirs(".data")
                    
                fig.write_image(".data/chart3.png", format="png", width=1200, height=800, scale=2)
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
                    errors='coerce',
                )
                
                fig = px.line(df_plot, x='Year', y='Count', markers=True, 
                              title="申請趨勢", color_discrete_sequence=px.colors.qualitative.Pastel)
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, theme="streamlit", width="stretch")

                fig.write_image(".data\/chart4.png", format="png", width=1200, height=800, scale=2)
        else:
            st.info("請上傳 趨勢 統計表")

    # === Tab 5: 技術功效矩陣 (Adaptive Bubble Chart) ===
    with tab5:
        st.subheader("💡 技術功效矩陣")
        
        if files_dict.get("matrix"):
            try:
                # 1. 讀取檔案
                # 使用 header=None 讀取，方便我們自己定位
                df_matrix = pd.read_excel(files_dict["matrix"], header=None)
                
                # 2. 解析資料 (Data Parsing)
                # 假設 Row 0 是 X 軸標籤 (從第3格開始)
                x_labels = df_matrix.iloc[0, 2:].fillna("Unknown").astype(str).values.tolist()
                
                # 假設 Row 2 開始是數據 (Y軸標籤在第1格)
                data_rows = df_matrix.iloc[2:]
                
                plot_data = []
                # 為了確保 Y 軸順序正確 (跟 Excel 一樣由上到下)，我們可以用 enumerate
                for _, row in data_rows.iterrows():
                    y_label = str(row[0]) # 第 1 欄是功效名稱
                    counts = row[2:].values
                    
                    for x_label, count in zip(x_labels, counts):
                        try:
                            val = float(str(count).replace(',', ''))
                        except:
                            val = 0
                        
                        if val > 0:
                            plot_data.append({
                                'Technology': x_label,
                                'Efficacy': y_label,
                                'Count': val
                            })
                
                df_plot = pd.DataFrame(plot_data)
                
                if not df_plot.empty:
                    # --- 3. 智慧版面計算 (Adaptive Layout Calculation) ---
                    
                    # 計算維度
                    n_x = len(x_labels) # X軸有多少技術
                    n_y = len(data_rows) # Y軸有多少功效
                    
                    # 規則 A: 動態高度
                    # 基礎高度 400px，每多一個 Y 軸項目增加 60px
                    # 這樣即使有 20 個功效，圖表也會自動變很長，不會擠在一起
                    dynamic_height = max(500, 200 + (n_y * 60))
                    
                    # 規則 B: 動態泡泡大小
                    # 如果格子很密 (例如 10x10)，泡泡要小一點才不會打架
                    # 如果格子很空 (例如 3x3)，泡泡可以大一點比較氣派
                    density_factor = max(n_x, n_y)
                    if density_factor > 15:
                        dynamic_size_max = 30 # 密集恐懼症，縮小
                    elif density_factor > 8:
                        dynamic_size_max = 40 # 中等
                    else:
                        dynamic_size_max = 50 # 疏鬆，大泡泡

                    # 規則 C: 處理標籤過長
                    # 我們將使用 automargin，但也可以截斷過長的文字
                    def truncate_label(text, limit=15):
                        return text[:limit] + "..." if len(str(text)) > limit else str(text)

                    # 4. 繪圖
                    fig = px.scatter(
                        df_plot, 
                        x='Technology', 
                        y='Efficacy', 
                        size='Count', 
                        color='Efficacy',
                        hover_name='Count',
                        title=f"技術功效矩陣 ({n_x}x{n_y})",
                        size_max=dynamic_size_max, # 應用動態大小
                        color_discrete_sequence=px.colors.qualitative.Bold, # 使用鮮豔配色
                        text='Count'
                    )

                    fig.update_layout(
                        # 移除軸標題，節省空間
                        xaxis_title="", 
                        yaxis_title="",
                        
                        # X軸設定 (上方顯示)
                        xaxis={
                            'side': 'top',
                            'tickangle': -45, # 傾斜 45 度
                            'dtick': 1,       # 顯示所有刻度
                            'automargin': True, # [關鍵] 自動調整邊距以容納長文字
                            'fixedrange': True  # 禁止縮放軸，避免跑版
                        },
                        
                        # Y軸設定
                        yaxis={
                            'autorange': "reversed", # 讓表格第一項在最上面
                            'dtick': 1,
                            'automargin': True, # [關鍵] 自動調整邊距
                            'fixedrange': True
                        },
                        
                        # 應用動態高度
                        height=dynamic_height,
                        
                        # 邊距 (留給 automargin 發揮，這裡只給最小安全距離)
                        margin=dict(l=20, r=20, t=20, b=20),
                        
                        showlegend=False
                    )
                    
                    # 優化文字顯示
                    fig.update_traces(
                        textposition='middle center',
                        textfont={'color': 'white', 'weight': 'bold', 'size': 12}
                    )
                    
                    # [關鍵] use_container_width=True 會自動填滿網頁寬度
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander("查看原始數據矩陣"):
                        st.dataframe(df_matrix)
                    
                    fig.write_image(".data\/chart5.png", format="png", width=1200, height=800, scale=2)
                    

                else:
                    st.warning("⚠️ 矩陣數據為空 (所有數值皆為 0)")

                
                    
            except Exception as e:
                st.error(f"矩陣解析錯誤: {str(e)}")
        else:
            st.info("👈 請在左側上傳 `Result.xls` (矩陣分析結果)")