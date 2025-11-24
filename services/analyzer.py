# services/analyzer.py
import pandas as pd

class PatentAnalyzer:
    """負責進行數據處理與分析的服務"""

    @staticmethod
    def parse_config_text(text):
        """解析使用者輸入的規則字串 -> Dictionary"""
        rules = {}
        for line in text.strip().split('\n'):
            if ':' in line:
                key, vals = line.split(':', 1)
                rules[key.strip()] = [v.strip().lower() for v in vals.split(',')]
        return rules

    @staticmethod
    def generate_matrix(df, tech_config, effect_config):
        """執行技術功效矩陣分析"""
        if df.empty:
            return None

        tech_rules = PatentAnalyzer.parse_config_text(tech_config)
        effect_rules = PatentAnalyzer.parse_config_text(effect_config)
        
        matrix_data = []
        
        # 向量化處理會更快，但為了邏輯清晰，這裡維持迭代
        # 先把全文合併並轉小寫，加速比對
        df['FullText'] = (df['Title'] + " " + df['Abstract']).str.lower()

        for _, row in df.iterrows():
            text = row['FullText']
            
            # 找出這篇專利符合哪些技術
            matched_techs = [t for t, kws in tech_rules.items() if any(k in text for k in kws)]
            # 找出這篇專利符合哪些功效
            matched_effects = [e for e, kws in effect_rules.items() if any(k in text for k in kws)]
            
            # 產生關聯對 (Pairs)
            for t in matched_techs:
                for e in matched_effects:
                    matrix_data.append({'Technology': t, 'Efficacy': e})
        
        if not matrix_data:
            return None
            
        return pd.DataFrame(matrix_data)