import streamlit.web.cli as stcli
import os, sys
import webbrowser
from threading import Timer

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

def open_browser():
    """等待伺服器啟動後，自動開啟瀏覽器"""
    # 預設 Port 是 8501，如果你有改 port 這裡也要改
    webbrowser.open_new("http://localhost:8501")

if __name__ == "__main__":
    # 設定 Streamlit 為 headless 模式 (不讓它自己亂開，我們手動控制)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    main_script = resolve_path("main.py")
    
    # 設定參數
    sys.argv = [
        "streamlit",
        "run",
        main_script,
        "--global.developmentMode=false",
        "--server.port=8501", # 強制固定 Port，確保跟上面的網址一致
    ]
    
    # 【關鍵修改】：設定一個計時器，在 1.5 秒後執行 open_browser
    # 這樣可以讓 Streamlit 先有時間啟動伺服器
    Timer(1.5, open_browser).start()
    
    # 啟動 Streamlit (這行程式碼會一直執行，直到你關閉程式)
    sys.exit(stcli.main())