# main.py
import asyncio
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import nest_asyncio
nest_asyncio.apply()

from services.state import init_session_state, detect_state
from views.components import render_all

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    init_session_state()

    detect_state()

    render_all()
        
        
if __name__ == "__main__":
    main()