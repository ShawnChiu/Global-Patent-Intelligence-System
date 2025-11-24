# 🌐 GPIS - Global Patent Intelligence System
### 全球專利情資自動化分析系統

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red) ![Plotly](https://img.shields.io/badge/Visualization-Plotly-green) ![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## 📖 專案簡介 (Introduction)

**GPIS** 是一套專為智慧財產權分析設計的自動化工具。有別於傳統手動檢索與 Excel 整理的繁瑣流程，本系統採用 **Data-Driven** 的方法，透過 API 直接獲取結構化數據，並即時進行資料清洗與視覺化分析。

本專案特別針對「智慧座艙 AR-HUD」等新興科技議題設計，具備動態關鍵字定義功能，可產出符合產業分析標準的「技術功效矩陣圖」。

## ✨ 核心功能 (Key Features)

* **🚀 自動化 ETL 流程**：自動呼叫 GPSS API，支援多國 (TW/US/CN/JP/WO) 專利數據的擷取、解析與清洗。
* **📊 互動式視覺化**：
    * **技術領域分析**：自動統計 IPC 分類號，識別核心技術。
    * **全球佈局戰場**：分析專利申請國別，掌握市場熱點。
    * **申請趨勢圖**：繪製歷年專利數量，判斷技術生命週期。
* **💡 技術功效矩陣 (Tech-Efficacy Matrix)**：
    * 內建關鍵字掃描演算法 (Rule-based Text Mining)。
    * 自動分析專利摘要 (Abstract)，將專利歸類至「技術手段」與「達成功效」象限。
    * 支援使用者在 UI 上動態自定義矩陣定義，無需修改程式碼。

## 🛠️ 技術堆疊 (Tech Stack)

本專案採用 **MVC (Model-View-Controller)** 架構設計，確保程式碼的低耦合與可維護性：

* **Language**: Python 3.x
* **Web Framework**: Streamlit (快速構建互動式資料應用)
* **Data Processing**: Pandas (資料清洗與結構化處理)
* **Visualization**: Plotly Express (互動式圖表繪製)
* **Networking**: Requests (RESTful API 串接)

## 📂 專案結構 (Project Structure)

```text
GPIS_Project/
├── main.py               # [Controller] 程式入口點
├── config.py             # [Config] 全域參數與預設矩陣定義
├── models/               # [Model] 資料層
│   └── gpss_client.py    # 封裝 GPSS API 連線與錯誤處理
├── services/             # [Service] 商業邏輯層
│   └── analyzer.py       # 負責矩陣運算與關鍵字匹配邏輯
└── views/                # [View] 介面層
    └── components.py     # 負責 Streamlit UI 渲染與圖表繪製
