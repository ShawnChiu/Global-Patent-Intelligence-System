# main.py
import streamlit as st
from models.gpss_client import GPSSClient
from services.analyzer import PatentAnalyzer
from views.components import render_sidebar, render_charts

# 設定頁面資訊 (這行必須是 main 的第一行 Streamlit 指令)
st.set_page_config(page_title="專利分析", layout="wide")

def main():
    st.title("專利分析與佈局系統")
    
    # 1. 取得使用者輸入 (View)
    inputs = render_sidebar()
    
    if inputs["submitted"]:
        if not inputs["api_key"]:
            st.error("請輸入 API Key")
            return

        # 2. 初始化客戶端 (Model)
        client = GPSSClient(inputs["api_key"])
        
        with st.spinner("正在進行 ETL (Extract-Transform-Load) ..."):
            try:
                # 3. 獲取數據 (Model)
                df = client.fetch_data(inputs["query"], inputs["ipc"], inputs["qty"])
                
                if df.empty:
                    st.warning("查無資料，請放寬搜尋條件。")
                else:
                    st.success(f"ETL 完成！共處理 {len(df)} 筆專利數據。")
                    
                    # 4. 執行進階分析 (Service)
                    matrix_df = PatentAnalyzer.generate_matrix(
                        df, inputs["tech_conf"], inputs["effect_conf"]
                    )
                    
                    # 5. 渲染結果 (View)
                    render_charts(df, matrix_df)
                    
                    # 顯示原始資料表格 (Optional)
                    with st.expander("檢視原始數據"):
                        st.dataframe(df)

            except Exception as e:
                st.error(f"系統發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()