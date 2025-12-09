import PyInstaller.__main__
import streamlit
import os
import re
def get_hidden_imports_from_requirements(file_path):
    """
    讀取 requirements.txt 並轉成 PyInstaller 的 hidden-import 格式
    """
    hidden_imports = []
    
    if not os.path.exists(file_path):
        print(f"⚠️ 警告: 找不到 {file_path}，將跳過自動匯入。")
        return hidden_imports

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 去除空白與註解
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 處理版本號 (例如: pandas==1.5.3 -> pandas)
            # 使用正則表達式，只要遇到 ==, >=, <=, >, <, ~= 就切斷
            package_name = re.split(r'[><=~]', line)[0].strip()
            
            if package_name:
                # 特別處理: 有些套件安裝名稱跟 import 名稱不一樣
                # 這裡列出常見的例外，你可以自己補充
                if package_name == "python-dotenv":
                    package_name = "dotenv"
                elif package_name == "scikit-learn":
                    package_name = "sklearn"
                elif package_name == "Pillow":
                    package_name = "PIL"
                elif package_name == "google-generativeai":
                    package_name = "google.generativeai"
                elif package_name == "playwright":
                    # Playwright 有時候比較頑固，我們多加幾個相關模組
                    hidden_imports.append('--hidden-import=playwright')
                    hidden_imports.append('--hidden-import=playwright.sync_api')
                    hidden_imports.append('--hidden-import=playwright.async_api')
                    # 它是 package_name 本身，所以下面這行不做事也沒關係，但為了邏輯一致：
                    package_name = "playwright"
                elif package_name == "python-docx":
                    package_name = "docx"
                
                hidden_imports.append(f'--hidden-import={package_name}')
    
    print(f"📦 自動載入 {len(hidden_imports)} 個套件 from requirements.txt")
    return hidden_imports

# ... (前面讀取 requirements 的函式保持不變) ...

# ==================================================
# 主程式
# ==================================================

streamlit_path = os.path.dirname(streamlit.__file__)
static_path = os.path.join(streamlit_path, "static")
runtime_path = os.path.join(streamlit_path, "runtime")

# 1. 定義你要打包的額外資料夾 (除了 services，如果你有 pages, utils 也要寫在這裡)
# 格式: "資料夾名稱"
extra_folders = [
    "services",   # <--- 這裡加入你的 services 資料夾
    "models",
    "views",
    # "pages",    # 如果你有 Streamlit 的多頁面功能，這個也要加
    # "utils",    # 如果你有工具資料夾
    # "components",
]

pyinstaller_args = [
    'run.py',
    '--onefile',
    '--clean',
    '--copy-metadata=streamlit',
    f'--add-data={static_path};streamlit/static',
    f'--add-data={runtime_path};streamlit/runtime',
    '--hidden-import=docx',
    '--hidden-import=playwright.sync_api',  # 既然都手動了，這幾個也建議手動加保險
    '--hidden-import=google.generativeai',
    f'--add-data=config.py;.',
    '--add-data=main.py;.',
]

# 2. 自動把 extra_folders 加入參數
for folder in extra_folders:
    if os.path.exists(folder):
        # 語法: --add-data="來源資料夾;目標資料夾"
        # 這裡把 services 複製到 exe 內部的根目錄下的 services
        pyinstaller_args.append(f'--add-data={folder};{folder}')
        print(f"📂 已加入資料夾: {folder}")
    else:
        print(f"⚠️ 警告: 找不到資料夾 {folder}，跳過。")

# 3. 讀取 requirements 並加入 hidden imports
req_imports = get_hidden_imports_from_requirements('requirements.txt')
pyinstaller_args.extend(req_imports)

print("🚀 開始打包中...")
PyInstaller.__main__.run(pyinstaller_args)
print("✅ 打包完成！")