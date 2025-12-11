# 🌐 GPIS - Global Patent Intelligence System
### 全球專利自動化分析系統

這是一個自動化的專利分析工具，旨在協助使用者從 **全球專利檢索系統 (GPSS)** 快速獲取專利數據，並進行視覺化分析與報告生成。系統整合了 **Google Gemini AI**，可自動生成布林檢索式 (Boolean Query) 與技術功效矩陣分類，大幅降低專利分析的門檻。

## ✨ 主要功能

  * **自動化 GPSS 登入與檢索**：使用 Playwright 自動通過驗證碼 (OCR) 登入並執行檢索。
  * **雙模式檢索設定**：
      * **規則式 (Rule-based)**：手動輸入或使用預設範本。
      * **AI 推論 (Gemini LLM)**：輸入自然語言主題，由 AI 自動生成符合語法的布林檢索式。
  * **多維度圖表分析**：
      * IPC 技術領域分類
      * 技術領先企業 (Assignee)
      * 主要布局國家
      * 專利申請趨勢
  * **技術功效矩陣 (Tech-Efficacy Matrix)**：自動抓取專利摘要，利用關鍵字或 AI 語意分析進行矩陣歸類。
  * **一鍵生成報告**：自動將分析結果、圖表與詮釋資料彙整為 `.docx` 格式的期末報告。
  * **單一執行檔打包**：內建 PyInstaller 腳本，可將 Streamlit 應用打包為 `.exe` 執行檔。

## 🛠️ 技術架構

  * **UI 框架**: [Streamlit](https://streamlit.io/)
  * **網頁自動化**: [Playwright](https://playwright.dev/)
  * **生成式 AI**: [Google Gemini API](https://ai.google.dev/)
  * **數據處理**: Pandas, EasyOCR (驗證碼辨識)
  * **視覺化**: Plotly
  * **報告生成**: Python-docx

## ⚙️ 安裝說明

### 1\. 環境需求

  * Python 3.9 或以上版本
  * Google Chrome 瀏覽器 (供 Playwright 使用)

### 2\. 安裝依賴套件

請確保目錄下有 `requirements.txt` ，然後執行：

```bash
pip install -r requirements.txt
```

### 3\. 安裝 Playwright 瀏覽器核心

系統需要 Chromium 核心來執行爬蟲：

```bash
playwright install chromium
```

## 🚀 執行方式

### 開發模式 (Development)

直接使用 Streamlit 啟動：

```bash
streamlit run main.py
```

或者使用包裝好的啟動腳本 (會自動開啟瀏覽器)：

```bash
python run.py
```

### 打包為執行檔 (Build .exe)

本專案包含 `build.py`，可將環境打包為獨立的 `.exe` 檔案 (Windows)：

```bash
python build.py
```

*打包完成後，執行檔將位於 `dist/` 資料夾中。*

## 📖 使用指南

1.  **啟動系統**：執行程式後，瀏覽器將自動開啟操作介面。
2.  **設定基本資料**：
      * 於側邊欄點擊「✏️ 點擊編輯基本資料」。
      * 輸入您的 **GPSS 帳號** 與 **密碼** (必填，用於爬蟲登入)。
      * (選填) 輸入 **Gemini API Key** 以啟用 AI 輔助功能。
3.  **選擇主題**：
      * 可選擇預設範例 (如：智慧座艙 AR-HUD、矽光子技術...)。
      * 或選擇「自訂」並輸入感興趣的技術關鍵字。
4.  **開始分析**：
      * 點擊「🚀 開始分析」。
      * 系統將自動執行：登入 -\> 檢索 -\> 抓圖 -\> 矩陣分析 -\> 生成報告。
5.  **下載報告**：分析完成後，頁面頂端會出現下載按鈕，可取得完整的 Word 報告。

## 📂 專案結構

```text
.
├── main.py                 # Streamlit 主程式入口
├── run.py                  # 開發環境啟動腳本 (Wrapper)
├── build.py                # PyInstaller 打包腳本
├── config.py               # 預設參數與範例資料
├── requirements.txt        # (需自行建立) 依賴套件列表
├── models/
│   ├── gemini_client.py    # Google Gemini API 串接
│   └── gpss_client.py      # GPSS 爬蟲與自動化邏輯
├── services/
│   ├── workflow.py         # 主要業務邏輯控制
│   ├── state.py            # Session State 管理
│   ├── settings_manager.py # 使用者設定存取 (.data/user_settings.json)
│   ├── parser.py           # 表格解析與圖表繪製
│   ├── gen_report.py       # Word 報告生成器
│   └── captcha.py          # 驗證碼辨識 (EasyOCR)
└── views/
    └── components.py       # Streamlit UI 元件與 Dialog
```

## ⚠️ 注意事項

1.  **GPSS 帳號**：本系統僅提供自動化操作工具，使用者需自行擁有合法的 GPSS 帳號權限。
2.  **驗證碼辨識**：登入時使用 OCR 辨識驗證碼，若失敗系統會自動重試 (預設 10 次)，若網路不穩或驗證碼過於複雜可能導致登入失敗。
3.  **Kaleido**：圖表轉圖片功能依賴 `kaleido` 套件，建議使用 `0.2.1` 版本以確保穩定性。

## ⚖️ 免責聲明

本工具僅供 IBG009301 智慧財產實戰策略 課程研究使用。請遵守 [經濟部智慧財產局全球專利檢索系統](https://www.google.com/search?q=https://gpss.tipo.gov.tw/) 之使用規範，請勿進行高頻率惡意爬取或用於商業營利行為。

## 👨‍💻 開發成員 (Contributors)

| 學號 (Student ID) |
| :---: |
| **B11315053** | 
| **B11315059** | 
| **B11330043** |

