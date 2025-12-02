# main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright
from models.gpss_client import GPSSClient
from services.analyzer import PatentAnalyzer
from services.gen_report import ReportGenrator
from views.components import render_sidebar, render_charts_from_files
from models.gemini_client import GeminiClient
import json

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    
    # 1. 取得使用者輸入 (View)
    inputs = render_sidebar()

    playeright = sync_playwright().start()
    browser = playeright.chromium.launch(headless=False)

    if inputs["submitted"]:        # 2. 初始化客戶端 (Model)
        gemini_client = GeminiClient(inputs["llm_key"])
        if inputs["search_mode"] != "搜尋布林檢索式":
            with st.spinner("正在生成布林檢索式，請稍候..."):
                query = gemini_client.convert_topic_to_query(inputs["topic"])
                with st.expander("查看布林檢索式", expanded=False):
                    st.text(query)
        else:
            query = inputs["query"]

        gpss_client = GPSSClient(browser)
        if not gpss_client.login(inputs["user"], inputs["password"]):
            st.error("登入失敗：請確認帳號密碼是否正確或是再試一次")
            return

        with st.spinner("正在進行 ETL (Extract-Transform-Load) ..."):
            try:
                # 3. 獲取數據 (Model)
                gpss_client.fetch_data(query)
                
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")

        matrix_json = []
        with st.spinner("正在進行矩陣分析 ..."):
            try:
                if inputs["matrix_mode"] == "AI 語意推論 (Gemini LLM)":
                        matrix_json, state = gemini_client.generate_gpss_strategy(".data\contents.xls");    
                        if state != "Success":
                            st.error(state)
                            return
                        gpss_client.fill_matrix_form(matrix_json)
                    
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
                gpss_client.fill_matrix_form(matrix_json)
            except Exception as e:
                    st.error(f"系統發生錯誤: {str(e)}")

        with st.spinner("正在讀取並渲染圖表 ..."):
            # 4. 讀取並渲染圖表 (View)
            render_charts_from_files({"ipc": ".data/diagram_4.html", "assignee": ".data/diagram_2.html", 'country': ".data/diagram_3.html", 'trend_range': ".data/diagram_1.html", "matrix": ".data\matrix_form.xls"})


        with st.spinner("正在生成專利分析報告 ..."):
            try:
                regen = ReportGenrator(
                    search_result=gpss_client.get_results(), 
                    query=query, 
                    matrix_json=matrix_json, 
                    students_data=[inputs["name"], inputs["student_id"]], 
                    theme=inputs["topic"], 
                    # 注意：確認 inputs 裡面是否有 "source" 這個 key，原本代碼有用到
                    source=[inputs.get("source", ""), inputs["conf_source"]]
                )
                
                # 【關鍵修改】改為回傳 BytesIO 物件，不存硬碟
                # 請確認 services/gen_report.py 已經改成回傳 buffer
                report_buffer = regen.gen_report() 
                
                st.success("分析完成！")
                
                # 顯示下載按鈕
                st.download_button(
                    label="📥 下載專利分析期末報告 (.docx)",
                    data=report_buffer,
                    file_name="專利分析報告.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                    
            except Exception as e:
                st.error(f"報告生成失敗: {str(e)}")
    browser.close()
        
        
if __name__ == "__main__":
    main()