import streamlit as st
from models.gemini_client import GeminiClient
from models.gpss_client import GPSSClient
from services.settings_manager import setmgr
from services.analyzer import parse_diagrams
from services.gen_report import ReportGenrator

def get_result():
    st.session_state.results = {}

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

    if st.session_state.search_mode != "搜尋布林檢索式":
        gemini_client = GeminiClient(st.session_state.gemini_api_key)
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

        matrix_json = []
        with st.spinner("正在進行矩陣維度分析 ..."):
            try:
                if st.session_state.matrix_mode == "AI 語意推論 (Gemini LLM)":
                    gpss_client.fetch_names_and_contents()
                    matrix_json, state = gemini_client.generate_gpss_strategy(gpss_client.diagram_buffers["contents"])  
                    if state != "Success":
                        st.error(state)
                        return
                    else:
                        setmgr.settings.gemini_api_key = st.session_state.gemini_api_key
                else:
                    def parse_manual_input(text_block):
                        """
                        將 "Label: (Query)" 格式的多行字串轉換為 list of dicts
                        """
                        items = []
                        if not text_block: 
                            return items
                            
                        # 逐行處理
                        for line in text_block.strip().split('\n'):
                            line = line.strip()
                            if not line: continue  # 跳過空行
                            
                            # 尋找第一個冒號 (:) 來切割 Label 與 Boolean String
                            if ':' in line:
                                parts = line.split(':', 1) # 只切第一刀
                                label = parts[0].strip()
                                query = parts[1].strip()
                                
                                items.append({
                                    "label": label,
                                    "boolean": query
                                })
                                
                        return items
                    matrix_json = {
                        "domain_detected": "Manual Input (手動定義)",
                        "technologies": parse_manual_input(st.session_state.tech),
                        "efficacies": parse_manual_input(st.session_state.eff)
                    }
                st.success("維度分析完成！")
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")
    else:
        st.warning("專利筆數超過 30000，跳過矩陣分析步驟。")

    with st.spinner("正在進行矩陣分析"):
        gpss_client.fill_matrix_form(matrix_json)
        st.session_state.results["matrix_data"] = matrix_json
        st.success("矩陣分析完成！")

    gpss_client.close()


    render_success_place = st.empty()
    report_success_place = st.empty()
    with st.spinner("正在讀取並渲染圖表並生成簡報 ..."):
        parse_diagrams(gpss_client.diagram_buffers)
        render_success_place.success("渲染圖表完成！")
        try:
            regen = ReportGenrator(
                search_result=[gpss_client.search_result, gpss_client.dedup_result], 
                query=st.session_state.query, 
                matrix_json=matrix_json, 
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