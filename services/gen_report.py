import html
import math
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from services.chart_data import (
    extract_bar_points,
    extract_line_points,
    extract_matrix_points,
    figure_title,
)
from services.parser import Parser


class ReportGenerator:
    def __init__(
        self,
        topic="",
        search_result=None,
        query="",
        students_data=None,
        source=None,
        matrix_json=None,
        chart_buffers=None,
        figures=None,
    ):
        self.report_title = "智財分析報告"
        self.topic = topic or "未命名主題"
        self.search_result = search_result or [0, 0]
        self.query = query or ""
        self.scope = Parser.parse_query(self.query)
        self.students_data = students_data or []
        self.source = source or ["", ""]
        self.matrix_json = matrix_json or {}
        self.chart_buffers = chart_buffers or {}
        self.figures = figures or {}

        self.font_name = _register_font()
        self.styles = _build_styles(self.font_name)

    def gen_report(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.75 * cm,
            leftMargin=1.75 * cm,
            topMargin=1.7 * cm,
            bottomMargin=1.55 * cm,
            title=self.report_title,
            author="Global Patent Intelligence System",
        )

        story = []
        story.extend(self._cover())
        story.append(PageBreak())
        story.extend(self._summary_section())
        story.append(PageBreak())
        story.extend(self._chart_section())
        if self.matrix_json:
            story.append(PageBreak())
            story.extend(self._matrix_section())

        doc.build(story, onFirstPage=self._draw_page, onLaterPages=self._draw_page)
        buffer.seek(0)
        return buffer

    def _cover(self):
        return [
            Spacer(1, 3.2 * cm),
            Paragraph(self.report_title, self.styles["CoverTitle"]),
            Spacer(1, 0.55 * cm),
            Paragraph(_safe(self.topic), self.styles["CoverTopic"]),
            Spacer(1, 1.3 * cm),
            Table(
                [
                    ["分析日期", datetime.now().strftime("%Y-%m-%d")],
                    ["資料來源", "GPSS 專利檢索與統計圖表"],
                    ["分析範圍", self.scope or "依本次布林檢索式與矩陣條件界定"],
                ],
                colWidths=[3.2 * cm, 11.2 * cm],
                style=[
                    ("FONTNAME", (0, 0), (-1, -1), self.font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 10.5),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#334155")),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e2e8f0")),
                    ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dbe3ef")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ],
            ),
            Spacer(1, 4.6 * cm),
            Paragraph("本報告由系統依本次智財分析資料自動生成，內容包含檢索策略、專利管理圖、技術功效矩陣與重點觀察。", self.styles["Note"]),
        ]

    def _summary_section(self):
        total, deduped = _result_pair(self.search_result)
        source_text = self.source[0] or "未填寫"
        scope_text = self.scope or "未解析到 IPC/CPC 條件，依完整檢索式判定分析範圍。"

        return [
            Paragraph("一、研究設計與檢索摘要", self.styles["Heading1"]),
            Paragraph(
                _safe(
                    f"本研究以「{self.topic}」為分析主題，透過 GPSS 執行專利資料檢索，"
                    f"初始取得 {total} 筆資料；經去重與專利家族整理後，納入分析樣本為 {deduped} 筆。"
                ),
                self.styles["Body"],
            ),
            Spacer(1, 0.3 * cm),
            Paragraph("1.1 檢索式", self.styles["Heading2"]),
            Paragraph(_safe(self.query or "未提供檢索式"), self.styles["Code"]),
            Spacer(1, 0.25 * cm),
            Paragraph("1.2 分析範圍與資料來源", self.styles["Heading2"]),
            _kv_table(
                self.font_name,
                [
                    ("分析範圍", scope_text),
                    ("來源說明", source_text),
                    ("資料處理", "以檢索結果去重、統計圖表解析與矩陣交叉分析作為主要處理流程。"),
                ],
            ),
            Spacer(1, 0.45 * cm),
            Paragraph("1.3 方法說明", self.styles["Heading2"]),
            Paragraph(
                "本報告採用描述性統計與矩陣式技術分類方法，先由專利數量、權利人、布局國家與申請趨勢建立整體樣貌，"
                "再以技術與功效兩個維度交叉檢視專利分布，以輔助辨識技術密集區、競爭者集中度與潛在研發空白。",
                self.styles["Body"],
            ),
        ]

    def _chart_section(self):
        sections = [
            ("ipc", "2.1 技術領域分類分析", "bar"),
            ("assignee", "2.2 技術領先企業分析", "bar"),
            ("country", "2.3 主要布局國家分析", "bar"),
            ("trend_range", "2.4 專利申請趨勢分析", "line"),
        ]
        story = [Paragraph("二、專利管理圖分析", self.styles["Heading1"])]
        for key, title, chart_type in sections:
            fig = self.figures.get(key)
            story.append(Paragraph(title, self.styles["Heading2"]))
            if fig:
                story.append(
                    KeepTogether(
                        [
                            FigureChart(fig, chart_type, self.font_name, width=16.1 * cm, height=8.2 * cm),
                            Spacer(1, 0.2 * cm),
                            _chart_data_table(key, fig, self.font_name),
                            Spacer(1, 0.18 * cm),
                            Paragraph(_safe(_analysis_for_figure(key, fig)), self.styles["Body"]),
                        ]
                    )
                )
            else:
                story.append(Paragraph("本項圖表資料未取得，因此未納入圖形化分析。", self.styles["Body"]))
            story.append(Spacer(1, 0.42 * cm))
        return story

    def _matrix_section(self):
        story = [Paragraph("三、技術功效矩陣分析", self.styles["Heading1"])]
        technologies = _items(self.matrix_json.get("technologies", []))
        efficacies = _items(self.matrix_json.get("efficacies", []))

        story.append(Paragraph("3.1 技術分類關鍵字", self.styles["Heading2"]))
        story.append(_keyword_table(self.font_name, technologies, "技術分類", "布林檢索式"))
        story.append(Spacer(1, 0.35 * cm))

        story.append(Paragraph("3.2 功效分類關鍵字", self.styles["Heading2"]))
        story.append(_keyword_table(self.font_name, efficacies, "功效分類", "布林檢索式"))
        if self.source[1]:
            story.append(Paragraph(_safe(f"矩陣分類來源說明：{self.source[1]}"), self.styles["Note"]))
        story.append(Spacer(1, 0.35 * cm))

        story.append(Paragraph("3.3 技術功效矩陣圖", self.styles["Heading2"]))
        fig = self.figures.get("matrix")
        if fig:
            story.append(FigureChart(fig, "matrix", self.font_name, width=16.1 * cm, height=8.8 * cm))
            story.append(Spacer(1, 0.2 * cm))
            story.append(_chart_data_table("matrix", fig, self.font_name))
            story.append(Spacer(1, 0.18 * cm))
            story.append(Paragraph(_safe(_analysis_for_figure("matrix", fig)), self.styles["Body"]))
        else:
            story.append(Paragraph("本次未取得矩陣圖表資料。", self.styles["Body"]))
        return story

    def _draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font_name, 8.5)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(doc.leftMargin, 1.0 * cm, self.report_title)
        canvas.drawRightString(A4[0] - doc.rightMargin, 1.0 * cm, f"第 {doc.page} 頁")
        canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
        canvas.setLineWidth(0.35)
        canvas.line(doc.leftMargin, 1.25 * cm, A4[0] - doc.rightMargin, 1.25 * cm)
        canvas.restoreState()


