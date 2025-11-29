# 檔案位置：config.py (在專案根目錄，與 main.py 同層)

# API 設定
API_URL = "https://tiponet.tipo.gov.tw/gpss1/gpsskmc/gpss_api"
DEFAULT_USER_CODE = ""
DEFAULT_GEMINI_API = ""

# 預設矩陣定義
DEFAULT_TECH_CONFIG = """PGU: (projector OR pgu OR light engine OR 光機)
Combiner: (waveguide OR combiner OR holographic OR 光波導)
Reflector: (mirror OR reflection OR 反射鏡)
Windshield: (windshield OR glass OR 擋風玻璃)"""

DEFAULT_EFFECT_CONFIG = """FOV: (fov OR field OR view OR 視場 OR 廣角)
VID: (vid OR distance OR depth, OR 虛像距離)
3D: (3d OR stereoscopic OR 立體)
Image Quality: (resolution OR contrast OR 清晰 OR 畫質)"""