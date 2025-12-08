# 檔案位置：config.py (在專案根目錄，與 main.py 同層)

DEFAULT_NAME ="Good Leader 👍"
DEFAULT_STUDENT_ID = "B113150"

# API 設定
DEFAULT_GEMINI_API_KEY = ""
DEFAULT_GPSS_ID = ""
DEFAULT_GPSS_PW = ""

DEFAULT_QUERY = "(IGS OR \"International Games System\" OR 鈊象 OR \"インターナショナル ゲーム システム\" OR \"인터내셔널 게임 시스템\")@TI,AB,CL,DE AND ID=:20241231 AND (IC=A63F* OR IC=G07F* OR IC=G06F*)"

# 預設矩陣定義
DEFAULT_MATRIX = {}
DEFAULT_TECH_CONFIG = """PGU: (projector OR pgu OR light engine OR 光機)
Combiner: (waveguide OR combiner OR holographic OR 光波導)
Reflector: (mirror OR reflection OR 反射鏡)
Windshield: (windshield OR glass OR 擋風玻璃)"""

DEFAULT_EFFECT_CONFIG = """FOV: (fov OR field OR view OR 視場 OR 廣角)
VID: (vid OR distance OR depth, OR 虛像距離)
3D: (3d OR stereoscopic OR 立體)
Image Quality: (resolution OR contrast OR 清晰 OR 畫質)"""

EXAMPLE_CONFIG = {
    "智慧座艙 AR-HUD": {
        "main_boolean": "(((HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이)@TI,AB,CL,DE AND (head)@TI,AB,CL AND (UP)@TI,AB,CL AND (DISPLAY OR DISPLAYS)@TI,AB,CL) OR ((AR OR Augmented Reality OR 擴增實境 OR 扩增现实 OR 拡張現実 OR 증강현실 OR HOE OR Hologram OR Holography OR Holographic OR 全息投影 OR 全息 OR ホログラフィック OR ホログラフィ OR Waveguide OR 光波導 OR 光波导 OR ウェーブガイド OR 도파관 OR 3D OR Three Dimentional OR Multi-Depth OR 三維 OR 三维 OR 三元 OR 입체적인 OR Pupil expander OR Pupil expansion OR Eye OR Eyebox OR Steerable Eyebox OR Eye Tracking OR Eye Tracker OR Naked Eye OR 瞳孔 OR 虹膜 OR 眼 OR 目 OR 눈)@TI AND (HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイ OR 헤드 업 디스플레이)@TI,AB,CL,DE) NOT (Wearable OR Portable OR HeadMounted OR Helmet OR Glasses OR Aircraft OR Flight OR Plane OR Medical OR Mask OR Surgery OR Game OR VR OR 穿戴式 OR 便攜的 OR 頭戴式 OR 頭盔 OR 眼鏡 OR 飛機 OR 航班 OR 飛機 OR 醫療的 OR 口罩 OR 手術 OR 遊戲 OR 虛擬實境 OR 可穿戴 OR 便携式 OR 头戴式 OR 头盔 OR 眼镜 OR 飞机 OR 飞行 OR 医疗 OR 口罩 OR 外科手術 OR 游戏 OR 虚拟现实 OR ウェアラブル OR ポータブル OR ヘッドマウント OR ヘルメット OR メガネ OR 航空機 OR フライト OR 飛行機 OR 医療 OR マスク OR 外科 OR ゲーム OR 仮想現実 OR 착용형 OR 휴대용 OR 헤드 마운트형 OR 헬멧형 OR 안경형 OR 항공기 OR 비행 OR 비행기 OR 의료 OR マスク OR 外科 OR ゲーム OR 가상현실)@TI) AND (IC=G02B* OR IC=B60J* OR IC=B60K* OR IC=B60R*)",
        "matrix": {
            "technologies": [
                {
                    "label": "PGU(圖像生成器) ",
                    "boolean": "(PGU OR \"Picture Generation Unit\" OR TFT-LCD OR \"Thin Film Transistor Liquid Crystal Display\" OR LCOS OR \"Liquid Crystal On Silicon\" OR DLP OR \"Digital Light Processing\" OR MEMS OR \"Micro Electro Mechanical System\" OR \"Laser Beam\" OR microLED OR SLM OR \"Spatial Light Modulator\")@TI,AB,CL,DE"
                },
                {
                    "label": "Combiner(全息光學元件的組合器)",
                    "boolean": "(Waveguide OR Holography OR Holographic OR Hologram OR HOE OR \"Holographic Optical Elements\")@TI,AB,CL,DE"
                },
                {
                    "label": "Reflector(反射)",
                    "boolean": "(Reflector OR Reflection OR \"beam splitter\")@TI,AB,CL,DE"
                },
                {
                    "label": "Windshield(擋風玻璃及折射零件技術)",
                    "boolean": "(windshield OR windscreen OR \"Laminated Glass\" OR \"Wedge shaped\" OR pvb OR 檔風玻璃 OR 楔形膜 OR 夾層玻璃)@TI,AB,CL,DE"
                },
                {
                    "label": "Eye(駕駛視覺監控)",
                    "boolean": "(\"Pupil expander\" OR \"Pupil expansion\" OR Eye OR Eyebox OR \"Eye Tracking\" OR \"Eye Tracker\" OR \"Naked Eye\")@TI,AB,CL,DE"
                },
                {
                    "label": "Diffuser(擴散)",
                    "boolean": "(擴散器 OR 擴散片 OR Diffuser)@TI,AB,CL,DE"
                }
            ],
            "efficacies": [
                {
                    "label": "提升可視範圍(FOV)",
                    "boolean": "(FOV OR \"Field of view\" OR 可視範圍 OR 視野)@TI,AB,CL,DE"
                },
                {
                    "label": "增加虛擬距離(VID)",
                    "boolean": "(VID OR \"Virtual Image Distance\" OR 虚像距离 OR 虛擬距離 OR 虛像 )@TI,AB,CL,DE"
                },
                {
                    "label": "引導光線性質變化",
                    "boolean": "(Polarization OR 偏振 OR 偏光 OR Polarizing OR \"diffraction pattern\" OR Phase OR \"phase modulation\" OR amplitude)@TI,AB,CL,DE"
                },
                {
                    "label": "擴增視覺維度(3D)",
                    "boolean": "(AR OR \"Augmented Reality\" OR 擴增實境 OR 3D OR 三維 OR \"three dimensional\" OR \"MultiDepth\")@TI,AB,CL,DE"
                },
                {
                    "label": "增加視覺焦點平面(Focal)",
                    "boolean": "(\"Double-focal\" OR \"Multi focal\" OR\"Dual-focal\" OR \"two or more focal\" OR 多焦 OR 雙焦 OR planes OR planar OR 平面)@TI,AB,CL,DE"
                }
            ]
        }
    }
}