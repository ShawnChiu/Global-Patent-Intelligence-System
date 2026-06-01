import base64
from typing import Any


def figure_data(fig: Any) -> list[dict]:
    if hasattr(fig, "to_plotly_json"):
        return fig.to_plotly_json().get("data", [])
    if isinstance(fig, dict):
        return fig.get("data", [])
    return []


def figure_title(fig: Any) -> str:
    layout = {}
    if hasattr(fig, "to_plotly_json"):
        layout = fig.to_plotly_json().get("layout", {})
    elif isinstance(fig, dict):
        layout = fig.get("layout", {})

    title = layout.get("title", "")
    if isinstance(title, dict):
        return str(title.get("text") or "圖表")
    return str(title or "圖表")


def extract_bar_points(fig: Any) -> list[tuple[str, float]]:
    points = []
    for trace in figure_data(fig):
        if trace.get("type") != "bar":
            continue

        x_values = as_list(trace.get("x", []))
        y_values = as_list(trace.get("y", []))
        if trace.get("orientation") == "h":
            labels, values = y_values, x_values
        else:
            labels, values = x_values, y_values

        for label, value in zip(labels, values):
            parsed = to_float(value)
            if parsed is not None:
                points.append((str(label), parsed))
    return points


def extract_line_points(fig: Any) -> list[tuple[str, float]]:
    points = []
    for trace in figure_data(fig):
        if trace.get("type") not in {"scatter", "line"}:
            continue

        x_values = as_list(trace.get("x", []))
        y_values = as_list(trace.get("y", []))
        for label, value in zip(x_values, y_values):
            parsed = to_float(value)
            if parsed is not None:
                points.append((str(label), parsed))
    return points


def extract_matrix_points(fig: Any) -> tuple[list[tuple[str, str, float]], list[str], list[str]]:
    points = []
    x_labels = []
    y_labels = []

    for trace in figure_data(fig):
        if trace.get("type") != "scatter":
            continue

        xs = as_list(trace.get("x", []))
        ys = as_list(trace.get("y", []))
        text = as_list(trace.get("text", []))
        sizes = as_list((trace.get("marker") or {}).get("size", []))

        for index, (x_label, y_label) in enumerate(zip(xs, ys)):
            value = None
            if index < len(text):
                value = to_float(text[index])
            if value is None and index < len(sizes):
                value = to_float(sizes[index])
            if value is None:
                value = 1

            x_label = str(x_label)
            y_label = str(y_label)
            points.append((x_label, y_label, value))
            if x_label not in x_labels:
                x_labels.append(x_label)
            if y_label not in y_labels:
                y_labels.append(y_label)

    return points, x_labels, y_labels


def as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, dict) and "bdata" in value and "dtype" in value:
        return decode_plotly_typed_array(value)
    if hasattr(value, "tolist"):
        return value.tolist()
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, list):
        return value
    return [value]


def decode_plotly_typed_array(value: dict) -> list:
    try:
        import numpy as np

        dtype = np.dtype(value["dtype"])
        raw = base64.b64decode(value["bdata"])
        values = np.frombuffer(raw, dtype=dtype)
        if value.get("shape"):
            values = values.reshape(value["shape"])
        return values.tolist()
    except Exception:
        return []


def to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(str(value).replace(",", "").replace("(", "").replace(")", "").strip())
    except Exception:
        return None
