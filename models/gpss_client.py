# models/gpss_client.py
import requests
import pandas as pd
from config import API_URL

class GPSSClient:
    """負責與 GPSS API 進行通訊的客戶端類別"""
    
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_data(self, query, qty):
        """
        發送請求並回傳原始 DataFrame
        """
        params = {
            "userCode": self.api_key,
            "patDB": "TWA,TWB,USA,USB,CNA,CNB,JPA,JPB",
            "patAG": "A,B",
            "patTY": "I,M",
            "expFmt": "json",
            "expQty": str(qty),
            "expFld": "TI,AB,IC,AD,PN", # 只取需要的欄位
            "TI": query,
            "IC": ""
        }

        try:
            response = requests.get(API_URL, params=params, timeout=60)
            response.raise_for_status() # 檢查 HTTP 錯誤
            
            data = response.json()
            return self._parse_response(data)
            
        except Exception as e:
            raise RuntimeError(f"API 連線失敗: {str(e)}")

    def _parse_response(self, data):
        """內部方法：解析 GPSS 特有的巢狀 JSON"""
        api_resp = data.get("gpss-API", {})
        status = api_resp.get("status")
        
        if status == "fail" or api_resp.get("message") == "No record found":
            raise ValueError(f"API 錯誤: {api_resp.get('message')}")

        raw_list = api_resp.get("patent", {}).get("patentcontent", [])
        if not raw_list:
            return pd.DataFrame()

        # 資料正規化 (Flatten)
        cleaned_list = []
        for p in raw_list:
            cleaned_list.append({
                "Title": p.get("patent-title", {}).get("title", ""),
                "Abstract": self._get_text(p.get("abstract", {}).get("p", "")),
                "Year": p.get("application-reference", {}).get("date", "")[:4],
                "Country": p.get("publication-reference", {}).get("doc-number", "")[:2],
                "IPC": self._get_ipc(p.get("classifications-ipc", {}).get("ipc", []))
            })
            
        return pd.DataFrame(cleaned_list)

    def _get_text(self, obj):
        return "".join(obj) if isinstance(obj, list) else str(obj)

    def _get_ipc(self, ipc_list):
        if isinstance(ipc_list, list) and len(ipc_list) > 0:
            # 取第一個 IPC 的主類 (例如 G02B)
            return ipc_list[0].get("keyValue", "").split("/")[0]
        return "Unknown"