class FigureChart(Flowable):
    def __init__(self, figure, chart_type, font_name, width, height):
        super().__init__()
        self.figure = figure
        self.chart_type = chart_type
        self.font_name = font_name
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        self._draw_frame(c)
        if self.chart_type == "line":
            self._draw_line(c)
        elif self.chart_type == "matrix":
            self._draw_matrix(c)
        else:
            self._draw_bar(c)
        c.restoreState()

    def _draw_frame(self, c):
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(0.55)
        c.roundRect(0, 0, self.width, self.height, 5, fill=0, stroke=1)
        c.setFont(self.font_name, 11)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(0.45 * cm, self.height - 0.55 * cm, figure_title(self.figure))

    def _draw_bar(self, c):
        points = extract_bar_points(self.figure)
        if not points:
            _draw_no_data(c, self.font_name, self.width, self.height)
            return

        points = sorted(points, key=lambda item: item[1], reverse=True)[:12]
        max_value = max(value for _, value in points) or 1
        label_w = min(4.8 * cm, self.width * 0.36)
        plot_x = label_w + 0.6 * cm
        plot_y = 0.65 * cm
        plot_w = self.width - plot_x - 1.1 * cm
        plot_h = self.height - 1.7 * cm
        row_h = plot_h / max(len(points), 1)

        _draw_grid(c, plot_x, plot_y, plot_w, plot_h, max_value, self.font_name)
        palette = ["#2563eb", "#0891b2", "#16a34a", "#ca8a04", "#dc2626", "#7c3aed"]
        c.setFont(self.font_name, 8.2)
        for index, (label, value) in enumerate(points):
            y_mid = plot_y + plot_h - (index + 0.5) * row_h
            bar_h = min(row_h * 0.55, 0.34 * cm)
            bar_w = max((value / max_value) * plot_w, 1.5)
            color = colors.HexColor(palette[index % len(palette)])
            c.setFillColor(colors.HexColor("#334155"))
            _draw_ellipsis(c, label, plot_x - 0.18 * cm, y_mid - 3, label_w - 0.3 * cm, self.font_name, 8.2, align="right")
            c.setFillColor(color)
            c.roundRect(plot_x, y_mid - bar_h / 2, bar_w, bar_h, 2.2, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#0f172a"))
            c.drawString(plot_x + bar_w + 3, y_mid - 3, _fmt_number(value))

    def _draw_line(self, c):
        points = extract_line_points(self.figure)
        if len(points) < 2:
            _draw_no_data(c, self.font_name, self.width, self.height)
            return

        plot_x = 1.15 * cm
        plot_y = 1.0 * cm
        plot_w = self.width - 2.0 * cm
        plot_h = self.height - 2.2 * cm
        ys = [value for _, value in points]
        min_y = min(ys)
        max_y = max(ys)
        if min_y == max_y:
            min_y = 0
        y_range = max(max_y - min_y, 1)

        c.setStrokeColor(colors.HexColor("#cbd5e1"))
        c.setLineWidth(0.5)
        for i in range(5):
            y = plot_y + plot_h * i / 4
            c.line(plot_x, y, plot_x + plot_w, y)
        c.setStrokeColor(colors.HexColor("#334155"))
        c.line(plot_x, plot_y, plot_x, plot_y + plot_h)
        c.line(plot_x, plot_y, plot_x + plot_w, plot_y)

        coords = []
        for index, (label, value) in enumerate(points):
            x = plot_x + (plot_w * index / max(len(points) - 1, 1))
            y = plot_y + ((value - min_y) / y_range) * plot_h
            coords.append((x, y, label, value))

        c.setStrokeColor(colors.HexColor("#0284c7"))
        c.setLineWidth(2.2)
        for first, second in zip(coords, coords[1:]):
            c.line(first[0], first[1], second[0], second[1])

        c.setFont(self.font_name, 8)
        c.setFillColor(colors.HexColor("#0f172a"))
        stride = max(1, math.ceil(len(coords) / 7))
        for index, (x, y, label, value) in enumerate(coords):
            c.setFillColor(colors.HexColor("#0284c7"))
            c.circle(x, y, 3.2, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#0f172a"))
            if index % stride == 0 or index == len(coords) - 1:
                c.drawCentredString(x, plot_y - 0.35 * cm, str(label))
            c.drawCentredString(x, y + 0.18 * cm, _fmt_number(value))

    def _draw_matrix(self, c):
        points, x_labels, y_labels = extract_matrix_points(self.figure)
        if not points or not x_labels or not y_labels:
            _draw_no_data(c, self.font_name, self.width, self.height)
            return

        plot_x = 3.2 * cm
        plot_y = 1.1 * cm
        plot_w = self.width - 4.0 * cm
        plot_h = self.height - 2.65 * cm
        cell_w = plot_w / max(len(x_labels), 1)
        cell_h = plot_h / max(len(y_labels), 1)
        max_value = max(value for _, _, value in points) or 1

        c.setStrokeColor(colors.HexColor("#dbe3ef"))
        c.setLineWidth(0.45)
        for i in range(len(x_labels) + 1):
            x = plot_x + i * cell_w
            c.line(x, plot_y, x, plot_y + plot_h)
        for i in range(len(y_labels) + 1):
            y = plot_y + i * cell_h
            c.line(plot_x, y, plot_x + plot_w, y)

        c.setFont(self.font_name, 7.5)
        c.setFillColor(colors.HexColor("#334155"))
        for idx, label in enumerate(x_labels):
            x = plot_x + (idx + 0.5) * cell_w
            c.saveState()
            c.translate(x, plot_y + plot_h + 0.22 * cm)
            c.rotate(28)
            _draw_ellipsis(c, label, 0, 0, 2.4 * cm, self.font_name, 7.5)
            c.restoreState()
        for idx, label in enumerate(y_labels):
            y = plot_y + plot_h - (idx + 0.5) * cell_h
            _draw_ellipsis(c, label, plot_x - 0.24 * cm, y - 2.5, 2.7 * cm, self.font_name, 7.5, align="right")

        palette = ["#2563eb", "#0891b2", "#16a34a", "#ca8a04", "#dc2626", "#7c3aed"]
        c.setFont(self.font_name, 7.5)
        for index, (x_label, y_label, value) in enumerate(points):
            if x_label not in x_labels or y_label not in y_labels:
                continue
            x = plot_x + (x_labels.index(x_label) + 0.5) * cell_w
            y = plot_y + plot_h - (y_labels.index(y_label) + 0.5) * cell_h
            radius = 4 + 10 * math.sqrt(value / max_value)
            c.setFillColor(colors.HexColor(palette[index % len(palette)]))
            c.circle(x, y, radius, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.drawCentredString(x, y - 2.5, _fmt_number(value))


def _register_font():
    candidates = []
    windir = os.environ.get("WINDIR", r"C:\Windows")
    fonts_dir = Path(windir) / "Fonts"
    candidates.extend(
        [
            fonts_dir / "msjh.ttc",
            fonts_dir / "msjh.ttf",
            fonts_dir / "mingliu.ttc",
            fonts_dir / "kaiu.ttf",
            fonts_dir / "NotoSansCJKtc-Regular.otf",
        ]
    )
    for path in candidates:
        if not path.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont("ReportCJK", str(path)))
            return "ReportCJK"
        except Exception:
            continue

    for cid_font in ("MSung-Light", "STSong-Light"):
        try:
            pdfmetrics.registerFont(UnicodeCIDFont(cid_font))
            return cid_font
        except Exception:
            continue
    return "Helvetica"


def _build_styles(font_name):
    return {
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            fontName=font_name,
            fontSize=25,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=12,
        ),
        "CoverTopic": ParagraphStyle(
            "CoverTopic",
            fontName=font_name,
            fontSize=15,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
        ),
        "Heading1": ParagraphStyle(
            "Heading1",
            fontName=font_name,
            fontSize=16,
            leading=22,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
            spaceBefore=6,
        ),
        "Heading2": ParagraphStyle(
            "Heading2",
            fontName=font_name,
            fontSize=12.4,
            leading=18,
            textColor=colors.HexColor("#1e40af"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "Body": ParagraphStyle(
            "Body",
            fontName=font_name,
            fontSize=10.4,
            leading=17,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2937"),
            firstLineIndent=0.55 * cm,
        ),
        "Code": ParagraphStyle(
            "Code",
            fontName=font_name,
            fontSize=8.6,
            leading=12.2,
            textColor=colors.HexColor("#1e3a8a"),
            backColor=colors.HexColor("#eef2ff"),
            borderColor=colors.HexColor("#c7d2fe"),
            borderWidth=0.4,
            borderPadding=7,
            wordWrap="CJK",
        ),
        "Note": ParagraphStyle(
            "Note",
            fontName=font_name,
            fontSize=9.2,
            leading=13,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_CENTER,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            fontName=font_name,
            fontSize=8.8,
            leading=12,
            textColor=colors.HexColor("#1f2937"),
            wordWrap="CJK",
        ),
    }


def _kv_table(font_name, rows):
    style = _build_styles(font_name)["TableCell"]
    data = [[Paragraph(_safe(k), style), Paragraph(_safe(v), style)] for k, v in rows]
    table = Table(data, colWidths=[3.2 * cm, 12.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e2e8f0")),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#ffffff")),
                ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dbe3ef")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _keyword_table(font_name, items, left_header, right_header):
    styles = _build_styles(font_name)
    rows = [[Paragraph(left_header, styles["TableCell"]), Paragraph(right_header, styles["TableCell"])]]
    rows.extend([[Paragraph(_safe(item["label"]), styles["TableCell"]), Paragraph(_safe(item["boolean"]), styles["TableCell"])] for item in items])
    if len(rows) == 1:
        rows.append([Paragraph("無資料", styles["TableCell"]), Paragraph("無資料", styles["TableCell"])])
    table = LongTable(rows, colWidths=[4.0 * cm, 11.7 * cm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dbe3ef")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _chart_data_table(key, fig, font_name):
    styles = _build_styles(font_name)
    cell_style = styles["TableCell"]

    if key in {"ipc", "assignee", "country"}:
        label_name = {
            "ipc": "分類",
            "assignee": "權利人",
            "country": "國家/地區",
        }[key]
        points = sorted(extract_bar_points(fig), key=lambda item: item[1], reverse=True)[:12]
        rows = [[label_name, "件數"]]
        rows.extend([[label, _fmt_number(value)] for label, value in points])
        col_widths = [11.2 * cm, 4.5 * cm]
    elif key == "trend_range":
        points = extract_line_points(fig)
        rows = [["年份", "申請件數"]]
        rows.extend([[label, _fmt_number(value)] for label, value in points])
        col_widths = [7.8 * cm, 7.9 * cm]
    elif key == "matrix":
        points, _, _ = extract_matrix_points(fig)
        rows = [["技術分類", "功效分類", "件數"]]
        sorted_points = sorted(points, key=lambda item: item[2], reverse=True)[:12]
        rows.extend(
            [[tech, efficacy, _fmt_number(value)] for tech, efficacy, value in sorted_points]
        )
        col_widths = [6.3 * cm, 6.3 * cm, 3.1 * cm]
    else:
        rows = [["資料", "數值"]]
        col_widths = [7.8 * cm, 7.9 * cm]

    if len(rows) == 1:
        rows.append(["無資料", "0"])

    table = LongTable(
        [[Paragraph(_safe(cell), cell_style) for cell in row] for row in rows],
        colWidths=col_widths,
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ffffff")),
                ("BOX", (0, 0), (-1, -1), 0.45, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def _analysis_for_figure(key, fig):
    if key in {"ipc", "assignee", "country"}:
        points = sorted(extract_bar_points(fig), key=lambda item: item[1], reverse=True)
        if not points:
            return "本圖未提供足夠數據供分析。"
        top_label, top_value = points[0]
        total = sum(value for _, value in points) or top_value
        share = top_value / total * 100 if total else 0
        if key == "ipc":
            return f"觀察重點：{top_label} 為本次樣本中最集中的技術分類，約占圖表可視樣本 {share:.1f}%。此結果可作為後續技術分類、競品監測與研發布局判斷的優先切入點。"
        if key == "assignee":
            return f"觀察重點：{top_label} 在主要權利人中排名最高，顯示此領域存在明確的專利持有者。若前幾名數量差距明顯，代表競爭優勢可能集中於少數企業或機構。"
        return f"觀察重點：{top_label} 是本次資料中布局最明顯的國家或地區，約占可視樣本 {share:.1f}%。此資訊可用於判斷主要市場、製造布局與潛在侵權風險區域。"

    if key == "trend_range":
        points = extract_line_points(fig)
        if len(points) < 2:
            return "本圖未提供足夠趨勢資料。"
        first_label, first_value = points[0]
        last_label, last_value = points[-1]
        direction = "上升" if last_value > first_value else "下降" if last_value < first_value else "持平"
        peak_label, peak_value = max(points, key=lambda item: item[1])
        return f"觀察重點：申請量由 {first_label} 的 {_fmt_number(first_value)} 件至 {last_label} 的 {_fmt_number(last_value)} 件，整體呈現{direction}趨勢；其中 {peak_label} 達到高峰，顯示該時期可能是技術投入或市場競爭最活躍的階段。"

    if key == "matrix":
        points, _, _ = extract_matrix_points(fig)
        if not points:
            return "本次矩陣未取得可視化交叉數據。"
        x_label, y_label, value = max(points, key=lambda item: item[2])
        return f"觀察重點：矩陣中「{x_label}」與「{y_label}」的交叉數量最高，共 {_fmt_number(value)} 件，代表該技術與功效組合是目前專利布局最密集的位置。低數量或空白區域則可作為後續研發差異化與迴避設計的參考。"

    return "本圖提供本次智財分析的描述性統計結果，可搭配檢索式與矩陣分類進一步解讀。"


def _items(items):
    return [item for item in items if item.get("label") or item.get("boolean")]


def _result_pair(search_result):
    values = list(search_result or [0, 0])
    while len(values) < 2:
        values.append(0)
    return values[0], values[1]


def _safe(text):
    return html.escape(str(text or "")).replace("\n", "<br/>")


def _fmt_number(value):
    if value is None:
        return "0"
    if abs(value - int(value)) < 0.00001:
        return f"{int(value):,}"
    return f"{value:,.1f}"


def _draw_grid(c, x, y, width, height, max_value, font_name):
    c.setStrokeColor(colors.HexColor("#dbe3ef"))
    c.setLineWidth(0.45)
    c.setFont(font_name, 7.5)
    c.setFillColor(colors.HexColor("#64748b"))
    for i in range(5):
        gx = x + width * i / 4
        c.line(gx, y, gx, y + height)
        c.drawCentredString(gx, y - 0.28 * cm, _fmt_number(max_value * i / 4))
    c.setStrokeColor(colors.HexColor("#334155"))
    c.line(x, y, x + width, y)


def _draw_ellipsis(c, text, x, y, max_width, font_name, size, align="left"):
    text = str(text or "")
    c.setFont(font_name, size)
    if c.stringWidth(text, font_name, size) > max_width:
        while text and c.stringWidth(text + "...", font_name, size) > max_width:
            text = text[:-1]
        text = text + "..." if text else "..."
    if align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)


def _draw_no_data(c, font_name, width, height):
    c.setFont(font_name, 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(width / 2, height / 2, "無圖表資料")


# Backward-compatible alias for existing imports.
ReportGenrator = ReportGenerator
