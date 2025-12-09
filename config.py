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
    "智能客服技術": {
        "main_boolean": "((((((((人工智慧 OR AI OR \"ARTIFICIAL INTELLIGENCE\") OR (自然語言 OR NL OR \"NATURAL LANGUAGE\") OR ((機器學習 OR ML OR \"MACHINE LEARNING\" OR 深度學習 OR DL OR \"DEEP LEARNING\") OR (SVM OR \"Support Vector Machine\" OR \"Random Forest\" OR Adaboost OR \"Decision Tree\" OR \"Markov Decision Process\" OR \"KNN\" OR \"k-means\" OR \"Naive Bayes\" OR \"tf-idf\") OR (神經網路 OR \"Neural Network\" OR RNN OR \"Recurrent Neural Network\" OR LSTM OR \"Long Short-Term Memory\" OR GRU OR \"Gated Recurrent Unit\" OR \"Generative Adversarial Networks\" OR GAN OR \"Autoencoder\") OR (BERT OR \"Bidirectional Encoder Representations from Transformers\" OR ROBERT OR \"A Robustly Optimized BERT Pretraining Approach\" OR \"Self-Attention\" OR \"Multi-Head Attention\" OR XLNet OR ELECTRA OR ELMO OR T5) OR (GPT OR \"Generative Pre-trained Transformer\" OR LLaMA OR \"Large Language Model Meta AI\" OR LLM* OR \"Self-Attention\" OR \"Multi-Head Attention\" OR ChatGPT\")))) AND ((識別 OR IDENTIF* OR 分析 OR ANALY* OR 分類 OR Classif* OR CATEGOR* OR 標記 OR Label* OR 命名 OR Nameing OR NER OR 生成 OR Generat* OR 翻譯 OR Translat* OR 轉錄 OR Transcrip* OR 問答 OR Question* OR 回覆 OR 回應 OR 回答 OR REPLY OR RESPONSE OR ANSWER*) AND (文字 OR 文本 OR 情感 OR 情緒 OR text* OR emotion* OR senti*) OR ((語音 OR 聲音 OR 音頻 OR VOICE OR AUDIO) OR (圖像 OR 圖片 OR 影像 OR 照片 OR IMAGE* OR PHOTO* OR PICTURE*)))) AND (客服 OR 客戶服務 OR \"CUSTOMER SERVICE\" OR 客戶 OR 顧客 OR 用戶 OR 使用者 OR CUSTOMER OR USER) AND (對話 OR DIALOGUE OR 聊天 OR CHAT OR 助理 OR 助手 OR 客訴 OR 秘書 OR ASSIST* OR CONVERSATION*))) NOT (管理 OR 編輯 OR MANAGE* OR CONTROL* OR EDIT* OR 展示 OR DISPLA*))@TI,AB",
        "matrix": {
            "technologies": [
                {
                    "label": "機器學習 (Machine Learning)",
                    "boolean": "(SVM OR \"Support Vector Machine\" OR \"Random Forest\" OR Adaboost OR \"Decision Tree\" OR \"Markov Decision Process\" OR \"KNN\" OR \"k-means\" OR \"Naive Bayes\" OR \"tf-idf\")"
                },
                {
                    "label": "簡單深度學習 (Simple Deep Learning)",
                    "boolean": "(神經網路 OR \"Neural Network\" OR RNN OR \"Recurrent Neural Network\" OR LSTM OR \"Long Short-Term Memory\" OR GRU OR \"Gated Recurrent Unit\" OR \"Generative Adversarial Networks\" OR GAN OR \"Autoencoder\")"
                },
                {
                    "label": "基於編碼器架構的 Transformer (Encoder-based)",
                    "boolean": "(BERT OR \"Bidirectional Encoder Representations from Transformers\" OR ROBERTA OR \"A Robustly Optimized BERT Pretraining Approach\" OR \"Self-Attention\" OR \"Multi-Head Attention\" OR XLNet OR ELECTRA OR ELMO OR T5)"
                },
                {
                    "label": "基於解碼器架構的 Transformer (Decoder-based)",
                    "boolean": "(GPT OR \"Generative Pre-trained Transformer\" OR LLAMA OR \"Large Language Model Meta AI\" OR LLM* OR \"Self-Attention\" OR \"Multi-Head Attention\" OR ChatGPT)"
                }
            ],
            "efficacies": [
                {
                    "label": "分類 (Classification)",
                    "boolean": "(識別 OR IDENTIFY OR 分析 OR ANALYSIS OR 分類 OR Classification)"
                },
                {
                    "label": "辨識/標記 (Identification/NER)",
                    "boolean": "(標記 OR Labeling OR 命名 OR Named OR NER)"
                },
                {
                    "label": "回應 (Response)",
                    "boolean": "(生成 OR Generation OR 翻譯 OR Translation OR 轉錄 OR Transcription OR 問答 OR Question OR 回覆 OR 回應 OR 回答 OR REPLY OR RESPONSE* OR ANSWER)"
                },
                {
                    "label": "語音 (Voice)",
                    "boolean": "(語音 OR 聲音 OR 音頻 OR VOICE OR AUDIO)"
                },
                {
                    "label": "圖像 (Image)",
                    "boolean": "(圖像 OR 圖片 OR 影像 OR 照片 OR IMAGE* OR PHOTO* OR PICTURE*)"
                }
            ]
        }
    },
    "台灣大哥大智能客服-語音辨識技術": {
        "main_boolean": "((深[1,4]神經網路 OR 深[1,4]神經网络 OR 深度學習 OR 強化學習 OR 機器學習 OR deep [1,13] neural network OR ((reinforcement OR deep OR machine) AND learning) OR ((深層 OR ディープ OR リカレント) AND (ニューラルネットワーク OR 神経ネットワーク)) OR 強化学習 OR 深層学習 OR ディープラーニング OR マシンラーニング OR 機械学習 OR (딥 AND (뉴럴네트워크 OR 신경망 OR 강화학습)) OR 강화러닝 OR ((심층 OR 기계) AND 학습) OR 자율조정 OR 추론알고리즘 OR ((심층 OR 심층학습) AND 신경망)) OR (語音[1,3]檢測 OR 聲音[1,3]檢測 OR 語音[1,3]偵測 OR 聲音[1,3]偵測 OR ((音動 OR 音態) AND (偵測 OR 檢測)) OR ((Voice OR speech) AND activity detection) OR VAD OR 音声[1,3]検出 OR 音動検出 OR 発話区間検出 OR 音声エンドポイント OR ((음성 OR 음향 OR 연설) AND (활동 OR 상태) AND (식별하는 OR 검출 OR 발각 OR 감지))))",
        "matrix": {
            "technologies": [
                {
                    "label": "深度神經網絡 (Deep Neural Networks, DNN)",
                    "boolean": "(深[1,4]神經網路 OR 深[1,4]神經网络 OR 深度學習 OR 強化學習 OR 機器學習 OR deep [1,13] neural network OR ((reinforcement OR deep OR machine) AND learning) OR ((深層 OR ディープ OR リカレント) AND (ニューラルネットワーク OR 神経ネットワーク)) OR 強化学習 OR 深層学習 OR ディープラーニング OR マシンラーニング OR 機械学習 OR (딥 AND (뉴럴네트워크 OR 신경망 OR 강화학습)) OR 강화러닝 OR ((심층 OR 기계) AND 학습) OR 자율조정 OR 추론알고리즘 OR ((심층 OR 심층학습) AND 신경망))"
                },
                {
                    "label": "語音活動檢測 (Voice Activity Detection, VAD)",
                    "boolean": "(語音[1,3]檢測 OR 聲音[1,3]檢測 OR 語音[1,3]偵測 OR 聲音[1,3]偵測 OR ((音動 OR 音態) AND (偵測 OR 檢測)) OR ((Voice OR speech) AND activity detection) OR VAD OR 音声[1,3]検出 OR 音動検出 OR 発話区間検出 OR 音声エンドポイント OR ((음성 OR 음향 OR 연설) AND (활동 OR 상태) AND (식별하는 OR 검출 OR 발각 OR 감지)))"
                },
                {
                    "label": "語音合成 (Speech Synthesis)",
                    "boolean": "((語音 OR 音訊 OR 音声 OR 音頻) AND (產生 OR 合成 OR 生成)) OR (speech AND synthe*) OR スピーチシンセサイザー OR (음성 AND (생성 OR 합성 OR 합성))"
                },
                {
                    "label": "情感計算 (Affective Computing)",
                    "boolean": "((情感 OR 情緒 OR 感情 OR エモーション) AND (計算 OR 識別 OR 分析 OR コンピューティング OR 認識)) OR ((affective OR emotion) AND (computing OR recognition)) OR (감정 AND (계산 OR 인식 OR 내용분석))"
                },
                {
                    "label": "語音分離 (Speech Separation)",
                    "boolean": "((語音 OR 聲音 OR 音声 OR ボイス) AND (分離 OR 隔離 OR 分割)) OR ((voice OR speech) AND separat*) OR 음성분리"
                },
                {
                    "label": "語者分割 (Speaker Diarization)",
                    "boolean": "((語者 OR 說話人 OR 話者) AND (分割 OR 分離 OR 切割 OR 識別 OR 分段 OR セグメンテーション OR ラベリング OR ダイアライゼーション)) OR (speaker AND (Diarization OR segmentation OR separation OR Identification OR recognition)) OR (화자 AND (분할 OR 분리 OR 인식))"
                },
                {
                    "label": "語音轉換 (Voice Conversion)",
                    "boolean": "((聲音 OR 語音) AND 轉換) OR ((Voice OR speech OR audio) AND (Transform* OR convers* OR transmit*)) OR ((音声 OR ボイス) AND 変換) OR 음성변환"
                },
                {
                    "label": "端對端學習 (End-to-End Learning)",
                    "boolean": "((端對端 OR 端到端) AND 學習) OR (End-to-End AND Learning) OR エンドツーエンド学習 OR ((엔드투엔드 OR 종단간) AND 학습)"
                },
                {
                    "label": "自動語音辨識 (Automatic Speech Recognition)",
                    "boolean": "(自動語音 AND (辨識 OR 识别)) OR ((Speech OR voice) AND Recognition) OR (自動 AND 音声認識) OR (자동 AND 음성인식)"
                },
                {
                    "label": "文字轉語音+自然語言處理 (TTS + NLP)",
                    "boolean": "文字[2,3]語音 OR 文句[2,3]語音 OR TTS OR Text to Speech OR 自然語言處理 OR \"Natural Language Processing\" OR NLP OR 文[1,2]音声変換 OR テキストトゥスピーチ OR 音声読み上げ OR 自然言語処理 OR 문자[1,2]음성변환 OR 텍스트음성변환 OR 자연 [1,2]어처리"
                }
            ],
            "efficacies": [
                {
                    "label": "迴聲消除 (Echo Cancellation)",
                    "boolean": "((回聲 OR 回波 OR 回音 OR 迴音 OR 迴聲 OR 迴波) AND (消除 OR 去除)) OR Echo Cancel* OR ((エコー OR 反響) AND (除去 OR 消去 OR キャンセル)) OR 에코제거"
                },
                {
                    "label": "噪聲抑制 (Noise Reduction)",
                    "boolean": "((噪聲 OR 噪音 OR 雜訊) AND (抑制 OR 限制 OR 降低)) OR 去噪 OR 降噪 OR 減噪 OR (Noise AND (Reduc* OR Suppress*)) OR (ノイズ AND (抑制 OR 制限 OR 除去 OR 低減 OR リダクション)) OR ((잡음 OR 노이즈 OR 소음) AND (제거 OR 감소 OR 리덕션 OR 억제 OR 제한 OR 저감))"
                },
                {
                    "label": "公平性 (Fairness)",
                    "boolean": "公平性 OR 公平 OR Fairness OR 공평"
                },
                {
                    "label": "實時處理 (Real-time Processing)",
                    "boolean": "((實時 OR 即時) AND 處理) OR Real-time Processing OR ((リアルタイム OR 即時) AND 処理) OR ((실시간 OR 즉각적인) AND 처리)"
                },
                {
                    "label": "隱私保護 (Privacy Protection)",
                    "boolean": "((隱私 OR プライバシー) AND 保護) OR Privacy Protect* OR ((프라이버시 OR 개인정보 OR 사생활) AND 보호)"
                },
                {
                    "label": "能效優化 (Energy Efficiency)",
                    "boolean": "((能效 OR 能源效率) AND 優化) OR Energy Efficiency OR エネルギー効率 OR 에너지 효율성"
                },
                {
                    "label": "用戶體驗 (User Experience)",
                    "boolean": "((用戶 OR 使用者 OR 顧客 OR 个性化) AND (體驗 OR 經驗)) OR ((User OR Personalized) AND Experience) OR UX OR ((ユーザー OR 顧客 OR パーソナライズ) AND (体験 OR 経験 OR エクスペリエンス)) OR ((사용자 OR 고객 OR 개인화된) AND (경험 OR 체험))"
                },
                {
                    "label": "可擴展性、泛用性 (Scalability)",
                    "boolean": "可擴展性 OR 可伸縮性 OR 泛用性 OR 可擴縮性 OR 可規模性 OR 可擴充性 OR Scalability OR 拡張性 OR スケーラビリティ OR 汎用性 OR 拡縮性 OR 拡充性 OR (확장 AND (성 OR 축소가능성 OR 가능성)) OR 스케일러빌리티"
                },
                {
                    "label": "數據安全 (Data Security)",
                    "boolean": "((數據 OR 資料) AND (安全 OR 保密)) OR (Data AND (Security OR Safety)) OR (データ AND (セキュリティ OR 機密保持 OR 安全)) OR (데이터 AND 보안)"
                },
                {
                    "label": "語音增強 (Speech Enhancement)",
                    "boolean": "(語音 AND (增強 OR 強化)) OR ((Speech OR voice) AND enhancement) OR (音声 AND (強調 OR 強化)) OR スピーチエンハンスメント OR (음성 AND (강화 OR 향상))"
                }
            ]
        }
    },
    "矽光子技術 (Silicon Photonics)": {
        "main_boolean": "(IC=G02B* OR IC=H02B* OR IC=H01S* OR IC=H01L* OR IC=H04J* OR IC=H04B*) AND (modulator or Modulation Device or Modulation Unit or Transducer or Electro-Optic Converter or Optoelectronic Conversion Module or 調制器 or 調變器 or 調制單元 or 調變單元 or 變調器 or 電光變換器 or 調相器 or 光電轉換模塊 or 変調器 or 変調デバイス)@TI,CL,AB AND (silicon photonic* OR Si photonic* OR Integrated Optics OR OPTICAL Integrated CIRCUIT* OR Photonic* Integrated Circuit* OR Co-Packaged Optic* OR photonic integration OR 矽光子 OR 矽光學 OR 光子積體電路 OR 光子集成電路 OR 共同封裝光學 OR 積體光學 OR シーフォトニクス OR 集積光学 OR フォトニック回路 OR フォトニック集積回路 OR 共封止光学)@TI,CL,AB NOT (電漿 OR 清潔 OR 浸潤 OR Plasma OR Cleaning OR Immersion)@TI,CL,AB NOT (IC=G03F* OR IC=G09F* OR IC=G01S*)",
        "matrix": {
            "technologies": [
                {
                    "label": "波導與傳輸技術 (Waveguide & Transmission)",
                    "boolean": "(光波導 OR Waveguide OR G02B 6/12 OR Optical waveguide OR 傳輸 OR Transmission)@TI,AB,CL"
                },
                {
                    "label": "調制與檢測技術 (Modulation & Detection)",
                    "boolean": "(調變器 OR Modulator OR 光檢測器 OR Photodetector OR G02F OR 調制 OR Detection)@TI,AB,CL"
                },
                {
                    "label": "光源技術 (Light Source)",
                    "boolean": "(光源 OR Light Source OR 雷射 OR Laser OR H01S OR DFB OR 分佈式回饋雷射)@TI,AB,CL"
                },
                {
                    "label": "光開關與光耦合技術 (Optical Switch & Coupling)",
                    "boolean": "(光開關 OR Optical Switch OR 光耦合 OR Optical Coupling OR 光柵耦合器 OR Grating Coupler OR 端面耦合器 OR Edge Coupler)@TI,AB,CL"
                },
                {
                    "label": "封裝與散熱技術 (Packaging & Thermal Management)",
                    "boolean": "(封裝 OR Packaging OR CPO OR Co-Packaged Optics OR 散熱 OR Thermal OR Heat dissipation OR 覆晶 OR Flip-chip)@TI,AB,CL"
                },
                {
                    "label": "測試與檢測技術 (Test & Measurement)",
                    "boolean": "(測試 OR Test OR 檢測 OR Measurement OR Testing OR Monitoring)@TI,AB,CL"
                }
            ],
            "efficacies": [
                {
                    "label": "傳輸效率 (Transmission Efficiency)",
                    "boolean": "(效率 OR Efficiency OR 損耗 OR Loss OR 傳輸率 OR Transmission rate OR 高效 OR High efficiency)@TI,AB,CL"
                },
                {
                    "label": "調製速度與頻寬 (Modulation Speed & Bandwidth)",
                    "boolean": "(速度 OR Speed OR 頻寬 OR Bandwidth OR 速率 OR Rate OR Gbps OR Tbps)@TI,AB,CL"
                },
                {
                    "label": "光源穩定性 (Stability)",
                    "boolean": "(穩定性 OR Stability OR 可靠性 OR Reliability OR 壽命 OR Lifetime)@TI,AB,CL"
                },
                {
                    "label": "功率消耗 (Power Consumption)",
                    "boolean": "(功耗 OR Power consumption OR 能耗 OR Energy consumption OR 低功耗 OR Low power)@TI,AB,CL"
                },
                {
                    "label": "集成度 (Integration)",
                    "boolean": "(集成度 OR Integration OR 整合 OR Integrated OR 尺寸 OR Size OR 微型化 OR Miniaturization OR 緊湊 OR Compact)@TI,AB,CL"
                },
                {
                    "label": "成本效益 (Cost Effectiveness)",
                    "boolean": "(成本 OR Cost OR 經濟 OR Economic OR 效益 OR Benefit OR 量產 OR Mass production OR 良率 OR Yield)@TI,AB,CL"
                }
            ]
        }
    },
    "口服巴金森氏症藥物 (Oral Parkinson's Disease Drugs)": {
        "main_boolean": "((((Tab* OR oral* OR 口服* OR *경구 OR *オーラル OR *藥片 OR *ビル OR *알약 OR *藥錠 OR *錠剤 OR *정제 OR pill NOT (Table)))@AB@TI@CL OR (\"4-ethylphenol Sulfate\" OR 4EPS OR \"gut-brain axis\" OR GUT OR 腸 OR 장의 OR psychobiotic OR \"Enteric Nervous System\" OR ENS OR probiotic* OR Prebiotic* OR Synbiotics OR microorganism* OR bacteria* OR yeast* OR Lactobacillus* OR Bifidobacterium* OR Enterococcus* OR amyloid*)@AB@TI@CL) AND ((Parkinson* OR 帕金森* OR 巴金森* OR パーキンソン* OR 파킨슨병*) AND (IC=A23L* OR IC=A61K* OR IC=A61P* OR IC=C07C* OR IC=C07D* OR IC=C07F* OR IC=C07K*)))",
        "matrix": {
            "technologies": [
                {
                    "label": "口服給藥與劑型 (Oral Delivery & Dosage Forms)",
                    "boolean": "(Tab* OR oral* OR 口服* OR *경구 OR *オーラル OR *藥片 OR *ピル OR *알약 OR *藥錠 OR *錠剤 OR *정제 OR pill) NOT (Table)"
                },
                {
                    "label": "腸腦軸與微生物機制 (Gut-Brain Axis & Microbiome)",
                    "boolean": "(\"4-ethylphenol Sulfate\" OR 4EPS OR \"gut-brain axis\" OR GUT OR 腸 OR 장의 OR psychobiotic OR \"Enteric Nervous System\" OR ENS OR probiotic* OR Prebiotic* OR Synbiotics OR microorganism* OR bacteria* OR yeast* OR Lactobacillus* OR Bifidobacterium* OR Enterococcus* OR amyloid*)"
                },
                {
                    "label": "主要IPC分類號 (Main IPC Classifications)",
                    "boolean": "(IC=A23L* OR IC=A61K* OR IC=A61P* OR IC=C07C* OR IC=C07D* OR IC=C07F* OR IC=C07K*)"
                }
            ],
            "efficacies": [
                {
                    "label": "適應症：巴金森氏症 (Target Disease: Parkinson's)",
                    "boolean": "(Parkinson* OR 帕金森* OR 巴金森* OR パーキンソン* OR 파킨슨병*)"
                },
                {
                    "label": "相關病理特徵 (Pathological Features - *from search history*)",
                    "boolean": "(synucleinopathies OR \"Alpha-synuclein\" OR \"a-syn\" OR GBA OR LKKR2 OR \"Levodopa Delivery\" OR \"Gene Therapy\" OR Dyskinesia OR Anxiety OR Constipation)"
                }
            ]
        }
    },
    "聚乳酸技術 (Polylactic Acid, PLA)": {
        "main_boolean": "((聚乳酸 OR \"Polylactic acid\" OR PLA OR Polylactide OR \"Poly(lactic acid)\" OR \"Poly-lactic acid\")@TI,AB,CL) AND (IC=C08G 63/* OR IC=C08L 67/* OR IC=C08J 5/*) AND ((合成 OR Synthesis OR Polymerization) OR (改質 OR Modification) OR (觸媒 OR Catalyst) OR (純化 OR Purification) OR (立體複合 OR Stereocomplex))@TI,AB,CL NOT (醫療 OR Medical OR Drug OR Scaffold OR Tissue engineering)@TI",
        "matrix": {
            "technologies": [
                {
                    "label": "合成技術 (Synthesis Technology)",
                    "boolean": "(合成 OR Synthesis OR Polymerization OR \"Ring-opening polymerization\" OR ROP OR \"Direct polycondensation\" OR 開環聚合 OR 直接縮合)@TI,AB,CL"
                },
                {
                    "label": "觸媒技術 (Catalyst Technology)",
                    "boolean": "(觸媒 OR Catalyst OR Initiator OR \"Metal catalyst\" OR \"Organocatalyst\" OR 錫 OR Tin OR 辛酸亞錫 OR \"Stannous octoate\")@TI,AB,CL"
                },
                {
                    "label": "純化技術 (Purification Technology)",
                    "boolean": "(純化 OR Purification OR Refining OR Removal OR Distillation OR Crystallization OR 結晶 OR 蒸餾 OR 去除)@TI,AB,CL"
                },
                {
                    "label": "改質技術 (Modification Technology)",
                    "boolean": "(改質 OR Modification OR Toughening OR Blending OR Copolymerization OR Plasticizer OR 增韌 OR 摻混 OR 共聚 OR 塑化劑)@TI,AB,CL"
                },
                {
                    "label": "立體複合技術 (Stereocomplex Technology)",
                    "boolean": "(立體複合 OR Stereocomplex OR SC-PLA OR \"Stereocomplex polylactide\" OR \"Stereo-complex\")@TI,AB,CL"
                }
            ],
            "efficacies": [
                {
                    "label": "耐熱性 (Heat Resistance)",
                    "boolean": "(耐熱 OR \"Heat resistance\" OR \"Thermal stability\" OR \"Melting point\" OR Tm OR 熱穩定性 OR 熔點)@TI,AB,CL"
                },
                {
                    "label": "機械性質 (Mechanical Properties)",
                    "boolean": "(機械性質 OR \"Mechanical properties\" OR Strength OR Toughness OR Tensile OR Modulus OR 強度 OR 韌性 OR 拉伸 OR 模數)@TI,AB,CL"
                },
                {
                    "label": "光學性質/透明度 (Optical Properties/Transparency)",
                    "boolean": "(光學 OR Optical OR Transparency OR Haze OR Clarity OR 透明度 OR 霧度)@TI,AB,CL"
                },
                {
                    "label": "阻氣性 (Gas Barrier)",
                    "boolean": "(阻氣 OR \"Gas barrier\" OR Permeability OR Oxygen OR Water vapor OR 阻隔 OR 滲透 OR 氧氣 OR 水氣)@TI,AB,CL"
                },
                {
                    "label": "分子量控制 (Molecular Weight Control)",
                    "boolean": "(分子量 OR \"Molecular weight\" OR Mw OR Mn OR PDI OR Polydispersity OR 分佈)@TI,AB,CL"
                },
                {
                    "label": "結晶性 (Crystallinity)",
                    "boolean": "(結晶 OR Crystallinity OR Crystallization OR Nucleating agent OR 核劑 OR 結晶速率)@TI,AB,CL"
                }
            ]
        }
    },
    "Immunocytokine 產業": {
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
    },
  "智慧穿戴式醫療監測系統": {
    "main_boolean": "((wearable OR ((wear OR wearing OR worn) W/3 (device OR apparatus OR instrument OR equipment OR system)) OR \"head mounted\" OR smart W/3 (watch OR ring OR glasses OR clothing OR garment)) AND ((monitor* OR detect* OR sens* OR measur*) W/5 (health OR medical OR physiological OR physical OR biological OR \"vital sign\" OR \"heart rate\" OR \"blood pressure\" OR \"blood oxygen\" OR temperature OR respiration OR sleep OR activity OR step OR calorie OR ecg OR ekg OR eeg OR emg OR spo2 OR glucose OR sugar))) AND (IPC=A61B5* OR IPC=G16H*)",
    "matrix": {
      "technologies": [
            {
            "label": "感測模組 (Sensing Module)",
            "boolean": "(sensor OR detector OR electrode OR probe OR transducer OR accelerometer OR gyroscope OR magnetometer OR ppg OR ecg OR eeg OR emg)@AB,CL"
            },
            {
            "label": "處理模組 (Processing Module)",
            "boolean": "(processor OR controller OR cpu OR mcu OR microprocessor OR microcontroller OR chip OR ic OR circuit OR algorithm OR \"artificial intelligence\" OR \"machine learning\")@AB,CL"
            },
            {
            "label": "傳輸模組 (Transmission Module)",
            "boolean": "(wireless OR bluetooth OR ble OR wifi OR zigbee OR nfc OR rf OR antenna OR transceiver OR transmitter OR receiver OR 5g)@AB,CL"
            },
            {
            "label": "電源模組 (Power Module)",
            "boolean": "(battery OR cell OR power OR energy OR charge OR recharge OR harvest OR supercapacitor OR voltage OR current)@AB,CL"
            },
            {
            "label": "顯示/回饋模組 (Display/Feedback Module)",
            "boolean": "(display OR screen OR led OR lcd OR oled OR touch OR haptic OR vibration OR audio OR speaker OR alarm OR alert OR interface)@AB,CL"
            }
        ],
      "efficacies": [
            {
            "label": "準確性 (Accuracy)",
            "boolean": "(accuracy OR precision OR reliability OR stability OR sensitivity OR \"signal-to-noise\" OR error)@AB,CL"
            },
            {
            "label": "舒適性/配戴性 (Comfort/Wearability)",
            "boolean": "(comfort OR fit OR flexible OR stretchable OR soft OR lightweight OR thin OR \"skin-friendly\")@AB,CL"
            },
            {
            "label": "即時性 (Real-time)",
            "boolean": "(\"real-time\" OR instant OR delay OR latency OR speed OR fast)@AB,CL"
            },
            {
            "label": "低功耗/續航 (Low Power/Endurance)",
            "boolean": "(\"low power\" OR \"power consumption\" OR \"energy saving\" OR \"battery life\" OR efficiency OR endurance)@AB,CL"
            },
            {
            "label": "小型化/便攜 (Miniaturization/Portability)",
            "boolean": "(small OR mini OR micro OR compact OR portable OR size OR dimension OR weight)@AB,CL"
            }
        ]
    }
  }
}