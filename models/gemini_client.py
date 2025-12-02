import google.generativeai as genai
import json
import pandas as pd
import io

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

        Task: Convert the user's "Patent Analysis Topic" into a syntactically perfect Boolean Search Query.

        [CRITICAL CONSTRAINT: LENGTH LIMIT]
        The system has a strict limit of 1900 bytes. Since CJK (Chinese/Japanese/Korean) characters take up 3 bytes each:
        1. **Language Priority**: English > Traditional Chinese > Simplified Chinese > Japanese > Korean.
        2. **Drop Low-Value Terms**: If a term is very generic (e.g., "System", "Method"), do not expand it into all languages.

        [CRITICAL RULE: SYNTAX INTEGRITY]
        1. **Balanced Parentheses**: Ensure every opening `(` has a matching closing `)`.
        2. **Structure**: Follow the "Strict Syntax Template" rigidly.

        [Strict Syntax Template]
        ( ( <POSITIVE_KEYWORDS> ) ) NOT ( <NEGATIVE_KEYWORDS>@TI ) AND ID=:20241231 AND ( <IPC_CODES> )

        [Construction Steps]
        1. **Positive Keywords**:
        - Identify core concepts.
        - Expand into 5 languages (EN, TC, SC, JP, KR).
        - **LIMIT**: Max 3 synonyms per language to save space.
        - Example: `( (Car OR 車 OR 自動車)@TI,AB,CL,DE AND (Battery OR 電池)@TI,AB,CL,DE )`

        2. **Negative Keywords (Noise Filtering)**:
        - Identify irrelevant keywords.
        - **Keep it brief**: Use broadly excluding terms.
        - Apply `@TI` ONLY.

        3. **IPC Classification**:
        - Infer relevant IPC codes (e.g., G06F*).
        - Combine with OR.

        [Reference Example]
        Input Topic: "駛入新視界：智慧座艙AR-HUD專利分析與布局"
        Target Output: ( ( (HUD OR Head Up Display OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ)@TI,AB,CL,DE AND (AR OR Augmented Reality OR 擴增實境 OR Waveguide OR 光波導)@TI,AB,CL,DE ) ) NOT ( (Helmet OR Wearable OR Glasses OR VR OR 穿戴式 OR 頭盔 OR 眼鏡)@TI ) AND ID=:20241231 AND (IC=G02B* OR IC=B60K*)

        [New Topic]
        {topic}

        [Output]
        Return ONLY the raw Boolean Query String. Do NOT include markdown blocks.
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