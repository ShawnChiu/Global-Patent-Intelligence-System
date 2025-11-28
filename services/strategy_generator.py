import google.generativeai as genai
import json
import pandas as pd

class BooleanRetrievalGenerator:
    @staticmethod
    def convert_topic_to_query(topic, api_key):
        """
        將簡單的主題名稱（如 '固態電池'）轉換為 GPSS 專用的超複雜布林檢索式
        """
        if not api_key: return "Error: Missing API Key"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # 用 Flash 比較快且便宜
        
        # 這裡貼上上面的 prompt 變數
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
        Role: Expert Patent Strategist & Taxonomist.
        
        Task: Analyze the provided patent corpus (Sample Patents) to automatically discover the technology domain and construct a "Technology-Efficacy Matrix" strategy.
        
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