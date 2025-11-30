from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

class ReportGenrator:
    def __init__(self, theme = "", search_result = [0, 0], query = "", students_data = [], source = ["", ""], matrix_json = []):        
        # 初始化所有需要的欄位
        self.report_title = "智慧財產權實戰策略期末報告"
        self.theme = theme
        self.search_result = search_result
        self.query = query
        self.students_data = students_data
        self.source = source
        self.matrix_json = matrix_json

    def set(self, theme = None, search_result = None, query = None, students_data = None, source = None, matrix_json = None):
        if theme:
            self.theme = theme
        if search_result:
            self.search_result = search_result
        if query:
            self.query = query
        if students_data:
            self.students_data = students_data
        if source:
            self.source = source
        if matrix_json:
            self.matrix_json = matrix_json


    def gen_report(self):

        def set_chinese_font(run, size=12, bold=False):
            """設定中文字型的 Helper Function"""
            run.font.name = 'Times New Roman' # 西文部分
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體') # 中文部分 (可改微軟正黑體)
            run.font.size = Pt(size)
            run.bold = bold
        
        doc = Document()
        title = doc.add_heading(level=0)
        run = title.add_run('智慧財產權實戰策略期末報告')
        set_chinese_font(run, size=20, bold=True)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # --- 2. 成員名單表格 ---
        # 成員表格
        doc.add_heading('成員名單', level=1)
        table = doc.add_table(rows=4, cols=4)
        table.style = 'Table Grid'
        
        # 表頭
        headers = ['姓名', '學號', '姓名', '學號']
        for i, text in enumerate(headers):
            cell = table.cell(0, i)
            run = cell.paragraphs[0].add_run(text)
            set_chinese_font(run, bold=True)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 填充範例資料 (根據 source: 3 的格式)
        for i, row_data in enumerate(self.students_data):
            for j, text in enumerate(row_data):
                run = table.cell(i+1, j).paragraphs[0].add_run(text)
                set_chinese_font(run)

        doc.add_page_break()

        # --- 3. 檢索流程 ---
        # 
        h1 = doc.add_heading(level=1)
        set_chinese_font(h1.add_run('檢索流程'), size=16, bold=True)

        # 選定主題
        p = doc.add_paragraph()
        set_chinese_font(p.add_run('選定主題：'), bold=True)
        set_chinese_font(p.add_run(f"本研究針對{"<主題>"}專利分析與布局進行專利檢索分析。"))

        # 檢索條件
        p = doc.add_paragraph()
        set_chinese_font(p.add_run('訂出主題關鍵字：'), bold=True)
        if self.source:
            set_chinese_font(p.add_run(f"參考{self.source[0]}，設定以下檢索條件。"))
        else:
            set_chinese_font(p.add_run("設定以下檢索條件。"))
        
        query_para = doc.add_paragraph(self.query)
        query_para.runs[0].font.size = Pt(9)
        query_para.runs[0].font.color.rgb = RGBColor(50, 50, 150)

        items = [
            "專利資料庫：全球專利檢索系統GPSS。", 
            f"五、主題相關專利：本次專利檢索共獲得 {self.search_result[0]} 筆 專利資料，經過檢索結果去重與專利家族去重處理後，最終共有 {self.search_result[1]} 筆專利資料納入分析。", 
            f"六、IPC或CPC國際分類號採用：參考{self.source[1]}，將專利檢索式之國際專利分類號設定在{"<檢索範圍>"}。",
            "七、抽樣檢索：除了關鍵詞與國際分類號，檢索條件仍採取and or not等控制條件。"
        ]
        for item in items:
            p = doc.add_paragraph()
            set_chinese_font(p.add_run(item))

        charts = [
            ("專利管理圖分析 - 技術領域分類", "技術領域分類分析（業界用語）"),
            ("領導者分析", "誰是這個領域的領導者（業界用語）"),
            ("布局戰場", "那些國家是布局戰場（業界用語）"),
            ("專利申請趨勢", "專利申請趨勢（業界用語）")
        ]
        
        for title_text, desc in charts:
            doc.add_heading(title_text, level=2)
            doc.add_paragraph(f"[{desc} - 請在此處插入圖片]")
            # 如果您有圖片檔案，可以使用: doc.add_picture('path_to_image.png', width=Inches(6))

        doc.add_page_break()

        # --- 5. 技術與功效分類表 ---
        # 技術分類表格
        doc.add_heading('專利技術圖分析 - 技術分類', level=2)
        
        tech_data = self.matrix_json["technologies"]
        
        table = doc.add_table(rows=len(tech_data) + 1, cols=2)
        table.style = 'Table Grid'
        cell = table.cell(0, 0)
        run = cell.paragraphs[0].add_run("技術分類")
        set_chinese_font(run, size=10, bold=True)
        cell = table.cell(0, 1)
        run = cell.paragraphs[0].add_run("技術分類檢索詞")
        set_chinese_font(run, size=10, bold=True)    

        for i, tech in enumerate(tech_data):
            cell = table.cell(i + 1, 0)
            run = cell.paragraphs[0].add_run(tech["label"])
            set_chinese_font(run, size=10, bold=False)
            cell = table.cell(i + 1, 1)
            run = cell.paragraphs[0].add_run(tech["boolean"])
            set_chinese_font(run, size=10, bold=False)

        # 功效分類表格
        doc.add_heading('功效分類', level=2)
        
        eff_data = self.matrix_json["efficacies"]
        
        table = doc.add_table(rows=len(eff_data) + 1, cols=2)
        table.style = 'Table Grid'
        cell = table.cell(0, 0)
        run = cell.paragraphs[0].add_run("功效分類")
        set_chinese_font(run, size=10, bold=True)
        cell = table.cell(0, 1)
        run = cell.paragraphs[0].add_run("功效分類檢索詞")
        set_chinese_font(run, size=10, bold=True) 
        for i, eff in enumerate(eff_data):
            cell = table.cell(i + 1, 0)
            run = cell.paragraphs[0].add_run(eff["label"])
            set_chinese_font(run, size=10, bold=False)
            cell = table.cell(i + 1, 1)
            run = cell.paragraphs[0].add_run(eff["boolean"])
            set_chinese_font(run, size=10, bold=False)

        # --- 6. 技術功效矩陣分析 ---
        # 
        doc.add_heading('三、技術功效矩陣分析', level=1)
        doc.add_paragraph("[請在此處插入技術功效矩陣氣泡圖]")
        
        # 儲存
        doc.save('.data/期末報告.docx')


