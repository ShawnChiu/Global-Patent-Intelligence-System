# 檔案位置：views/components.py
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import io


@st.dialog("❓ 如何取得 Google Gemini API Key")
def show_gemini_tutorial():
    st.markdown("""
        <style>
        /* 針對 Dialog (模態視窗) 內的關閉按鈕進行隱藏 */
        div[role="dialog"] button[aria-label="Close"] {
            display: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("""
    ### 步驟教學：
    1. 前往 **[Google AI Studio](https://aistudio.google.com/)**。
    2. 點擊左下角的 **"Get API key"** 按鈕。
    3. 點擊 **"Create API key"**。
    4. 名字隨意，專案選擇 **"Gemini API"**後點選 Create。
    6. 複製生成的 Key 並貼回本系統。
    
    *(建議：申請後請妥善保存，不要洩漏給他人)*
    """)
    if st.button("💾 儲存並關閉", type="primary", use_container_width=True):
        st.rerun()

@st.dialog("✏️ 編輯矩陣分析")
def show_matrix_editor():
    st.markdown("""
        <style>
        /* 針對 Dialog (模態視窗) 內的關閉按鈕進行隱藏 */
        div[role="dialog"] button[aria-label="Close"] {
            display: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
# 設定 width="large" 讓視窗變寬，適合左右並排
    st.write("請在下方分別定義 X 軸與 Y 軸的關鍵字：")
    
    # 建立左右兩欄
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.subheader("🛠️ 技術手段 (X軸)")
        st.session_state.tech = st.text_area(
            "輸入技術關鍵字 (每行一個)",
            value=st.session_state.tech,
            height=300, # 高度拉長
            label_visibility="collapsed",
            key="dlg_tech_input"
        )

    with col2:
        st.subheader("✨ 達成功效 (Y軸)")
        st.session_state.eff = st.text_area(
            "輸入功效關鍵字 (每行一個)",
            value=st.session_state.eff,
            height=300, # 高度拉長
            label_visibility="collapsed",
            key="dlg_effect_input"
        )

    st.session_state.conf_source = st.text_input("來源說明 (選填)", value=st.session_state.conf_source, type="default", placeholder="輸入來源")

    # 儲存按鈕
    st.button("💾 儲存並關閉", type="primary", use_container_width=True, on_click=st.rerun)

@st.dialog("✏️ 編輯布林檢索式")
def show_query_editor():
    st.markdown("""
        <style>
        /* 針對 Dialog (模態視窗) 內的關閉按鈕進行隱藏 */
        div[role="dialog"] button[aria-label="Close"] {
            display: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.write("請在下方編輯您的完整檢索式：")
    
    # 使用 text_area 讓輸入框變很大，方便編輯多行
    st.session_state.query = st.text_area(
        "檢索式內容",
        value=st.session_state.query, # 從 session 讀取
        height=400, # 設定高度為 400px，夠大！
        label_visibility="collapsed"
    )
    
    st.session_state.source = st.text_input("來源說明 (選填)", value=st.session_state.source, type="default", placeholder="輸入來源")

    if st.button("💾 儲存並關閉", type="primary", use_container_width=True):
        st.rerun()

@st.dialog("📝 基本資料設定")
def show_basic_info():
    st.markdown("""
        <style>
        /* 針對 Dialog (模態視窗) 內的關閉按鈕進行隱藏 */
        div[role="dialog"] button[aria-label="Close"] {
            display: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.write("請在下方編輯您的完整檢索式：")
    
    st.header("🎓 學生資料")
    st.session_state.name = st.text_input("姓名", value=st.session_state.name, type="default", placeholder="輸入你的姓名")
    st.session_state.student_id = st.text_input("學號", value=st.session_state.student_id, type="default", placeholder="輸入你的學號") 

    st.header("🌸 GPSS 帳號密碼")
    st.session_state.gpss_id = st.text_input("GPSS 使用者代碼", value=st.session_state.gpss_id, type="default", placeholder="輸入你的 GPSS 使用者代碼")
    st.session_state.gpss_pw = st.text_input("GPSS 密碼", value=st.session_state.gpss_pw, type="password", placeholder="輸入你的 GPSS 密碼")   

    if st.button("💾 儲存並關閉", type="primary", use_container_width=True):
        st.rerun()

def render_sidebar():   
    with st.sidebar:
        st.header("🍬 專利主題")
        st.session_state.topic = st.text_input("輸入技術主題", value="", type="default", placeholder="輸入你的專利技術主題")

        st.header("📝 基本資料")
        st.button("✏️ 點擊編輯基本資料", help="點擊編輯基本資料", key="btn_edit_basic_info", on_click=show_basic_info)

        st.header("🔍 搜尋條件")

        st.session_state.search_mode = st.radio(
            "選擇搜尋模式",
            ["搜尋布林檢索式", "AI 檢索式推論 (Gemini LLM)"],
        )
        
        if st.session_state.search_mode == "搜尋布林檢索式":
            st.button("✏️ 點擊編輯檢索式", help="點擊編輯檢索式", key="btn_edit_query", on_click=show_query_editor)
        else:
            st.markdown("""
            **🧠 AI 自動生成布林檢索式** 系統將根據主題自動生成複雜的布林檢索式
            """)
            # 如果是 AI 模式，這裡的 query 可能會在 main.py 產生，或是清空
            # query = "" 

        st.divider()
        st.header("🤖 分析設定")
        
        st.session_state.matrix_mode = st.radio(
            "選擇矩陣分析模式",
            ["關鍵字規則 (Rule-based)", "AI 語意推論 (Gemini LLM)"],
            captions=["快速、免費，需定義關鍵字", "精準、自動分類，需 Google API Key"]
        )

        if st.session_state.matrix_mode == "關鍵字規則 (Rule-based)":
            st.button("✏️ 點擊編輯關鍵字", help="點擊編輯關鍵字", key="btn_edit_matrix", on_click=show_matrix_editor)    
        else: # AI Mode
            st.markdown("""
            **🧠 AI 全自動分類** 系統將自動閱讀專利摘要並分析功效定義
            """)
            if not st.session_state.gemini_api_key:
                st.warning("請輸入 Key 以啟動 AI 功能")
        
        st.divider()
        st.header("🔑 API 設定")
            
        if st.button("❓ 查看教學", key="btn_api_help", help="點擊查看教學"):
            show_gemini_tutorial()


        # --- 下面放輸入框 ---
        st.session_state.gemini_api_key = st.text_input(
            "Google Gemini API Key", 
            value=st.session_state.gemini_api_key, 
            type="password", 
            placeholder="貼上你的 AI Studio Key",
            label_visibility="collapsed"
        )

        st.session_state.submitted = st.button("🚀 開始分析", type="primary")
        
    return {
        "name": st.session_state.name,
        "student_id": st.session_state.student_id,
        "user": st.session_state.gpss_id,
        "password": st.session_state.gpss_pw,
        "source": st.session_state.source,
        "query": st.session_state.query, 
        "tech_conf": st.session_state.tech,
        "effect_conf": st.session_state.eff,
        "matrix_mode": st.session_state.matrix_mode, 
        "search_mode": st.session_state.search_mode,
        "llm_key": st.session_state.gemini_api_key,
        "submitted": st.session_state.submitted,
        "conf_source": st.session_state.conf_source,
        "topic": st.session_state.topic
    }

def parse_diagrams(buffers):

    """
    爬蟲模式專用渲染函式 (Buffer 支援版)
    Args:
        files_dict (dict): 字典，Values 可以是 檔案路徑(str) 或 記憶體緩衝區(BytesIO)
    """
    
    if "results" not in st.session_state:
        st.session_state.results = {}
    
    fig_buffers = {}
    img_buffers = {}

    def parse_html_table(uploaded_file):
        """
        HTML 解析器：支援 Path, Bytes, BytesIO
        """
        if uploaded_file is None:
            return None

        try:
            html_content = ""

            # 1. 處理字串 (檔案路徑 或 HTML 原始碼)
            if isinstance(uploaded_file, str):
                # 如果是路徑，且檔案存在，就讀取
                if os.path.exists(uploaded_file) and uploaded_file.endswith(('.html', '.htm')):
                    with open(uploaded_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                else:
                    # 否則假設它就是 HTML 字串
                    html_content = uploaded_file
            
            # 2. 處理 Bytes (原始資料)
            elif isinstance(uploaded_file, bytes):
                html_content = uploaded_file.decode("utf-8")

            # 3. 處理 Buffer (BytesIO) 或 UploadedFile
            elif hasattr(uploaded_file, "read"):
                # 【關鍵】重置指標，確保從頭讀取
                if hasattr(uploaded_file, "seek"):
                    uploaded_file.seek(0)
                
                content = uploaded_file.read()
                
                if isinstance(content, bytes):
                    html_content = content.decode("utf-8", errors='ignore')
                else:
                    html_content = content
            
            # 4. 解析 Pandas
            if html_content:
                try:
                    dfs = pd.read_html(html_content, header=0, flavor='lxml')
                except:
                    dfs = pd.read_html(html_content, header=0)

                if dfs:
                    return dfs[0]
                
        except Exception as e:
            st.error(f"檔案解析錯誤: {str(e)}")
            return None
        
        return None

    # === Tab 1: IPC 技術分類 ===
    if buffers.get("ipc"):
        df_ipc = parse_html_table(buffers["ipc"])
            
        if df_ipc is not None and len(df_ipc.columns) >= 2:
            df_plot = df_ipc.copy()
            df_plot.columns = ['Category', 'Count'] + list(df_plot.columns[2:])
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_plot = df_plot.sort_values('Count', ascending=True).tail(15)
            df_plot['label'] = df_plot['Count'].apply(lambda x: f"({int(x)})" if pd.notnull(x) else "")

            fig = px.bar(df_plot, x='Count', y='Category', orientation='h', text='label', color='Category', 
                         title="IPC 技術分類 (Top 15)", color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(showlegend=False, margin=dict(l=150))
                
            fig_buffers["ipc"] = fig
                
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                    
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                 # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["ipc"] = img_buffer
                    
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                    
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
        else:
            st.error("表格讀取失敗")

    # === Tab 2: 技術領先企業 ===
    if buffers.get('assignee'):
        df_assignee = parse_html_table(buffers['assignee'])
        
        if df_assignee is not None and len(df_assignee.columns) >= 2:
            df_plot = df_assignee.iloc[:, :2].copy()
            df_plot.columns = ['Name', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_plot = df_plot.dropna(subset=['Count']).sort_values('Count', ascending=True).tail(15)
            
            if not df_plot.empty:
                fig = px.bar(df_plot, x='Count', y='Name', orientation='h', title="專利權人排名 (Top 15)", 
                                text='Count', color='Count', color_continuous_scale='Blues')
                fig_buffers["assignee"] = fig
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["assignee"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
        else:
            st.error("表格欄位不足")

    # === Tab 3: 主要布局國家 ===
    if buffers.get("country"):
        df_country = parse_html_table(buffers["country"])
        if df_country is not None and len(df_country.columns) >= 2:
            df_plot = df_country.iloc[:, :2].copy()
            df_plot.columns = ['Country', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_vis = df_plot.head(10).sort_values(by='Count', ascending=True)

            fig = px.bar(df_vis, x='Count', y='Country', orientation='h', title="全球專利佈局 (Top 10)",
                            text='Count', color='Count', color_continuous_scale='Viridis')
            fig.update_layout(showlegend=False, height=500)
            fig_buffers["country"] = fig
            
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["country"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)

    # === Tab 4: 專利申請趨勢 ===
    if buffers.get("trend_range"):
        df_trend = parse_html_table(buffers["trend_range"])
        if df_trend is not None and len(df_trend.columns) >= 2:
            df_plot = df_trend.iloc[:, :2].copy()
            df_plot.columns = ['Year', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            
            fig = px.line(df_plot, x='Year', y='Count', markers=True, title="申請趨勢", 
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_buffers["trend_range"] = fig
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["trend_range"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)

    # === Tab 5: 技術功效矩陣 ===
        
    # 這裡是最需要修改的地方，以支援 Buffer
    matrix_file = buffers.get("matrix")
    
    if matrix_file:
        try:
            # 【關鍵修改】如果是 Buffer，必須先歸零指標
            if hasattr(matrix_file, "seek"):
                matrix_file.seek(0)

            # 讀取 Excel (支援 Buffer 或 Path)
            df_matrix = pd.read_excel(matrix_file, header=None)
            
            # --- 原有的矩陣解析邏輯 ---
            x_labels = df_matrix.iloc[0, 2:].fillna("Unknown").astype(str).values.tolist()
            data_rows = df_matrix.iloc[2:]
            plot_data = []
            
            for _, row in data_rows.iterrows():
                y_label = str(row[0])
                counts = row[2:].values
                for x_label, count in zip(x_labels, counts):
                    try:
                        val = float(str(count).replace(',', ''))
                    except:
                        val = 0
                    if val > 0:
                        plot_data.append({'Technology': x_label, 'Efficacy': y_label, 'Count': val})
            
            df_plot = pd.DataFrame(plot_data)
            
            if not df_plot.empty:
                # 計算動態佈局
                n_x, n_y = len(x_labels), len(data_rows)
                dynamic_height = max(500, 200 + (n_y * 60))
                
                fig = px.scatter(df_plot, x='Technology', y='Efficacy', size='Count', color='Efficacy',
                                    title=f"技術功效矩陣 ({n_x}x{n_y})", size_max=40,
                                    color_discrete_sequence=px.colors.qualitative.Bold, text='Count')

                fig.update_layout(
                    xaxis={'side': 'top', 'tickangle': -45, 'dtick': 1, 'automargin': True, 'fixedrange': True},
                    yaxis={'autorange': "reversed", 'dtick': 1, 'automargin': True, 'fixedrange': True},
                    height=dynamic_height,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False
                )
                fig.update_traces(textposition='middle center', textfont={'color': 'white', 'weight': 'bold', 'size': 12})
                fig_buffers["matrix"] = fig
                try:
                    # 建立一個空的 BytesIO 物件
                    img_buffer = io.BytesIO()
                    
                    # 將圖表寫入這個 buffer (指定格式為 png)
                    # 需要安裝 kaleido 套件: pip install -U kaleido
                    fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                    
                    # 歸零指標，讓後續程式可以從頭讀取
                    img_buffer.seek(0)
                    
                    # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                    # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                    img_buffers["matrix"] = img_buffer
                    
                    # (選用) 顯示成功訊息 (除錯用)
                    # st.toast("IPC 圖表已快取至記憶體")
                    
                except Exception as e:
                    st.error(f"圖表轉換失敗: {e}")
                    # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                    # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
            else:
                st.warning("⚠️ 矩陣數據為空")

        except Exception as e:
            st.error(f"矩陣解析錯誤: {str(e)}")

    st.session_state.results["fig"] = fig_buffers
    st.session_state.results["img"] = img_buffers

def render_results():
    if not st.session_state.results:
        return  
    docx = st.session_state.results.get("docx")
    if docx:
        # 顯示下載按鈕
        st.download_button(
            label="📥 下載專利分析期末報告 (.docx)",
            data=docx,
            file_name="專利分析報告.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "布林檢索式", 
        "技術領域分類分析", 
        "技術領先企業", 
        "主要布局國家", 
        "專利申請趨勢", 
        "矩陣分析關鍵字", 
        "技術功效矩陣"
    ])

    with tab1:
        st.subheader("🧌 布林檢索式")
        st.code(st.session_state.results.get("query"), language=None)


    with tab2:
        st.subheader("📊 技術領域分類 (IPC)")
        fig = st.session_state.results["fig"].get("ipc")
        if fig:
            st.plotly_chart(fig, theme="streamlit", width="stretch") # use_container_width is deprecated
        else:
            st.error("找不到圖表")

    with tab3:
        st.subheader("🏆 技術領先企業 (Assignee)")
        fig = st.session_state.results["fig"].get("assignee")
        if fig:
            st.plotly_chart(fig, theme="streamlit", width="stretch") # use_container_width is deprecated
        else:
            st.error("找不到圖表")


    with tab4:
        st.subheader("🌍 主要布局國家")
        fig = st.session_state.results["fig"].get("country")
        if fig:
            st.plotly_chart(fig, theme="streamlit", width="stretch") # use_container_width is deprecated
        else:
            st.error("找不到圖表")

    with tab5:
        st.subheader("📈 專利申請趨勢")
        fig = st.session_state.results["fig"].get("trend_range")
        if fig:
            st.plotly_chart(fig, theme="streamlit", width="stretch") # use_container_width is deprecated
        else:
            st.error("找不到圖表")

    with tab6:
        st.markdown("""
        <style>
            /* 調整字體大小 */
            .stCodeBlock pre {
                font-size: 12px !important; /* 改小字體 */
            }
            
            /* 限制最大高度 (超過會有捲軸) */
            .stCodeBlock {
                max-height: 300px; /* 限制高度 */
                overflow-y: auto;  /* 加上垂直捲軸 */
            }
        </style>
        """, unsafe_allow_html=True)
        st.subheader("🏷️ 矩陣分析關鍵字")      
        st.code(st.session_state.results.get("matrix_data"), language=None)  

    with tab7:
        st.subheader("💡 技術功效矩陣")
        fig = st.session_state.results["fig"].get("matrix")
        if fig:
            st.plotly_chart(fig, theme="streamlit", width="stretch") # use_container_width is deprecated
        else:
            st.error("找不到圖表")

def render_all():
    render_sidebar()
    render_results()