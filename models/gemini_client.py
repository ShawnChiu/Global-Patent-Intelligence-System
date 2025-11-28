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

        Task: Convert the user's "Patent Analysis Topic" into a comprehensive, professional-grade Boolean Search Query string following the strict syntax of GPSS.

        [Reference Example]
        Input Topic: "駛入新視界：智慧座艙AR-HUD專利分析與布局"
        Target Output: (((HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이)@TI,AB,CL,DE AND (head)@TI,AB,CL AND (UP)@TI,AB,CL AND (DISPLAY OR DISPLAYS)@TI,AB,CL) OR ((AR OR Augmented Reality OR 擴增實境 OR 扩增现实 OR 拡張 現実 OR 증강현실 OR HOE OR Hologram OR Holography OR Holographic OR 全息投影 OR 全息 OR ホログラフィック OR 홀로그래피 OR Waveguide OR 光波導 OR 光波导 OR ウ ェーブガイド OR 도파관 OR 3D OR Three Dimentional OR Multi-Depth OR 三維 OR 三维 OR 三元 OR 입체적인 OR Pupil expander OR Pupil expansion OR Eye OR Eyebox OR Steerable Eyebox OR Eye Tracking OR Eye Tracker OR Naked Eye OR 瞳孔 OR 虹膜 OR 眼 OR 目 OR 눈)@TI AND (HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレ イ OR 헤드 업디스플레이)@TI,AB,CL,DE) NOT (Wearable OR Portable OR HeadMounted OR Helmet OR Glasses OR Aircraft OR Flight OR Plane OR Medical OR Mask OR Surgery OR Game OR VR OR 穿戴式 OR 便攜的 OR 頭戴式 OR 頭盔 OR 眼鏡 OR 飛機 OR 航班 OR 飛機 OR 醫療的 OR 口罩 OR 手術 OR 遊戲 OR 虛擬實境 OR 可穿戴 OR 便携式 OR 头戴式 OR 头盔 OR 眼镜 OR 飞机 OR 飞行 OR 医疗 OR 口罩 OR 外科手术 OR 游戏 OR 虚拟现实 OR ウェアラブル OR ポータブル OR ヘッドマウント OR ヘルメット OR メガネ OR 航空機 OR フライト OR 飛行機 OR 医療 OR マスク OR 外科 OR ゲーム OR 仮想現実 OR 착용형 OR 휴대용 OR 헤드 마운트형 OR 헬멧형 OR 안경형 OR 항공기 OR 비행 OR 비행기 OR 의료 OR 마스크 OR 외과 OR 게임 OR 가상현실 )@TI) AND ID=:20241231 AND (IC=G02B* OR IC=B60J* OR IC=B60K* OR IC=B60R*)

        [Construction Rules]
        Based on the "Reference Example" above, construct a query for the "New Topic" provided below. You must follow these steps:

        1.  **Core Concept Extraction**: Identify the core technology (e.g., "HUD") and the enabling technology (e.g., "AR").
        2.  **Multilingual Expansion (Critical)**: For EVERY key term, you MUST expand it into:
            * English (including acronyms)
            * Traditional Chinese (繁體)
            * Simplified Chinese (简体)
            * Japanese (Katakana/Kanji)
            * Korean (Hangul)
        3.  **Synonym Injection**: Include technical synonyms (e.g., for AR-HUD, include "Waveguide", "Holographic", "Eye Tracking").
        4.  **Noise Filtering (NOT Logic)**: Identify application scenarios that are NOT relevant to the topic (e.g., if the topic is "Automotive", exclude "Helmet", "Medical", "Gaming") and add them to a NOT condition restricted to @TI (Title).
        5.  **IPC Classification**: Infer the most relevant IPC codes (e.g., G02B for optics, H01M for batteries) and append them at the end using `(IC=... OR IC=...)`.
        6.  **Syntax Formatting**:
            * Use `@TI,AB,CL,DE` for broad inclusion.
            * Use `@TI` for strict exclusion (NOT).
            * Use `ID=:20241231` as the date constraint.

        [New Topic]
        {topic}

        [Output]
        Return ONLY the raw Boolean Query String. Do not include markdown code blocks or explanations.
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
            return None, f"AI Error: {str(e)}"