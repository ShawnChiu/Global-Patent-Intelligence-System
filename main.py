# main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import nest_asyncio
nest_asyncio.apply()
from playwright.sync_api import sync_playwright
from models.gpss_client import GPSSClient
from services.analyzer import PatentAnalyzer
from services.gen_report import ReportGenrator
from views.components import render_sidebar, parse_diagrams,render_results
from models.gemini_client import GeminiClient
from services.settings_manager import setmgr

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    
    # 1. 取得使用者輸入 (View)
    inputs = render_sidebar()

    if inputs["submitted"]:       
        st.session_state.results = {}

        # 2. 初始化客戶端 (Model)
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        with st.spinner("正在登入GPSS ..."):
            gpss_client = GPSSClient(browser)
            if not gpss_client.login(inputs["user"], inputs["password"]):
                st.error("登入失敗：請確認帳號密碼是否正確或是再試一次")
                return
            else:
                setmgr.settings.user_id = inputs["user"]
                setmgr.settings.user_pw = inputs["password"]
                st.success("登入成功！")

        gemini_client = GeminiClient(inputs["llm_key"])
        if inputs["search_mode"] != "搜尋布林檢索式":
            with st.spinner("正在生成布林檢索式，請稍候..."):
                query = gemini_client.convert_topic_to_query(inputs["topic"])
                setmgr.settings.gemini_api_key = inputs["llm_key"]
                with st.expander("查看布林檢索式", expanded=False):
                    st.text(query)
        else:
            query = inputs["query"]
        with st.spinner("正在搜索專利 ..."):
            try:
                gpss_client.search(query)
                st.success("搜索到： " + str(gpss_client.search_result) + "筆資料")
                setmgr.settings.query = query
                st.session_state.results["query"] = query
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")

        with st.spinner("正在獲取圖表資料 ..."):
            try:
                gpss_client.fetch_diagrams()
                st.success("獲取圖表成功！")
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")

        matrix_json = []
        if gpss_client.dedup_result != 0:
            with st.spinner("正在進行矩陣維度分析 ..."):
                try:
                    if inputs["matrix_mode"] == "AI 語意推論 (Gemini LLM)":
                        gpss_client.fetch_names_and_contents()
                        matrix_json, state = gemini_client.generate_gpss_strategy(gpss_client.diagram_buffers["contents"])  
                        if state != "Success":
                            st.error(state)
                            return
                        else:
                            setmgr.settings.gemini_api_key = inputs["llm_key"]
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
                            "technologies": parse_manual_input(inputs["tech_conf"]),
                            "efficacies": parse_manual_input(inputs["effect_conf"])
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


        render_success_place = st.empty()
        report_success_place = st.empty()
        with st.spinner("正在讀取並渲染圖表並生成簡報 ..."):
            parse_diagrams(gpss_client.diagram_buffers)
            render_success_place.success("渲染圖表完成！")
            try:
                regen = ReportGenrator(
                    search_result=[gpss_client.search_result, gpss_client.dedup_result], 
                    query=query, 
                    matrix_json=matrix_json, 
                    students_data=[inputs["name"], inputs["student_id"]], 
                    theme=inputs["topic"], 
                    # 注意：確認 inputs 裡面是否有 "source" 這個 key，原本代碼有用到
                    source=[inputs.get("source", ""), inputs["conf_source"]],
                    chart_buffers=st.session_state.results["img"]
                )
                
                # 【關鍵修改】改為回傳 BytesIO 物件，不存硬碟
                # 請確認 services/gen_report.py 已經改成回傳 buffer
                st.session_state.results["docx"] = regen.gen_report() 
                
                report_success_place.success("分析報告完成！")
                
                    
            except Exception as e:
                st.error(f"報告生成失敗: {str(e)}")
            setmgr.save()

        browser.close()
        p.stop()
    render_results()
        
        
if __name__ == "__main__":
    main()