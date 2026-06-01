import pandas as pd
import os
import io
import re
import plotly.express as px


def _notify(callback, level, message):
    if callback:
        callback(level, message)


class Parser:
    WEB_CHART_BG = "#0f172a"
    WEB_PLOT_BG = "#111827"
    WEB_TEXT = "#e5e7eb"
    WEB_GRID = "rgba(148, 163, 184, 0.18)"

    @staticmethod
    def _style_web_figure(fig, height=None, left_margin=120, bottom_margin=80, top_margin=72):
        fig.update_layout(
            paper_bgcolor=Parser.WEB_CHART_BG,
            plot_bgcolor=Parser.WEB_PLOT_BG,
            font=dict(color=Parser.WEB_TEXT, family="Microsoft JhengHei, Segoe UI, Arial", size=12),
            title=dict(font=dict(size=18, color="#f8fafc"), x=0.02, xanchor="left"),
            margin=dict(l=left_margin, r=52, t=top_margin, b=bottom_margin),
            hoverlabel=dict(bgcolor="#020617", bordercolor="rgba(255,255,255,0.14)", font=dict(color="#f8fafc")),
            uniformtext=dict(minsize=10, mode="hide"),
        )
        if height:
            fig.update_layout(height=height)
        fig.update_xaxes(
            showgrid=True,
            gridcolor=Parser.WEB_GRID,
            zeroline=False,
            color=Parser.WEB_TEXT,
            automargin=True,
        )
        fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            color=Parser.WEB_TEXT,
            automargin=True,
        )
        return fig

    @staticmethod
    def _style_bar_labels(fig):
        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#f8fafc", size=11),
            cliponaxis=False,
        )
        return fig
    
    @staticmethod
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
                html_source = io.StringIO(html_content)
                try:
                    dfs = pd.read_html(html_source, header=0, flavor='lxml')
                except:
                    html_source = io.StringIO(html_content)
                    dfs = pd.read_html(html_source, header=0)

                if dfs:
                    return dfs[0]
                
        except Exception as e:
            print(f"檔案解析錯誤: {e}")
            return None
        
        return None

    @staticmethod
    def _cache_figure(key, fig, fig_buffers, img_buffers, export_image=False, callback=None):
        fig_buffers[key] = fig
        if not export_image:
            return True

        try:
            if callback:
                callback("info", f"正在轉換圖表圖片：{key}")
            img_buffer = io.BytesIO()
            fig.write_image(img_buffer, format="png", width=1200, height=800, scale=2)
            img_buffer.seek(0)
            img_buffers[key] = img_buffer
            return True
        except Exception as e:
            message = f"圖表轉換失敗：{key} - {e}"
            if callback:
                callback("warning", message)
            else:
                print(message)
            return False

    @staticmethod
    def parse_diagrams(diagram_buffers, callback=None, export_images=False):

        """
        爬蟲模式專用渲染函式 (Buffer 支援版)
        Args:
            files_dict (dict): 字典，Values 可以是 檔案路徑(str) 或 記憶體緩衝區(BytesIO)
        """
        
        
        fig_buffers = {}
        img_buffers = {}

        def cache_figure(key, fig):
            Parser._cache_figure(
                key,
                fig,
                fig_buffers,
                img_buffers,
                export_image=export_images,
                callback=callback,
            )

        # === Tab 1: IPC 技術分類 ===
        if diagram_buffers.get("ipc"):
            df_ipc = Parser.parse_html_table(diagram_buffers["ipc"])
                
            if df_ipc is not None and len(df_ipc.columns) >= 2:
                df_plot = df_ipc.copy()
                df_plot.columns = ['Category', 'Count'] + list(df_plot.columns[2:])
                df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
                df_plot = df_plot.sort_values('Count', ascending=True).tail(15)
                df_plot['label'] = df_plot['Count'].apply(lambda x: f"({int(x)})" if pd.notnull(x) else "")

                fig = px.bar(df_plot, x='Count', y='Category', orientation='h', text='label', color='Category', 
                            title="IPC 技術分類 (Top 15)", color_discrete_sequence=px.colors.qualitative.Set2)
                Parser._style_web_figure(fig, left_margin=170, bottom_margin=56)
                Parser._style_bar_labels(fig)
                fig.update_layout(showlegend=False)
                cache_figure("ipc", fig)
            else:
                _notify(callback, "warning", "IPC 表格讀取失敗")

        # === Tab 2: 技術領先企業 ===
        if diagram_buffers.get('assignee'):
            df_assignee = Parser.parse_html_table(diagram_buffers['assignee'])
            
            if df_assignee is not None and len(df_assignee.columns) >= 2:
                df_plot = df_assignee.iloc[:, :2].copy()
                df_plot.columns = ['Name', 'Count']
                df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
                df_plot = df_plot.dropna(subset=['Count']).sort_values('Count', ascending=True).tail(15)
                
                if not df_plot.empty:
                    fig = px.bar(df_plot, x='Count', y='Name', orientation='h', title="專利權人排名 (Top 15).", 
                                    text='Count', color='Count', color_continuous_scale='Blues')
                    Parser._style_web_figure(fig, left_margin=210, bottom_margin=56)
                    Parser._style_bar_labels(fig)
                    fig.update_layout(showlegend=False, coloraxis_showscale=False)
                    cache_figure("assignee", fig)
            else:
                _notify(callback, "warning", "專利權人表格欄位不足")

        # === Tab 3: 主要布局國家 ===
        if diagram_buffers.get("country"):
            df_country = Parser.parse_html_table(diagram_buffers["country"])
            if df_country is not None and len(df_country.columns) >= 2:
                df_plot = df_country.iloc[:, :2].copy()
                df_plot.columns = ['Country', 'Count']
                df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
                df_vis = df_plot.head(10).sort_values(by='Count', ascending=True)

                fig = px.bar(df_vis, x='Count', y='Country', orientation='h', title="全球專利佈局 (Top 10)",
                                text='Count', color='Count', color_continuous_scale='Viridis')
                Parser._style_web_figure(fig, height=500, left_margin=150, bottom_margin=56)
                Parser._style_bar_labels(fig)
                fig.update_layout(showlegend=False, coloraxis_showscale=False)
                cache_figure("country", fig)

        # === Tab 4: 專利申請趨勢 ===
        if diagram_buffers.get("trend_range"):
            df_trend = Parser.parse_html_table(diagram_buffers["trend_range"])
            if df_trend is not None and len(df_trend.columns) >= 2:
                df_plot = df_trend.iloc[:, :2].copy()
                df_plot.columns = ['Year', 'Count']
                df_plot['Count'] = pd.to_numeric(df_plot['Count'].astype(str).str.replace(',', ''), errors='coerce')
                
                fig = px.line(df_plot, x='Year', y='Count', markers=True, title="申請趨勢", 
                                color_discrete_sequence=px.colors.qualitative.Pastel)
                Parser._style_web_figure(fig, height=500, left_margin=72, bottom_margin=72)
                fig.update_traces(line=dict(width=3, color="#38bdf8"), marker=dict(size=8, color="#f8fafc"))
                cache_figure("trend_range", fig)

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

                    Parser._style_web_figure(
                        fig,
                        height=dynamic_height,
                        left_margin=170,
                        bottom_margin=90,
                        top_margin=150,
                    )
                    fig.update_layout(
                        xaxis={'side': 'top', 'tickangle': -30, 'dtick': 1, 'automargin': True, 'fixedrange': True},
                        yaxis={'autorange': "reversed", 'dtick': 1, 'automargin': True, 'fixedrange': True},
                        height=dynamic_height,
                        showlegend=False
                    )
                    fig.update_xaxes(tickfont=dict(size=11))
                    fig.update_yaxes(tickfont=dict(size=11))
                    fig.update_traces(
                        textposition='middle center',
                        textfont={'color': 'white', 'weight': 'bold', 'size': 11},
                        marker=dict(line=dict(color="rgba(255,255,255,0.45)", width=1)),
                    )
                    cache_figure("matrix", fig)
                else:
                    _notify(callback, "warning", "矩陣數據為空")

            except Exception as e:
                _notify(callback, "warning", f"矩陣解析錯誤: {e}")

        return fig_buffers, img_buffers

    
    @staticmethod
    def parse_query(query):
        """
        從檢索字串中擷取 IC (IPC/CPC) 範圍，自動去除括號。
        """
        # Regex 解析：
        # 1. \(?       -> 匹配開頭可選的左括號 '('
        # 2. (IC=[^)]+) -> 【捕獲群組】抓取 IC= 開頭，且內容不包含 ')' 的所有字元
        # 3. \)?       -> 匹配結尾可選的右括號 ')'
        pattern = r"\(?(IC=[^)]+)\)?"
        
        # 搜尋所有符合的片段 (通常 IPC 設定會在最後面，我們取最後一個匹配的或是特定的)
        match = re.search(pattern, query)
        
        if match:
            # group(1) 會自動排除掉括號，只回傳中間的內容
            return match.group(1).strip()
        return None
    
    @staticmethod
    def is_valid_parentheses(text):
        """
        檢查字串中的括號是否對稱且正確閉合。
        支援: (), [], {}
        忽略括號以外的其他文字。
        """
        stack = []
        # 建立一個對照表，Key 是右括號，Value 是對應的左括號
        mapping = {
            ')': '(',
            ']': '[',
            '}': '{'
        }

        for char in text:
            # 1. 如果是左括號，放入堆疊 (Push)
            if char in mapping.values():
                stack.append(char)
            
            # 2. 如果是右括號
            elif char in mapping:
                # 情況 A: 堆疊是空的 (代表有右括號但前面沒有左括號) -> 錯誤
                if not stack:
                    return False
                
                # 情況 B: 取出堆疊最上面的左括號 (Pop)
                top_element = stack.pop()
                
                # 檢查是否匹配 (例如 ')' 必須配對 '(')
                if mapping[char] != top_element:
                    return False

        # 3. 迴圈結束後，如果堆疊是空的，代表全部抵銷完畢 -> 正確
        # 如果堆疊還有剩，代表有左括號沒閉合 -> 錯誤
        return len(stack) == 0
