# main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright
from models.gpss_client import GPSSClient
from services.analyzer import PatentAnalyzer
from views.components import render_sidebar, render_charts

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    
    # 1. 取得使用者輸入 (View)
    inputs = render_sidebar()

    playeright = sync_playwright().start()
    browser = playeright.chromium.launch(headless=False)

    st.success("登入成功！")
    if inputs["submitted"]:
        # 2. 初始化客戶端 (Model)
        
        client = GPSSClient(browser)
        client.login()

        print("Fetching data...")
        client.fetch_data(inputs["query"])


if __name__ == "__main__":
    main()