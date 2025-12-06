import streamlit as st
from models.gemini_client import GeminiClient
from models.gpss_client import GPSSClient
from services.settings_manager import setmgr
from services.parser import Parser
from services.gen_report import ReportGenrator
from config import EXAMPLE_CONFIG

def get_result():
    st.session_state.results = {}
    with st.spinner("正在分析輸入 ..."):
        if st.session_state.topic_select != "自訂":
            set_example(st.session_state.topic_select)
        if st.session_state.search_mode == "AI 檢索式推論 (Gemini LLM)" or st.session_state.matrix_mode == "AI 語意推論 (Gemini LLM)":
            if st.session_state.gemini_api_key:
                gemini_client = GeminiClient(st.session_state.gemini_api_key)
            else:
                st.error("尚未輸入 Gemini API")
                return
        if st.session_state.search_mode == "搜尋布林檢索式" and not Parser.is_valid_parentheses(st.session_state.query):
            st.error("非法布林檢索式")
            return
        if st.session_state.matrix_mode == "關鍵字規則 (Rule-based)":
            for i, tech in enumerate(st.session_state.matrix["technologies"]):
                if not Parser.is_valid_parentheses(tech["boolean"]):
                    st.error(f"非法技術布林式：{i+1}")
                    return
            for i, eff in enumerate(st.session_state.matrix["efficacies"]):
                if not Parser.is_valid_parentheses(eff["boolean"]):
                    st.error(f"非法功效布林式：{i+1}")
                    return
        st.success("輸入分析完成")


    # 2. 初始化客戶端 (Model)
    with st.spinner("正在登入GPSS ..."):
        gpss_client = GPSSClient()
        if not gpss_client.login(st.session_state.gpss_id, st.session_state.gpss_pw):
            st.error("登入失敗：請確認帳號密碼是否正確或是再試一次")
            return
        else:
            setmgr.settings.gpss_id = st.session_state.gpss_id
            setmgr.settings.gpss_pw = st.session_state.gpss_pw
            st.success("登入成功！")

    if st.session_state.search_mode == "AI 檢索式推論 (Gemini LLM)":
        with st.spinner("正在生成布林檢索式，請稍候..."):
            st.session_state.query = gemini_client.convert_topic_to_query(st.session_state.topic)
            setmgr.settings.gemini_api_key = st.session_state.search_model.gemini_api_key
            with st.expander("查看布林檢索式", expanded=False):
                st.text(st.session_state.query)

    with st.spinner("正在搜索專利 ..."):
        try:
            gpss_client.search(st.session_state.query)
            st.success("搜索到： " + str(gpss_client.search_result) + "筆資料")
            setmgr.settings.query = st.session_state.query
            st.session_state.results["query"] = st.session_state.query
        except Exception as e:
            st.error(f"系統發生錯誤: {str(e)}")

    with st.spinner("正在獲取圖表資料 ..."):
        try:
            gpss_client.fetch_diagrams()
            st.success("獲取圖表成功！")
        except Exception as e:
            st.error(f"系統發生錯誤: {str(e)}")

    if gpss_client.dedup_result <= 30000:

        with st.spinner("正在進行矩陣維度分析 ..."):
            try:
                if st.session_state.matrix_mode == "AI 語意推論 (Gemini LLM)":
                    gpss_client.fetch_names_and_contents()
                    st.session_state.matrix, state = gemini_client.generate_gpss_strategy(gpss_client.diagram_buffers["contents"])  
                    if state != "Success":
                        st.error(state)
                        return
                    else:
                        setmgr.settings.gemini_api_key = st.session_state.gemini_api_key
                st.success("維度分析完成！")
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")
    else:
        st.warning("專利筆數超過 30000，跳過矩陣分析步驟。")

    with st.spinner("正在進行矩陣分析"):
        gpss_client.fill_matrix_form(st.session_state.matrix)
        st.session_state.results["matrix"] = st.session_state.matrix
        st.success("矩陣分析完成！")

    gpss_client.close()


    render_success_place = st.empty()
    report_success_place = st.empty()
    with st.spinner("正在讀取並渲染圖表並生成簡報 ..."):
        st.session_state.results["fig"], st.session_state.results["img"] = Parser.parse_diagrams(gpss_client.diagram_buffers)
        render_success_place.success("渲染圖表完成！")
        try:
            regen = ReportGenrator(
                search_result=[gpss_client.search_result, gpss_client.dedup_result], 
                query=st.session_state.query, 
                matrix_json=st.session_state.matrix, 
                students_data=[st.session_state.name, st.session_state.student_id], 
                topic=st.session_state.topic, 
                # 注意：確認 inputs 裡面是否有 "source" 這個 key，原本代碼有用到
                source=[st.session_state.source, st.session_state.conf_source],
                chart_buffers=st.session_state.results["img"]
            )
            
            # 【關鍵修改】改為回傳 BytesIO 物件，不存硬碟
            # 請確認 services/gen_report.py 已經改成回傳 buffer
            st.session_state.results["docx"] = regen.gen_report() 
            
            report_success_place.success("分析報告完成！")
            
                
        except Exception as e:
            st.error(f"報告生成失敗: {str(e)}")
        setmgr.save()

def set_example(topic):
    st.session_state.topic = topic
    st.session_state.query = EXAMPLE_CONFIG[topic]["main_boolean"]
    st.session_state.matrix = EXAMPLE_CONFIG[topic]["matrix"]
    st.session_state.search_mode = "搜尋布林檢索式"
    st.session_state.matrix_mode = "關鍵字規則 (Rule-based)"
