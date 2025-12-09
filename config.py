# 檔案位置：config.py (在專案根目錄，與 main.py 同層)

DEFAULT_NAME ="USER"
DEFAULT_STUDENT_ID = "B11315000"

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
    },
    "Immunocytokine 產業專利分析與布局": {
        "main_boolean": "(((((\"Antibody Drug Conjugate\") OR (ADC) OR (ADCs) OR (抗體藥物複合體) OR (抗體藥物偶聯物) OR (抗體—藥物複合物) OR (Immunoconjugates) OR (免疫結合物) OR (Immunocytokine) OR (免疫細胞因子)) AND ((\"Monoclonal Antibodies\") OR (mAb) OR (mAbs) OR (單株抗體) OR (cytokine) OR (細胞激素) OR (細胞因子) OR (細胞介素) OR (細胞活素) OR (細胞素))@CL,TI,AB AND ((Chemotherapy) OR (Chemo) OR (化學藥物治療) OR (化療) OR (Cancer) OR (癌症) OR (\"Autoimmune Disease\") OR (自體免疫性疾病) OR (\"Immunosuppressive drugs\") OR (\"Immunosuppressive agents\") OR (免疫抑制劑) OR (\"chimeric antigen receptor T cell\") OR (CAR-T) OR (嵌合抗原受體重組 T 細胞) OR (\"chimeric antigen receptor NK cell\") OR (CARNK) OR (嵌合抗原受體自然殺手細胞))@CL,TI,AB AND (IC=A61K-039/00* OR IC=A61K-047/50* OR IC=A61P-035/00* OR IC=A61P-037/00* OR IC=C07K-016/00* OR IC=C07K-014/52* OR IC=C07K-016/28) NOT ((\"DIAGNOSTIC AGENTS\") OR (診斷劑) OR (\"BACTERIAL MEMBRANE PREPARATIONS\") OR (細菌膜製劑) OR (\"BACTERIAL STRAINS\") OR (BACTERIA) OR (細菌) OR (\"BACTERIA-BASED VACCINES\") OR (VACCINE) OR (疫苗) OR (\"Ligand Drug Conjugates\") OR (配體藥物結合物) OR (RADIOIMMUNOTHERAPY) OR (\"CELL CRYOPRESERVATION\") OR (細胞冷凍保存培養基) OR (\"TREATMENT METHOD\") OR (治療方法) OR (配體) OR (Ligand))@TI) AND (IC=A* OR IC=C*) AND (IU=//[01:化學工業] OR IU=//[02:生技醫藥業])))",
        "matrix": {
            "technologies": [
                {
                    "label": "CAR-T cells",
                    "boolean": "靶向治療 OR \"Targeted therapy\" OR 免疫療法 OR \"Immunotherapy\" OR 抗原特異性 OR \"Antigen specificity\" OR 抗體結合 OR \"Antibody binding\" OR 腫瘤細胞殺傷 OR \"Tumor cell killing\" OR 抗體依賴性細胞毒性 OR \"Antibody-dependent cellular cytotoxicity\" OR ADCC OR 細胞內毒素釋放 OR \"Intracellular toxin release\" OR 癌症治療 OR \"Cancer treatment\" OR 腫瘤微環境 OR \"Tumor microenvironment\" OR 抗體修飾 OR \"Antibody modification\" OR 嵌合抗原受體 OR \"Chimeric antigen receptor\" OR T細胞活化 OR \"T cell activation\" OR 靶向抗原 OR \"Target antigen\" OR 腫瘤抗原 OR \"Tumor antigen\" OR 細胞療法 OR \"Cell therapy\" OR 基因工程 OR \"Genetic engineering\" OR 免疫逃逸 OR \"Immune evasion\" OR 腫瘤免疫 OR \"Tumor immunity\" OR 靶向傳遞 OR \"Targeted delivery\""
                },
                {
                    "label": "Gene-modified dendritic cells",
                    "boolean": "基因修飾 OR \"Gene modification\" OR 樹突狀細胞 OR \"Dendritic cells\" OR 抗原呈遞 OR \"Antigen presentation\" OR 免疫激活 OR \"Immune activation\" OR 癌症免疫療法 OR \"Cancer immunotherapy\" OR 基因工程 OR \"Genetic engineering\" OR 腫瘤免疫反應 OR \"Tumor immune response\" OR T 細胞活化 OR \"T cell activation\" OR 細胞因子釋放 OR \"Cytokine release\" OR 免疫調節 OR \"Immune modulation\" OR 腫瘤抗原 OR \"Tumor antigens\" OR 個性化癌症疫苗 OR \"Personalized cancer vaccines\" OR 免疫記憶 OR \"Immune memory\" OR 抗原特異性免疫反應 OR \"Antigen-specific immune response\" OR 免疫監控 OR \"Immune surveillance\" OR 細胞療法 OR \"Cell therapy\" OR 基因轉染 OR \"Gene transfection\" OR 免疫耐受 OR \"Immune tolerance\""
                },
                {
                    "label": "Gene therapy for immune cells",
                    "boolean": "基因治療 OR \"Gene therapy\" OR 免疫細胞 OR \"Immune cells\" OR T 細胞 OR \"T cells\" OR B 細胞 OR \"B cells\" OR NK 細胞 OR \"NK cells\" OR CAR-T 細胞療法 OR \"CAR-T cell therapy\" OR 基因編輯 OR \"Gene editing\" OR CRISPR OR Cas9 技術 OR CRISPR OR \"Cas9 technology\" OR 基因轉染 OR \"Gene transfection\" OR 基因修飾 OR \"Gene modification\" OR 免疫系統增強 OR \"Immune system enhancement\" OR 抗癌免疫療法 OR \"Anti-cancer immunotherapy\" OR 靶向治療 OR \"Targeted therapy\" OR 免疫調節 OR \"Immune modulation\" OR 腫瘤免疫反應 OR \"Tumor immune response\" OR 基因載體 OR \"Gene vectors\" OR 基因插入 OR \"Gene insertion\" OR 細胞療法 OR \"Cell therapy\" OR 免疫逃逸 OR \"Immune evasion\""
                },
                {
                    "label": "Modified natural killer (NK) cells",
                    "boolean": "改造自然殺手細胞 OR 嵌合抗原受體自然殺手細胞 OR 免疫療法 OR 癌症治療 OR 細胞毒性 OR 細胞因子 OR 採納性細胞轉移 OR 腫瘤微環境 OR 免疫調節 OR 同種異體 NK 細胞 OR NK 細胞擴增 OR 靶向療法 OR基因工程 NK 細胞 OR 免疫逃逸 OR 臨床試驗 OR 腫瘤溶解病毒、Modified NK cells OR CAR-NK cells OR Immune therapy OR Cancer treatment OR Cytotoxicity OR Cytokines OR Adoptive cell transfer OR Tumor microenvironment OR Immune modulation OR Allogeneic NK cells OR NK cell expansion OR Targeted therapy OR Genetically engineered NK cells OR Immune escape OR Clinical trials OR Oncolytic viruses"
                },
                {
                    "label": "Gene-edited T cells",
                    "boolean": "基因編輯 T 細胞 OR 嵌合抗原受體 T 細胞 OR 免疫療法 OR 癌症治療 OR 細胞療法 OR CRISPR 技術 OR T 細胞擴增 OR 自體 T 細胞 OR 同種異體細胞 OR 免疫逃逸 OR 免疫監視 OR 臨床試驗 OR 轉基因技術 OR T 細胞功能增強 OR 腫瘤微環境 OR 免疫調節 OR Gene-edited T cells OR CAR T cells OR Immune therapy OR Cancer treatment OR Cell therapy OR CRISPR technology OR T cell expansion OR Autologous T cells OR Allogeneic cells OR Immune escape OR Immune surveillance OR Clinical trials OR Gene modification OR T cell enhancement OR Tumor microenvironment OR Immune modulation"
                }
            ],
            "efficacies": [
                {
                    "label": "T cell Immunity",
                    "boolean": "T 細胞毒性 OR enhance T cell OR activate T cells OR expand T cells OR activate particular T cell subsets and expand particular T cell subsets OR 特異性 T 細胞反應 OR tumor-specific T cell OR T 細胞免疫 OR T 細胞活化 OR 細胞介導免疫 OR T 細胞功能 OR T 細胞增殖 OR 免疫監視 OR 免疫記憶 OR 免疫逃逸 OR T cell immunity OR T cell activation OR cell-mediated immunity OR T cell function OR T cell proliferation OR immune surveillance OR immune memory OR immune evasion"
                },
                {
                    "label": "CDC",
                    "boolean": "補體依賴性細胞毒性 OR 補體系統 OR 抗體介導的細胞毒性 OR 免疫複合物 OR 補體激活 OR 細胞溶解 OR 腫瘤細胞殺傷 OR 免疫反應 OR complementdependent cytotoxicity (CDC) OR complement system OR antibody-mediated cytotoxicity OR immune complexes OR complement activation OR cell lysis OR tumor cell killing OR immune response"
                },
                {
                    "label": "ADCC",
                    "boolean": "抗體依賴性細胞介導的細胞毒性 OR 增強 ADCC 效應物 OR enhancing ADCC effectors OR NK cells OR macrophages OR 巨噬細胞 OR 腫瘤巨噬細胞 OR tumor macrophages OR 抗體依賴性細胞毒性 OR ADCC OR 效應細胞 OR 細胞介導的免疫反應 OR 腫瘤細胞殺傷 OR 抗體效能 OR 免疫療法 OR 淋巴細胞 OR antibody-dependent cell-mediated cytotoxicity (ADCC) OR ADCC OR effector cells OR cell-mediated immune response OR tumor cell killing OR antibody efficacy OR immunotherapy OR lymphocytes"
                },
                {
                    "label": "Maturation of Antigen Presenting Cells",
                    "boolean": "抗原呈遞細胞成熟 OR 樹突細胞 OR 抗原呈遞 OR 免疫激活 OR 細胞成熟 OR 免疫反應 OR 免疫調節 OR 細胞因子 OR maturation of antigen presenting cells OR dendritic cells OR antigen presentation OR immune activation OR cell maturation OR immune response OR immune modulation OR cytokines"
                },
                {
                    "label": "Angiogenesis",
                    "boolean": "Inhibition of Angiogenesis OR 抑制血管新生 OR 血管生成 OR 腫瘤血管生成 OR 血管新生 OR 血管生成 因子 OR 內皮細胞 OR 微血管生成 OR 血流供應 OR 腫瘤微環境 OR angiogenesis OR tumor angiogenesis OR vascular sprouting OR angiogenic factors OR endothelial cells OR microvascular generation OR blood supply OR tumor microenvironment"
                }
            ]
        }
    }
}