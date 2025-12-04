# services/analyzer.py
import pandas as pd
import os
import streamlit as st
import io
import plotly.express as px


def parse_diagrams(diagram_buffers):

    """
    爬蟲模式專用渲染函式 (Buffer 支援版)
    Args:
        files_dict (dict): 字典，Values 可以是 檔案路徑(str) 或 記憶體緩衝區(BytesIO)
    """
    
    
    fig_buffers = {}
    img_buffers = {}

    def parse_html_table(uploaded_file):
        """
        HTML 解析器：支援 Path, Bytes, BytesIO
        """
        if uploaded_file is None:
            return None

        try:
            html_content = ""

            # 1. 處理字串 (檔案路徑 或 HTML 原始碼)
            if isinstance(uploaded_file, str):
                # 如果是路徑，且檔案存在，就讀取
                if os.path.exists(uploaded_file) and uploaded_file.endswith(('.html', '.htm')):
                    with open(uploaded_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                else:
                    # 否則假設它就是 HTML 字串
                    html_content = uploaded_file
            
            # 2. 處理 Bytes (原始資料)
            elif isinstance(uploaded_file, bytes):
                html_content = uploaded_file.decode("utf-8")

            # 3. 處理 Buffer (BytesIO) 或 UploadedFile
            elif hasattr(uploaded_file, "read"):
                # 【關鍵】重置指標，確保從頭讀取
                if hasattr(uploaded_file, "seek"):
                    uploaded_file.seek(0)
                
                content = uploaded_file.read()
                
                if isinstance(content, bytes):
                    html_content = content.decode("utf-8", errors='ignore')
                else:
                    html_content = content
            
            # 4. 解析 Pandas
            if html_content:
                try:
                    dfs = pd.read_html(html_content, header=0, flavor='lxml')
                except:
                    dfs = pd.read_html(html_content, header=0)

                if dfs:
                    return dfs[0]
                
        except Exception as e:
            st.error(f"檔案解析錯誤: {str(e)}")
            return None
        
        return None

    # === Tab 1: IPC 技術分類 ===
    if diagram_buffers.get("ipc"):
        df_ipc = parse_html_table(diagram_buffers["ipc"])
            
        if df_ipc is not None and len(df_ipc.columns) >= 2:
            df_plot = df_ipc.copy()
            df_plot.columns = ['Category', 'Count'] + list(df_plot.columns[2:])
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_plot = df_plot.sort_values('Count', ascending=True).tail(15)
            df_plot['label'] = df_plot['Count'].apply(lambda x: f"({int(x)})" if pd.notnull(x) else "")

            fig = px.bar(df_plot, x='Count', y='Category', orientation='h', text='label', color='Category', 
                        title="IPC 技術分類 (Top 15)", color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(showlegend=False, margin=dict(l=150))
                
            fig_buffers["ipc"] = fig
                
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                    
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["ipc"] = img_buffer
                    
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                    
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
        else:
            st.error("表格讀取失敗")

    # === Tab 2: 技術領先企業 ===
    if diagram_buffers.get('assignee'):
        df_assignee = parse_html_table(diagram_buffers['assignee'])
        
        if df_assignee is not None and len(df_assignee.columns) >= 2:
            df_plot = df_assignee.iloc[:, :2].copy()
            df_plot.columns = ['Name', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_plot = df_plot.dropna(subset=['Count']).sort_values('Count', ascending=True).tail(15)
            
            if not df_plot.empty:
                fig = px.bar(df_plot, x='Count', y='Name', orientation='h', title="專利權人排名 (Top 15)", 
                                text='Count', color='Count', color_continuous_scale='Blues')
                fig_buffers["assignee"] = fig
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["assignee"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
        else:
            st.error("表格欄位不足")

    # === Tab 3: 主要布局國家 ===
    if diagram_buffers.get("country"):
        df_country = parse_html_table(diagram_buffers["country"])
        if df_country is not None and len(df_country.columns) >= 2:
            df_plot = df_country.iloc[:, :2].copy()
            df_plot.columns = ['Country', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            df_vis = df_plot.head(10).sort_values(by='Count', ascending=True)

            fig = px.bar(df_vis, x='Count', y='Country', orientation='h', title="全球專利佈局 (Top 10)",
                            text='Count', color='Count', color_continuous_scale='Viridis')
            fig.update_layout(showlegend=False, height=500)
            fig_buffers["country"] = fig
            
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["country"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)

    # === Tab 4: 專利申請趨勢 ===
    if diagram_buffers.get("trend_range"):
        df_trend = parse_html_table(diagram_buffers["trend_range"])
        if df_trend is not None and len(df_trend.columns) >= 2:
            df_plot = df_trend.iloc[:, :2].copy()
            df_plot.columns = ['Year', 'Count']
            df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
            
            fig = px.line(df_plot, x='Year', y='Count', markers=True, title="申請趨勢", 
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_buffers["trend_range"] = fig
            try:
                # 建立一個空的 BytesIO 物件
                img_buffer = io.BytesIO()
                
                # 將圖表寫入這個 buffer (指定格式為 png)
                # 需要安裝 kaleido 套件: pip install -U kaleido
                fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                
                # 歸零指標，讓後續程式可以從頭讀取
                img_buffer.seek(0)
                
                # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                img_buffers["trend_range"] = img_buffer
                
                # (選用) 顯示成功訊息 (除錯用)
                # st.toast("IPC 圖表已快取至記憶體")
                
            except Exception as e:
                st.error(f"圖表轉換失敗: {e}")
                # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)

    # === Tab 5: 技術功效矩陣 ===
        
    # 這裡是最需要修改的地方，以支援 Buffer
    matrix_file = diagram_buffers.get("matrix")
    
    if matrix_file:
        try:
            # 【關鍵修改】如果是 Buffer，必須先歸零指標
            if hasattr(matrix_file, "seek"):
                matrix_file.seek(0)

            # 讀取 Excel (支援 Buffer 或 Path)
            df_matrix = pd.read_excel(matrix_file, header=None)
            
            # --- 原有的矩陣解析邏輯 ---
            x_labels = df_matrix.iloc[0, 2:].fillna("Unknown").astype(str).values.tolist()
            data_rows = df_matrix.iloc[2:]
            plot_data = []
            
            for _, row in data_rows.iterrows():
                y_label = str(row[0])
                counts = row[2:].values
                for x_label, count in zip(x_labels, counts):
                    try:
                        val = float(str(count).replace(',', ''))
                    except:
                        val = 0
                    if val > 0:
                        plot_data.append({'Technology': x_label, 'Efficacy': y_label, 'Count': val})
            
            df_plot = pd.DataFrame(plot_data)
            
            if not df_plot.empty:
                # 計算動態佈局
                n_x, n_y = len(x_labels), len(data_rows)
                dynamic_height = max(500, 200 + (n_y * 60))
                
                fig = px.scatter(df_plot, x='Technology', y='Efficacy', size='Count', color='Efficacy',
                                    title=f"技術功效矩陣 ({n_x}x{n_y})", size_max=40,
                                    color_discrete_sequence=px.colors.qualitative.Bold, text='Count')

                fig.update_layout(
                    xaxis={'side': 'top', 'tickangle': -45, 'dtick': 1, 'automargin': True, 'fixedrange': True},
                    yaxis={'autorange': "reversed", 'dtick': 1, 'automargin': True, 'fixedrange': True},
                    height=dynamic_height,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False
                )
                fig.update_traces(textposition='middle center', textfont={'color': 'white', 'weight': 'bold', 'size': 12})
                fig_buffers["matrix"] = fig
                try:
                    # 建立一個空的 BytesIO 物件
                    img_buffer = io.BytesIO()
                    
                    # 將圖表寫入這個 buffer (指定格式為 png)
                    # 需要安裝 kaleido 套件: pip install -U kaleido
                    fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
                    
                    # 歸零指標，讓後續程式可以從頭讀取
                    img_buffer.seek(0)
                    
                    # 3. 存回你的 buffers 字典 (建議用新的 key 區分，例如 "ipc_chart")
                    # 這樣你的 ReportGenerator 就可以直接拿 buffers["ipc_chart"] 去貼圖了
                    img_buffers["matrix"] = img_buffer
                    
                    # (選用) 顯示成功訊息 (除錯用)
                    # st.toast("IPC 圖表已快取至記憶體")
                    
                except Exception as e:
                    st.error(f"圖表轉換失敗: {e}")
                    # 提示：如果這裡報錯，通常是因為沒有安裝 kaleido
                    # 請執行: pip install kaleido==0.2.1 (新版有時有 bug，0.2.1 較穩)
            else:
                st.warning("⚠️ 矩陣數據為空")

        except Exception as e:
            st.error(f"矩陣解析錯誤: {str(e)}")

    st.session_state.results["fig"] = fig_buffers
    st.session_state.results["img"] = img_buffers