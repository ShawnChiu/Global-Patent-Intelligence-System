import google.generativeai as genai
import json
import pandas as pd
import io
import os

class GeminiClient:

    def __init__(self, api_key):
        self.api_key = api_key

    def convert_topic_to_query(self, topic):
        """
        將簡單的主題名稱轉換為 GPSS 檢索式
        """
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        final_prompt = f"""
        Role: You are a Senior Patent Attorney and Search Expert specializing in the "Global Patent Search System (GPSS)".

        Task: Convert the user's "Patent Analysis Topic" into a syntactically perfect, MAXIMIZED Boolean Search Query.

        [CRITICAL GOAL: MAXIMIZE RICHNESS WITHIN LIMIT]
        The system allows up to **1600 bytes**. Your goal is to produce a query **between 1400 and 1600 bytes**.
        To achieve this:
        1. **Aggressive Expansion**: Do NOT limit yourself to 2-3 synonyms. List **as many relevant synonyms as possible** (5-10+ per language) for the core concepts.
        2. **Technical Granularity**: Include specific technical terms, acronyms, chemical formulas, component names, and spelling variations.
        3. **Language Coverage**: You MUST include English, Traditional Chinese, Simplified Chinese, Japanese, and Korean for ALL key concepts.
        
        [BYTE CALCULATION RULE]
        - English/Numbers: 1 Byte per char.
        - Chinese/Japanese/Korean: **3 Bytes** per char.
        - *Strategy*: Since CJK is expensive, prioritize a massive amount of English keywords, followed by a rich selection of CJK terms until the limit is approached.

        [CRITICAL RULE: SYNTAX INTEGRITY]
        1. **Balanced Parentheses**: Ensure every opening `(` has a matching closing `)`.
        2. **Structure**: Follow the "Strict Syntax Template" rigidly.

        [Strict Syntax Template]
        ( ( <POSITIVE_KEYWORDS> ) ) NOT ( <NEGATIVE_KEYWORDS>@TI ) AND ID=:20241231 AND ( <IPC_CODES> )

        [Construction Steps]
        1. **Positive Keywords (The Bulk of the Query)**:
        - Identify core concepts and sub-concepts.
        - **Expand Aggressively**: Use broader terms AND narrower specific terms (e.g., for "Display", use "Display", "Screen", "Panel", "OLED", "LCD", "Micro-LED"...).
        - Apply `@TI,AB,CL,DE` to the groups.
        - Structure: `( (Concept1_EN OR Concept1_TC OR Concept1_SC OR Concept1_JP OR Concept1_KR...)@TI,AB,CL,DE AND (Concept2...)@TI,AB,CL,DE )`

        2. **Negative Keywords (Noise Filtering)**:
        - Identify irrelevant keywords.
        - Keep it moderate.
        - Apply `@TI` ONLY.

        3. **IPC Classification**:
        - Include a comprehensive list of relevant IPC/CPC codes (e.g., G06F3/01, G06F3/048...).
        - Combine with OR.

        [Reference Example]
        Input Topic: "智慧座艙AR-HUD"
        Target Output (Truncated for brevity, but real output should be longer): 
        ( ( (HUD OR Head Up Display OR Head-Up-Display OR Heads Up Display OR 抬頭顯示器 OR 平視顯示器 OR 抬頭顯示 OR 平視顯示 OR ヘッドアップディスプレイ OR フロントガラス表示 OR 헤드 업 디스플레이 OR 전방 표시 장치)@TI,AB,CL,DE AND (AR OR Augmented Reality OR Mixed Reality OR Extended Reality OR XR OR MR OR 擴增實境 OR 增強現實 OR 混合實境 OR 光波導 OR Waveguide OR Holographic OR 全息 OR 虛實融合 OR 拡張現実 OR 複合現実 OR 拡張現実感 OR 증강 현실 OR 혼합 현실)@TI,AB,CL,DE ) ) NOT ( (Helmet OR Wearable OR Glasses OR VR OR Game OR Toy OR 穿戴式 OR 頭盔 OR 眼鏡 OR 遊戲 OR 玩具)@TI ) AND ID=:20241231 AND (IC=G02B* OR IC=B60K* OR IC=H04N*)

        [New Topic]
        {topic}

        [Output]
        Return ONLY the raw Boolean Query String. Do NOT include markdown blocks. 
        Ensure the string starts with `(` and checks out for balanced parentheses.
        """
        
        try:
            response = model.generate_content(final_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Generation Failed: {str(e)}"

    def _robust_read_file(self, input_data):
        """
        [暴力讀取版] 強力解析：
        1. 強制替換損壞的編碼字元 (encoding_errors='replace')
        2. 使用 python 引擎以支援自動分隔符偵測 (sep=None)
        """
        # 1. 如果已經是 DataFrame，直接回傳
        if isinstance(input_data, pd.DataFrame):
            return input_data

        # 2. 準備檔案內容 (File Content)
        file_content = None
        file_name = "unknown"

        try:
            if hasattr(input_data, 'name'):
                file_name = input_data.name
            
            # 讀取檔案串流
            if hasattr(input_data, 'read'):
                if hasattr(input_data, 'seek'):
                    input_data.seek(0)
                file_content = input_data.read()
            # 讀取檔案路徑
            elif isinstance(input_data, str):
                file_name = input_data
                with open(input_data, 'rb') as f:
                    file_content = f.read()
        except Exception as e:
            raise ValueError(f"檔案讀取失敗: {str(e)}")

        if not file_content:
            raise ValueError("檔案內容為空")

        # 3. 開始輪詢解析
        
        # --- 嘗試 A: 標準 Excel (.xlsx, .xls) ---
        try:
            return pd.read_excel(io.BytesIO(file_content))
        except Exception:
            pass 

        # --- 嘗試 B: CSV 解析 (暴力模式) ---
        # 關鍵修正：加入 'engine="python"' 和 'encoding_errors="replace"'
        encodings = ['utf-8', 'big5', 'cp950', 'gbk', 'utf-16']
        
        for enc in encodings:
            try:
                # 嘗試 1: 預設逗號分隔
                return pd.read_csv(
                    io.BytesIO(file_content), 
                    encoding=enc, 
                    on_bad_lines='skip',
                    encoding_errors='replace' # <--- 關鍵：遇到亂碼直接替換成問號，不報錯
                )
            except Exception:
                pass
            
            try:
                # 嘗試 2: 使用 Python 引擎自動偵測分隔符號 (處理 Tab 或其他分隔符)
                return pd.read_csv(
                    io.BytesIO(file_content), 
                    encoding=enc, 
                    sep=None, # 自動偵測
                    engine='python', # 必須搭配 python engine
                    on_bad_lines='skip',
                    encoding_errors='replace'
                )
            except Exception:
                continue

        # --- 嘗試 C: HTML 表格 ---
        try:
            dfs = pd.read_html(io.BytesIO(file_content), encoding='utf-8')
            if dfs: return dfs[0]
            
            dfs = pd.read_html(io.BytesIO(file_content), encoding='big5')
            if dfs: return dfs[0]
        except Exception:
            pass

        raise ValueError(f"無法識別檔案格式 (檔名: {file_name})。已嘗試所有編碼與讀取引擎均失敗。")

    def generate_gpss_strategy(self, input_data):
        """
        通用版：自動偵測領域，並生成該領域的矩陣關鍵字與布林檢索式
        """
        # --- 1. 讀取資料 ---
        df = None
        try:
            df = self._robust_read_file(input_data)
        except Exception as e:
            return None, f"Error: {str(e)}"

        if df is None or df.empty:
            return None, "Error: Empty dataset (讀取成功但資料為空)"

        # --- 2. 欄位對應 (Mapping) ---
        cols = df.columns
        clean_cols = [str(c).strip() for c in cols]
        
        title_col = None
        abstract_col = None

        t_keywords = ['Title', '專利名稱', 'Invention Title', 'TI', '標題', '名稱', 'Name']
        a_keywords = ['Abstract', '摘要', 'AB', 'Abstract of Disclosure', '簡介', 'Content']

        # 寬鬆匹配
        for k in t_keywords:
            match = next((c for c, clean in zip(cols, clean_cols) if k.lower() in clean.lower()), None)
            if match: 
                title_col = match
                break
        
        for k in a_keywords:
            match = next((c for c, clean in zip(cols, clean_cols) if k.lower() in clean.lower()), None)
            if match: 
                abstract_col = match
                break

        # 兜底
        if not title_col: title_col = cols[0]
        if not abstract_col and len(cols) > 1: abstract_col = cols[1]

        # --- 3. 準備文本 ---
        corpus = ""
        limit = min(300, len(df))
        
        for i in range(limit):
            row = df.iloc[i]
            
            t_val = row[title_col] if title_col in row else ""
            a_val = row[abstract_col] if abstract_col and abstract_col in row else ""
            
            title = str(t_val) if pd.notna(t_val) else "Unknown"
            abstract = str(a_val) if pd.notna(a_val) else ""
            
            title = title.replace('\n', ' ').strip()
            abstract = abstract.replace('\n', ' ').strip()
            
            corpus += f"[{i+1}] {title}\nAbs: {abstract}\n\n"

        if not corpus.strip():
            return None, "Error: 無法提取有效的標題與摘要文字。"

        # --- 4. Gemini API 呼叫 (保持不變) ---
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        Role: Expert Patent Strategist & Taxonomist.
        
        Task: Analyze the provided patent corpus (Sample Patents) to automatically discover the technology domain and construct a "Technology-Efficacy Matrix" strategy.
        
        [Input Patent Corpus]
        {corpus}

        [Analysis Steps]
        1. **Domain Detection**: Determine the core technology field.
        2. **Taxonomy Extraction**:
           - Identify 6 distinct **"Technical Means"** (X-Axis).
           - Identify 6 distinct **"Efficacy/Effects"** (Y-Axis).
        3. **Multilingual Query Construction**:
           - **Keywords**: Include English, Traditional Chinese, Simplified Chinese, Japanese, and Korean.
           - **Logic**: Use OR for synonyms, AND for precision, NOT for exclusion.
        
        [Output Format]
        Return a JSON object ONLY.
        Structure:
        {{
            "domain_detected": "Detected Field Name",
            "technologies": [
                {{"label": "Category Name", "boolean": "(Boolean String)"}}, ...
            ],
            "efficacies": [
                {{"label": "Category Name", "boolean": "(Boolean String)"}}
            ]
        }}
        """

        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2
                }
            )
            return json.loads(response.text), "Success"
        except Exception as e:
            return self.generate_gpss_strategy(input_data)