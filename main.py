# main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright
from models.gpss_client import GPSSClient
from services.analyzer import PatentAnalyzer
from views.components import render_sidebar, render_charts_from_files
from services.strategy_generator import BooleanRetrievalGenerator

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    
    # 1. 取得使用者輸入 (View)
    inputs = render_sidebar()

    playeright = sync_playwright().start()
    browser = playeright.chromium.launch(headless=False)

    if inputs["submitted"]:
        # 2. 初始化客戶端 (Model)
        client = GPSSClient(browser)

        with st.spinner("正在進行 ETL (Extract-Transform-Load) ..."):
            try:
                # 3. 獲取數據 (Model)
                client.fetch_data(inputs["query"])
                
            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")
        
        with st.spinner("正在讀取並渲染圖表 ..."):
            # 4. 讀取並渲染圖表 (View)
            render_charts_from_files(["diagarm_1.html", "diagram_2.html", "diagram_3.html", "diagram_4.html"])
        # with st.spinner("正在進行矩陣維度分析 ..."):
        #     try:
        #         data, state = BooleanRetrievalGenerator.generate_gpss_strategy(df, inputs["llm_key"]);    
        #         if state != "Success":
        #             st.error(state)
        #             return
        #         st.success(data);
        #     except Exception as e:
        #         st.error(f"系統發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()