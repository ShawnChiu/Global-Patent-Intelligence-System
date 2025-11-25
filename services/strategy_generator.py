import google.generativeai as genai
import json
import pandas as pd

class MatrixStrategy:
    @staticmethod
    def generate_gpss_strategy(df, api_key):
        """
        通用版：自動偵測領域，並生成該領域的矩陣關鍵字與布林檢索式
        """
        if df.empty or not api_key:
            return None, "資料不足或無 Key"

        # 1. 準備文本 (取前 300 篇，混合標題與摘要)
        # 這裡我們多抓一點資訊，讓 AI 能準確判斷領域
        corpus = ""
        for i, row in df.head(min(300, len(df))).iterrows():
            title = row.get('Title', 'Unknown')
            abstract = str(row.get('Abstract', ''))
            corpus += f"[{i+1}] {title}\nAbs: {abstract}\n\n"

        # 2. 設定 Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash') # Flash 夠快且通用性好

        # 3. 通用型 Prompt (General Purpose Prompt)
        # 關鍵：不指定領域，要求 AI "Infer" (推論) 領域
        prompt = f"""
        Role: Expert Patent Strategist & Multilingual Translator.
        
        Task: Analyze the patent corpus to discover the technology domain and construct a "Technology-Efficacy Matrix" strategy.
        
        [Input Patent Corpus]
        {corpus}

        [Analysis Steps]
        1. **Domain Detection**: Determine the core technology field.
        2. **Taxonomy Extraction**:
        - Identify 6 distinct **"Technical Means"** (X-Axis).
        - Identify 6 distinct **"Efficacy/Effects"** (Y-Axis).
        3. **Multilingual Query Construction** (CRITICAL):
        For EACH category, construct a precise Boolean Query string.
        - **Keywords**: Include English, Traditional Chinese, Simplified Chinese, Japanese, and Korean terms.
        - **Logic**: 
            - Use **OR** for synonyms (e.g., "Projector" OR "Light Engine").
            - Use **AND** if combining concepts is necessary for precision (e.g., "Eye" AND "Tracking").
            - Use **NOT** to exclude obvious ambiguity if needed.
            - **Parentheses**: Use parentheses `()` to group logic correctly.

        [Output Format]
        Return a JSON object. Do NOT include markdown code blocks.
        Structure:
        {{
            "domain_detected": "Detected Field Name",
            "technologies": [
                {{"label": "Category Name", "boolean": "(Complex Boolean String)"}},
                ...
            ],
            "efficacies": [
                {{"label": "Category Name", "boolean": "(Complex Boolean String)"}}
            ]
        }}
        
        [Constraint]
        - Ensure the boolean string is syntactically valid for patent search systems.
        - Do not label the language inside the string.
        """

        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2 # 保持低溫以確保格式穩定
                }
            )
            return json.loads(response.text), "Success"
        except Exception as e:
            return None, f"AI Error: {str(e)}"