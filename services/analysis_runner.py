from dataclasses import dataclass
from typing import Callable, Optional

from models.gemini_client import GeminiClient
from models.gpss_client import GPSSClient
from services.settings_manager import setmgr
from services.parser import Parser
from services.gen_report import ReportGenerator
from config import EXAMPLE_CONFIG


ProgressCallback = Callable[[str, str], None]


@dataclass
class AnalysisInputs:
    topic_select: str = "自訂"
    topic: str = ""
    gpss_id: str = ""
    gpss_pw: str = ""
    gemini_api_key: str = ""
    login_mode: str = "自動辨識驗證碼"
    search_mode: str = "搜尋布林檢索式"
    matrix_mode: str = "關鍵字規則 (Rule-based)"
    query: str = ""
    source: str = ""
    conf_source: str = ""
    matrix: dict = None
    name: str = ""
    student_id: str = ""


def _emit(callback: Optional[ProgressCallback], level: str, message: str):
    if callback:
        callback(level, message)


def apply_example(inputs: AnalysisInputs):
    if inputs.topic_select == "自訂":
        return

    example = EXAMPLE_CONFIG[inputs.topic_select]
    inputs.topic = inputs.topic_select
    inputs.query = example["main_boolean"]
    inputs.matrix = example["matrix"]
    inputs.search_mode = "搜尋布林檢索式"
    inputs.matrix_mode = "關鍵字規則 (Rule-based)"


def validate_inputs(inputs: AnalysisInputs, callback: Optional[ProgressCallback] = None):
    apply_example(inputs)

    needs_gemini = (
        inputs.search_mode == "AI 檢索式推論 (Gemini LLM)"
        or inputs.matrix_mode == "AI 語意推論 (Gemini LLM)"
    )
    if needs_gemini and not inputs.gemini_api_key:
        raise ValueError("尚未輸入 Gemini API")

    if inputs.search_mode == "搜尋布林檢索式":
        if not inputs.query or not Parser.is_valid_parentheses(inputs.query):
            raise ValueError("非法布林檢索式")

    if inputs.matrix_mode == "關鍵字規則 (Rule-based)":
        matrix = inputs.matrix or {}
        if not matrix.get("technologies"):
            raise ValueError("非法技術布林式")
        for i, tech in enumerate(matrix["technologies"][:6]):
            if not Parser.is_valid_parentheses(tech.get("boolean", "")):
                raise ValueError(f"非法技術布林式：{i + 1}")

        if not matrix.get("efficacies"):
            raise ValueError("非法功效布林式")
        for i, eff in enumerate(matrix["efficacies"][:6]):
            if not Parser.is_valid_parentheses(eff.get("boolean", "")):
                raise ValueError(f"非法功效布林式：{i + 1}")

    _emit(callback, "success", "輸入分析完成")


def run_patent_analysis(inputs: AnalysisInputs, callback: Optional[ProgressCallback] = None):
    validate_inputs(inputs, callback)

    gemini_client = None
    if inputs.gemini_api_key and (
        inputs.search_mode == "AI 檢索式推論 (Gemini LLM)"
        or inputs.matrix_mode == "AI 語意推論 (Gemini LLM)"
    ):
        gemini_client = GeminiClient(inputs.gemini_api_key)

    gpss_client = GPSSClient()
    try:
        _emit(callback, "info", "正在登入 GPSS ...")
        if not gpss_client.login(inputs.gpss_id, inputs.gpss_pw, True):
            raise RuntimeError("登入失敗：請確認帳號密碼是否正確或是再試一次")

        setmgr.settings.gpss_id = inputs.gpss_id
        setmgr.settings.gpss_pw = inputs.gpss_pw
        _emit(callback, "success", "登入成功")

        if inputs.search_mode == "AI 檢索式推論 (Gemini LLM)":
            _emit(callback, "info", "正在生成布林檢索式 ...")
            inputs.query = gemini_client.convert_topic_to_query(inputs.topic)
            setmgr.settings.gemini_api_key = inputs.gemini_api_key

        _emit(callback, "info", "正在搜索專利 ...")
        gpss_client.search(inputs.query)
        setmgr.settings.query = inputs.query
        _emit(callback, "success", f"搜索到：{gpss_client.search_result} 筆資料")

        _emit(callback, "info", "正在獲取圖表資料 ...")
        gpss_client.fetch_diagrams()
        _emit(callback, "success", "獲取圖表成功")

        if gpss_client.dedup_result is not None and gpss_client.dedup_result <= 30000:
            _emit(callback, "info", "正在進行矩陣維度分析 ...")
            if inputs.matrix_mode == "AI 語意推論 (Gemini LLM)":
                gpss_client.fetch_names_and_contents()
                inputs.matrix, state = gemini_client.generate_gpss_strategy(
                    gpss_client.diagram_buffers["contents"]
                )
                if state != "Success":
                    raise RuntimeError(state)
                setmgr.settings.gemini_api_key = inputs.gemini_api_key
            _emit(callback, "success", "維度分析完成")
        else:
            _emit(callback, "warning", "專利筆數超過 30000，跳過矩陣分析步驟")

        _emit(callback, "info", "正在進行矩陣分析 ...")
        gpss_client.fill_matrix_form(inputs.matrix)
        setmgr.settings.matrix = inputs.matrix
        _emit(callback, "success", "矩陣分析完成")

        diagram_buffers = gpss_client.diagram_buffers
        search_result = gpss_client.search_result
        dedup_result = gpss_client.dedup_result
    finally:
        gpss_client.close()

    _emit(callback, "info", "正在解析圖表資料 ...")
    fig_buffers, img_buffers = Parser.parse_diagrams(
        diagram_buffers,
        callback=callback,
        export_images=False,
    )
    _emit(callback, "info", "正在產生 PDF 報告 ...")
    report = ReportGenerator(
        search_result=[search_result, dedup_result],
        query=inputs.query,
        matrix_json=inputs.matrix,
        topic=inputs.topic,
        source=[inputs.source, inputs.conf_source],
        figures=fig_buffers,
    )

    pdf = report.gen_report()
    setmgr.save()
    _emit(callback, "success", "分析報告完成")

    return {
        "query": inputs.query,
        "matrix": inputs.matrix,
        "fig": fig_buffers,
        "img": img_buffers,
        "pdf": pdf,
        "search_result": [search_result, dedup_result],
    }