'''
def create_report():
    doc = Document()
    title = doc.add_heading(level=0)
    run = title.add_run('智慧財產權實戰策略期末報告')
    set_chinese_font(run, size=20, bold=True)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- 2. 成員名單表格 ---
    # 成員表格
    doc.add_heading('成員名單', level=1)
    table = doc.add_table(rows=4, cols=4)
    table.style = 'Table Grid'
    
    # 表頭
    headers = ['姓名', '學號', '姓名', '學號']
    for i, text in enumerate(headers):
        cell = table.cell(0, i)
        run = cell.paragraphs[0].add_run(text)
        set_chinese_font(run, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 填充範例資料 (根據 source: 3 的格式)
    data = [
        ['組長姓名', '請依照實際情況撰寫', '組長姓名', '請依照實際情況撰寫'],
        ['組員姓名', '請依照實際情況撰寫', '組員姓名', '請依照實際情況撰寫'],
        ['組員姓名', '請依照實際情況撰寫', '組員姓名', '請依照實際情況撰寫']
    ]
    for i, row_data in enumerate(data):
        for j, text in enumerate(row_data):
            run = table.cell(i+1, j).paragraphs[0].add_run(text)
            set_chinese_font(run)

    doc.add_page_break()

    # --- 3. 檢索流程 ---
    # 
    h1 = doc.add_heading(level=1)
    set_chinese_font(h1.add_run('檢索流程'), size=16, bold=True)

    # 選定主題
    p = doc.add_paragraph()
    set_chinese_font(p.add_run('選定主題：'), bold=True)
    set_chinese_font(p.add_run('本研究針對智慧座艙AR-HUD專利分析與布局進行專利檢索分析。'))

    # 檢索條件
    p = doc.add_paragraph()
    set_chinese_font(p.add_run('訂出主題關鍵字：'), bold=True)
    set_chinese_font(p.add_run('參考網路資源「駛入新視界：智慧座艙AR-HUD專利分析與布局」p60-62設定以下檢索條件。'))

    # 巨大的檢索字串
    # 這裡將多段文字合併
    search_query = (
        "(((HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイOR  헤드   업   디스플레이 )@TI,AB,CL,DE AND"
        "(head)@TI,AB,CL AND (UP)@TI,AB,CL AND (DISPLAY OR DISPLAYS)@TI,AB,CL) OR "
        "((AR OR Augmented Reality OR擴增實境 OR 扩增现实 OR 拡張現実 OR  증강현실 OR HOE OR Hologram OR Holography OR Holographic OR 全息投影 OR 全息 OR ホログラフィック OR 홀로그래피 OR Waveguide OR 光波導 OR光波导 ORウェーブガイド OR  도파관 OR 3D OR Three Dimentional OR Multi-Depth OR 三維 OR 三维 OR 三元 OR  입체적인  OR Pupil expander OR Pupil expansion OR Eye OR Eyebox OR Steerable Eyebox OR Eye Tracking OR Eye Tracker OR Naked Eye OR 瞳孔 OR 虹膜 OR 眼 OR 目 OR  눈 )@TI AND "
        "(HUD OR 抬頭顯示器 OR 平視顯示器 OR ヘッドアップディスプレイOR  헤드   업디스플레이 )@TI,AB,CL,DE) NOT "
        "(Wearable OR Portable OR HeadMounted OR Helmet OR Glasses OR Aircraft OR Flight OR Plane OR Medical OR Mask OR Surgery OR Game OR VR OR 穿戴式 OR 便攜的 OR 頭戴式 OR 頭盔 OR 眼鏡 OR 飛機 OR 航班 OR飛機 OR 醫療的 OR 口罩 OR手術 OR 遊戲 OR 虛擬實境 OR 可穿戴 OR 便携式 OR 头戴式 OR 头盔 OR 眼镜 OR 飞机 OR 飞行 OR医疗 OR 口罩 OR 外科手术 OR 游戏 OR 虚拟现实 OR ウェアラブル OR ポータブル OR ヘッドマウント ORヘルメット OR メガネ OR 航空機 OR フライト OR 飛行機 OR 医療 OR マスク OR 外科 OR ゲーム OR 仮想現実 OR  착용형  OR  휴대용  OR  헤드   마운트형  OR  헬멧형  OR  안경형  OR  항공기  OR  비행  OR  비행기  OR  의료  OR  마스크  OR  외과  OR  게임  OR  가상현실  )@TI) "
        "AND ID=:20231231 AND (IC=G02B* OR IC=B60J* OR IC=B60K* OR IC=B60R*)"
    )
    
    query_para = doc.add_paragraph(search_query)
    query_para.runs[0].font.size = Pt(9) # 字體縮小一點以免佔版面
    query_para.runs[0].font.color.rgb = RGBColor(50, 50, 150) # 設定為深藍色區別

    # 資料庫與統計
    items = [
        "專利資料庫：全球專利檢索系統GPSS。",
        "五、主題相關專利：本次專利檢索共獲得 14,240 筆 專利資料，經過檢索結果去重與專利家族去重處理後，最終共有7,914 筆專利資料納入分析。",
        "六、IPC或CPC國際分類號採用：參考HUD與AR-HUD之相關應用與光學原理，將專利檢索式之國際專利分類號設定在G02B* OR B60J* OR B60K* OR B60R*。",
        "七、抽樣檢索：除了關鍵詞與國際分類號，檢索條件仍採取and or not等控制條件。"
    ]
    for item in items:
        p = doc.add_paragraph()
        set_chinese_font(p.add_run(item))

    # --- 4. 圖表分析 (預留位置) ---
    # 
    charts = [
        ("專利管理圖分析 - 技術領域分類", "技術領域分類分析（業界用語）"),
        ("領導者分析", "誰是這個領域的領導者（業界用語）"),
        ("布局戰場", "那些國家是布局戰場（業界用語）"),
        ("專利申請趨勢", "專利申請趨勢（業界用語）")
    ]
    
    for title_text, desc in charts:
        doc.add_heading(title_text, level=2)
        doc.add_paragraph(f"[{desc} - 請在此處插入圖片]")
        # 如果您有圖片檔案，可以使用: doc.add_picture('path_to_image.png', width=Inches(6))

    doc.add_page_break()

    # --- 5. 技術與功效分類表 ---
    # 技術分類表格
    doc.add_heading('專利技術圖分析 - 技術分類', level=2)
    
    tech_data = [
        ["技術分類", "技術分類檢索詞"],
        ["PGU(圖像生成器)", '"(PGU OR "Picture Generation Unit" OR "TFT-LCD" OR "Thin Film Transistor Liquid Crystal Display" OR LCOS OR "Liquid Crystal On Silicon" OR DLP OR "Digital Light Processing" OR MEMS OR "Micro Electro Mechanical System" OR "Laser Beam" OR "microLED" OR SLM OR "Spatial Light Modulator")@TI,AB,CL,DE"'],
        ["Combiner(全息光學元件的組合器)", '"(Waveguide OR Holography OR Holographic OR Hologram OR HOE OR "Holographic Optical Elements")@TI,AB,CL,DE"'],
        ["Reflector(反射)", '"(Reflector OR Reflection OR "beam splitter")@TI,AB,CL,DE"'],
        ["Windshield(擋風玻璃及折射零件技術)", '"(windshield OR windscreen OR "Laminated Glass" OR "Wedge shaped" OR pvb OR 檔風玻璃 OR 楔形膜 OR 夾層玻璃)@TI,AB,CL,DE"'],
        ["Eye(駕駛視覺監控)", '"("Pupil expander" OR "Pupil expansion" OR Eye OR Eyebox OR "Eye Tracking" OR "Eye Tracker" OR "Naked Eye")@TI,AB,CL,DE"'],
        ["Diffuser(擴散)", '"(擴散器 OR 擴散片 OR Diffuser)@TI,AB,CL,DE"']
    ]
    
    table = doc.add_table(rows=len(tech_data), cols=2)
    table.style = 'Table Grid'
    for i, row in enumerate(tech_data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            run = cell.paragraphs[0].add_run(val)
            # 表頭加粗
            set_chinese_font(run, size=10, bold=(i==0))

    # 功效分類表格
    doc.add_heading('功效分類', level=2)
    
    effect_data = [
        ["功效分類", "功效分類檢索詞"],
        ["提升可視範圍(FOV)", '"(FOV OR "Field of view" OR可視範圍 OR 視野)@TI,AB,CL,DE"'],
        ["增加虛擬距離(VID)", '"(VID OR "Virtual Image Distance" OR 虚像距离 OR 虛擬距離 OR 虛像 )@TI,AB,CL,DE"'],
        ["引導光線性質變化", '"(Reflector OR Reflection OR "beam splitter")@TI,AB,CL,DE"'],
        ["擴增視覺維度(3D)", '"(Polarization OR 偏振 OR 偏光 OR Polarizing OR "diffraction pattern" OR Phase OR "phase modulation" OR amplitude)@TI,AB,CL,DE"'],
        ["增加視覺焦點平面(Focal)", '"("Double-focal" OR "Multi focal" OR "Dual-focal" OR "two or more focal" OR 多焦 OR 雙焦 OR planes OR planar OR 平面)@TI,AB,CL,DE"']
    ]
    
    table = doc.add_table(rows=len(effect_data), cols=2)
    table.style = 'Table Grid'
    for i, row in enumerate(effect_data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            run = cell.paragraphs[0].add_run(val)
            set_chinese_font(run, size=10, bold=(i==0))

    # --- 6. 技術功效矩陣分析 ---
    # 
    doc.add_heading('三、技術功效矩陣分析', level=1)
    doc.add_paragraph("[請在此處插入技術功效矩陣氣泡圖]")
    
    # 儲存
    doc.save('.data/期末報告_自動生成版.docx')
'''