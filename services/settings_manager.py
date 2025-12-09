# 檔案：settings_manager.py
import json
import os
from dataclasses import dataclass, asdict
import config
import sys

def get_project_root():
    """
    智慧判斷專案根目錄：
    1. 打包後 (.exe)：回傳 exe 所在的資料夾 (視為根目錄)。
    2. 開發時 (.py)：因為腳本在 services 內，所以回傳腳本的「上一層」資料夾。
    """
    if getattr(sys, 'frozen', False):
        # --- 打包模式 (Frozen) ---
        # sys.executable 是 .exe 的完整路徑
        # dirname(sys.executable) 就是 .exe 所在的資料夾
        return os.path.dirname(sys.executable)
    else:
        # --- 開發模式 (Development) ---
        # __file__ 是 settings_manager.py 的路徑 (.../services/settings_manager.py)
        # 第一個 dirname 拿到 .../services
        # 第二個 dirname 拿到 .../ (即根目錄)
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.dirname(base_path)

# 設定檔案路徑
SETTINGS_FILE = os.path.join(get_project_root(), ".data", "user_settings.json")


@dataclass
class UserSettings:
    gpss_id: str = config.DEFAULT_GPSS_ID
    gpss_pw: str = config.DEFAULT_GPSS_PW
    tech_config: str = config.DEFAULT_TECH_CONFIG
    effect_config: str = config.DEFAULT_EFFECT_CONFIG
    gemini_api_key: str = config.DEFAULT_GEMINI_API_KEY
    query: str = config.DEFAULT_QUERY
    name : str = config.DEFAULT_NAME
    student_id : str = config.DEFAULT_STUDENT_ID
    matrix = config.DEFAULT_MATRIX

class SettingsManager:
    def __init__(self, filepath=SETTINGS_FILE):
        self.filepath = filepath
        self.settings = self._load_settings()

    def _load_settings(self) -> UserSettings:
        default_settings = UserSettings()
        if not os.path.exists(self.filepath):
            return default_settings
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            current_data = asdict(default_settings)
            current_data.update(data)
            valid_keys = default_settings.__dict__.keys()
            clean_data = {k: v for k, v in current_data.items() if k in valid_keys}
            return UserSettings(**clean_data)
        except Exception:
            return default_settings

    def save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存失敗: {e}")


# ==========================================
# 【關鍵】：在這裡直接實例化
# ==========================================
setmgr = SettingsManager()