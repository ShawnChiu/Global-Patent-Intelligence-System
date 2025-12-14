# 檔案位置：views/components.py
import streamlit as st
import pandas as pd
from services.workflow import get_results
from config import EXAMPLE_CONFIG


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

@st.dialog("✏️ 編輯矩陣分析", width="large")
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
    st.write("請在下方分別定義技術與功效的關鍵字：")
    col1 ,col2 = st.columns([1, 1])
    with col1:
        st.header("技術分析")
        tech = []
        for i in range(6):
            c1, c2 = st.columns([1, 3]) # 設定左右寬度比例
            with c1:
                # 左邊：短的輸入框
                label = st.text_input(
                    f"功效 {i+1}", 
                    key=f"tech_lable{i}", 
                    label_visibility="collapsed" # 隱藏每個輸入框的標籤，看起來像表格
                )
                
            with c2:
                # 右邊：長文字區域 (關鍵在這裡！)
                # height=100 可以讓格子變高，容納約 3-4 行文字
                boolean = st.text_area(
                    f"布林式 {i+1}", 
                    key=f"tech_boolean{i}", 
                    height=100, 
                    label_visibility="collapsed"
                )
            if label and boolean:
                tech.append({
                    "label": label, 
                    "boolean": boolean
                })
        st.session_state.matrix["technologies"] = tech
    with col2:
        st.header("功效分析")
        eff = []
        for i in range(6):
            c1, c2 = st.columns([1, 3]) # 設定左右寬度比例
            
            with c1:
                # 左邊：短的輸入框
                label = st.text_input(
                    f"功效 {i+1}", 
                    key=f"eff_label{i}", 
                    label_visibility="collapsed" # 隱藏每個輸入框的標籤，看起來像表格
                )
                
            with c2:
                # 右邊：長文字區域 (關鍵在這裡！)
                # height=100 可以讓格子變高，容納約 3-4 行文字
                boolean = st.text_area(
                    f"布林式 {i+1}", 
                    key=f"eff_boolean{i}", 
                    height=100, 
                    label_visibility="collapsed"
                )
        if label and boolean:
            eff.append({
                "label": label, 
                "boolean": boolean
            })
        st.session_state.matrix["efficacies"] = eff
    

    st.session_state.conf_source = st.text_input("來源說明 (選填)", value=st.session_state.conf_source, type="default", placeholder="輸入來源")

    # 儲存按鈕
    if st.button("💾 儲存並關閉", type="primary", use_container_width=True):
        st.rerun()

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
    st.header("🔐 登入模式")
    st.session_state.login_mode = st.radio(
        "選擇登入模式",
        ["手動輸入驗證碼", "自動辨識驗證碼"],
        captions=["", "快速但不穩定"]
    )

    if st.button("💾 儲存並關閉", type="primary", use_container_width=True):
        st.rerun()

def render_sidebar():   
    with st.sidebar:
        st.header("📝 基本資料")
        st.button("✏️ 點擊編輯基本資料", help="點擊編輯基本資料", key="btn_edit_basic_info", on_click=show_basic_info)
        st.divider()

        topic_list = list(EXAMPLE_CONFIG.keys())
        topic_list.append("自訂")
        st.header("🍬 專利主題")
        st.session_state.topic_select = st.selectbox(
            "選擇主題", 
            options=topic_list,
            key="topic_mode"
        )
        if st.session_state.topic_select != "自訂" :
            st.divider()
            st.button("🚀 開始分析", type="primary", on_click=get_results)
            return

        st.session_state.topic = st.text_input("輸入技術主題", value="", type="default", placeholder="輸入你的專利技術主題")

        st.divider()
        st.header("🔍 搜尋條件")

        st.session_state.search_mode = st.radio(
            "選擇搜尋模式",
            ["搜尋布林檢索式", "AI 檢索式推論 (Gemini LLM)"],
            captions=["快速、免費", "需 Google API Key"]
        )
        
        if st.session_state.search_mode != "AI 檢索式推論 (Gemini LLM)":
            st.button("✏️ 點擊編輯檢索式", help="點擊編輯檢索式", key="btn_edit_query", on_click=show_query_editor)
        else:
            print(st.session_state.search_mode)
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

        if st.session_state.matrix_mode != "AI 語意推論 (Gemini LLM)":
            st.button("✏️ 點擊編輯關鍵字", help="點擊編輯關鍵字", key="btn_edit_matrix", on_click=show_matrix_editor)    
        else: # AI Mode
            st.markdown("""
            **🧠 AI 全自動分類** 系統將自動閱讀專利摘要並分析功效定義
            """)
        
        if st.session_state.search_mode != "搜尋布林檢索式" or st.session_state.matrix_mode != "關鍵字規則 (Rule-based)":
            st.divider()
            st.header("🔑 API 設定")

            if st.button("❓ 查看教學", key="btn_api_help", help="點擊查看教學"):
                show_gemini_tutorial()

            if not st.session_state.gemini_api_key:
                st.warning("請輸入 Key 以啟動 AI 功能")
            # --- 下面放輸入框 ---
            st.session_state.gemini_api_key = st.text_input(
                "Google Gemini API Key", 
                value=st.session_state.gemini_api_key, 
                type="password", 
                placeholder="貼上你的 AI Studio Key",
                label_visibility="collapsed"
            )

        st.divider()
        st.button("🚀 開始分析", type="primary", on_click=get_results)

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
        col1 ,col2 = st.columns([1, 1])
        with col1:
            st.header("技術分析")
            for tech in st.session_state.matrix.get("technologies", []):
                c1, c2 = st.columns([1, 3]) # 設定左右寬度比例
                with c1:
                    st.code(
                        tech.get("label", ""),
                        language=None
                    )
                    
                with c2:
                    st.code(
                        tech.get("boolean", ""),
                        language=None
                    )
        with col2:
            st.header("功效分析")
            for eff in st.session_state.matrix.get("efficacies", []):
                c1, c2 = st.columns([1, 3]) # 設定左右寬度比例
                with c1:
                    st.code(
                        eff.get("label", ""),
                        language=None
                    )
                    
                with c2:
                    st.code(
                        eff.get("boolean", ""),
                        language=None
                    )

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