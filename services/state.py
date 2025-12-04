import streamlit as st
from services.settings_manager import setmgr
from services.workflow import get_result


def init_session_state():
    """
    負責初始化所有的 Session State 變數。
    只會在第一次執行時生效，後續 Rerun 會直接跳過。
    """
    # 1. 初始化結果容器 (最重要)
    st.session_state.setdefault("results", {})

    # 2. 初始化按鈕狀態
    st.session_state.setdefault("submitted", False)

    # 3. 初始化輸入欄位預設值 (從 settings 讀取)
    # 使用 setdefault 是更簡潔的寫法，等同於 if key not in ... then set ...
    st.session_state.setdefault("topic", "")
    st.session_state.setdefault("gpss_id", setmgr.settings.gpss_id)
    st.session_state.setdefault("gpss_pw", setmgr.settings.gpss_pw)
    st.session_state.setdefault("gemini_api_key", setmgr.settings.gemini_api_key)
    st.session_state.setdefault("name", setmgr.settings.name)
    st.session_state.setdefault("student_id", setmgr.settings.student_id)

    # 4. 初始化複雜邏輯變數
    st.session_state.setdefault("search_mode", "搜尋布林檢索式")
    st.session_state.setdefault("matrix_mode", "關鍵字規則 (Rule-based)")
    
    # 5. 初始化那些會在 render 過程中產生，但尚未存在的變數
    st.session_state.setdefault("query", setmgr.settings.query)
    st.session_state.setdefault("source", "")
    st.session_state.setdefault("tech", setmgr.settings.tech_config)
    st.session_state.setdefault("eff", setmgr.settings.effect_config)
    st.session_state.setdefault("conf_source", "")

def detect_state():
    if st.session_state.submitted:
        get_result()