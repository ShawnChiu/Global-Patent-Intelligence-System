import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const searchModes = ["搜尋布林檢索式", "AI 檢索式推論 (Gemini LLM)"];
const matrixModes = ["關鍵字規則 (Rule-based)", "AI 語意推論 (Gemini LLM)"];

const tabs = [
  ["query", "布林檢索式"],
  ["ipc", "技術領域分類分析"],
  ["assignee", "技術領先企業"],
  ["country", "主要布局國家"],
  ["trend_range", "專利申請趨勢"],
  ["keywords", "矩陣分析關鍵字"],
  ["matrix", "技術功效矩陣"]
];

function App() {
  const [examples, setExamples] = useState([]);
  const [form, setForm] = useState(defaultForm());
  const [matrixDraft, setMatrixDraft] = useState(defaultMatrix());
  const [modal, setModal] = useState(null);
  const [job, setJob] = useState({ status: "idle", messages: [] });
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState("query");

  useEffect(() => {
    fetch("/api/bootstrap")
      .then((res) => res.json())
      .then((data) => {
        setExamples(data.examples || []);
        setForm((current) => ({
          ...current,
          ...mapDefaults(data.defaults || {})
        }));
      });
  }, []);

  const isCustom = form.topic_select === "自訂";
  const needsApi = isCustom && (
    form.search_mode === "AI 檢索式推論 (Gemini LLM)"
    || form.matrix_mode === "AI 語意推論 (Gemini LLM)"
  );

  function updateField(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function openMatrix() {
    setMatrixDraft(normalizeMatrix(form.matrix));
    setModal("matrix");
  }

  function saveMatrix() {
    setForm((current) => ({
      ...current,
      matrix: {
        technologies: compactItems(matrixDraft.technologies),
        efficacies: compactItems(matrixDraft.efficacies)
      }
    }));
    setModal(null);
  }

  async function startAnalyze() {
    setResult(null);
    setActiveTab("query");
    setJob({ status: "queued", messages: [] });

    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });

    if (!response.ok) {
      setJob({ status: "error", messages: [{ level: "error", message: await response.text(), time: "" }] });
      return;
    }

    const { job_id } = await response.json();
    pollJob(job_id);
  }

  async function pollJob(jobId) {
    const response = await fetch(`/api/jobs/${jobId}`);
    const data = await response.json();
    setJob(data);

    if (data.status === "done") {
      setResult(data.result);
      setForm((current) => ({
        ...current,
        query: data.result?.query || current.query,
        matrix: data.result?.matrix || current.matrix
      }));
      return;
    }

    if (data.status !== "error") {
      window.setTimeout(() => pollJob(jobId), 1000);
    }
  }

  const canStart = job.status !== "running" && job.status !== "queued";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 lg:grid lg:grid-cols-[320px_1fr]">
      <aside className="border-b border-white/10 bg-slate-900 p-4 lg:h-screen lg:overflow-y-auto lg:border-b-0 lg:border-r">
        <SidebarSection title="🌸 GPSS 帳號">
          <button className="btn-secondary" onClick={() => setModal("basic")}>✏️ 點擊編輯 GPSS 帳號</button>
        </SidebarSection>

        <SidebarSection title="🍬 專利主題">
          <FieldLabel>選擇主題</FieldLabel>
          <select className="input" value={form.topic_select} onChange={(e) => updateField("topic_select", e.target.value)}>
            {examples.map((name) => <option key={name} value={name}>{name}</option>)}
            <option value="自訂">自訂</option>
          </select>
          {isCustom && (
            <>
              <FieldLabel>輸入技術主題</FieldLabel>
              <input className="input" value={form.topic} onChange={(e) => updateField("topic", e.target.value)} placeholder="輸入你的專利技術主題" />
            </>
          )}
        </SidebarSection>

        {isCustom && (
          <>
            <SidebarSection title="🔍 搜尋條件">
              <FieldLabel>選擇搜尋模式</FieldLabel>
              <RadioGroup name="search" value={form.search_mode} options={searchModes} captions={["快速、免費", "需 Google API Key"]} onChange={(value) => updateField("search_mode", value)} />
              {form.search_mode !== "AI 檢索式推論 (Gemini LLM)" ? (
                <button className="btn-secondary mt-3" onClick={() => setModal("query")}>✏️ 點擊編輯檢索式</button>
              ) : (
                <p className="mt-3 text-sm text-slate-400">🧠 AI 自動生成布林檢索式 系統將根據主題自動生成複雜的布林檢索式</p>
              )}
            </SidebarSection>

            <SidebarSection title="🤖 分析設定">
              <FieldLabel>選擇矩陣分析模式</FieldLabel>
              <RadioGroup name="matrix" value={form.matrix_mode} options={matrixModes} captions={["快速、免費，需定義關鍵字", "精準、自動分類，需 Google API Key"]} onChange={(value) => updateField("matrix_mode", value)} />
              {form.matrix_mode !== "AI 語意推論 (Gemini LLM)" ? (
                <button className="btn-secondary mt-3" onClick={openMatrix}>✏️ 點擊編輯關鍵字</button>
              ) : (
                <p className="mt-3 text-sm text-slate-400">🧠 AI 全自動分類 系統將自動閱讀專利摘要並分析功效定義</p>
              )}
            </SidebarSection>

            {needsApi && (
              <SidebarSection title="🔑 API 設定">
                <button className="btn-secondary" onClick={() => setModal("api")}>❓ 查看教學</button>
                {!form.gemini_api_key && <p className="mt-3 text-sm text-amber-300">請輸入 Key 以啟動 AI 功能</p>}
                <input className="input mt-3" type="password" value={form.gemini_api_key} onChange={(e) => updateField("gemini_api_key", e.target.value)} placeholder="貼上你的 AI Studio Key" />
              </SidebarSection>
            )}
          </>
        )}

        <button className="btn-primary mt-4" disabled={!canStart} onClick={startAnalyze}>🚀 開始分析</button>
      </aside>

      <main className="h-screen overflow-y-auto p-5 lg:p-7">
        <h1 className="mb-5 text-3xl font-bold">智財分析報告系統</h1>
        <StatusPanel job={job} />
        {result?.pdf && <DownloadPanel pdf={result.pdf} />}
        {result && <Results result={result} form={form} activeTab={activeTab} setActiveTab={setActiveTab} />}
      </main>

      {modal === "basic" && (
        <Modal onClose={() => setModal(null)} title="🌸 GPSS 帳號設定">
          <h3 className="section-subtitle">GPSS 帳號密碼</h3>
          <FieldLabel>GPSS 使用者代碼</FieldLabel>
          <input className="input" value={form.gpss_id} onChange={(e) => updateField("gpss_id", e.target.value)} placeholder="輸入你的 GPSS 使用者代碼" />
          <FieldLabel>GPSS 密碼</FieldLabel>
          <input className="input" type="password" value={form.gpss_pw} onChange={(e) => updateField("gpss_pw", e.target.value)} placeholder="輸入你的 GPSS 密碼" />
          <p className="mt-3 text-sm text-slate-400">登入時會固定使用自動辨識驗證碼。</p>
          <button className="btn-primary mt-4" onClick={() => setModal(null)}>💾 儲存並關閉</button>
        </Modal>
      )}

      {modal === "query" && (
        <Modal onClose={() => setModal(null)} title="✏️ 編輯布林檢索式" wide>
          <p className="mb-3 text-sm text-slate-400">請在下方編輯您的完整檢索式：</p>
          <textarea className="input min-h-96" value={form.query} onChange={(e) => updateField("query", e.target.value)} />
          <FieldLabel>來源說明 (選填)</FieldLabel>
          <input className="input" value={form.source} onChange={(e) => updateField("source", e.target.value)} placeholder="輸入來源" />
          <button className="btn-primary mt-4" onClick={() => setModal(null)}>關閉</button>
        </Modal>
      )}

      {modal === "matrix" && (
        <Modal onClose={() => setModal(null)} title="✏️ 編輯矩陣分析" wide>
          <p className="mb-3 text-sm text-slate-400">請在下方分別定義技術與功效的關鍵字：</p>
          <div className="grid gap-5 xl:grid-cols-2">
            <MatrixEditor title="技術分析" items={matrixDraft.technologies} onChange={(items) => setMatrixDraft((current) => ({ ...current, technologies: items }))} labelPrefix="技術" />
            <MatrixEditor title="功效分析" items={matrixDraft.efficacies} onChange={(items) => setMatrixDraft((current) => ({ ...current, efficacies: items }))} labelPrefix="功效" />
          </div>
          <FieldLabel>來源說明 (選填)</FieldLabel>
          <input className="input" value={form.conf_source} onChange={(e) => updateField("conf_source", e.target.value)} placeholder="輸入來源" />
          <button className="btn-primary mt-4" onClick={saveMatrix}>💾 儲存並關閉</button>
        </Modal>
      )}

      {modal === "api" && (
        <Modal onClose={() => setModal(null)} title="❓ 如何取得 Google Gemini API Key">
          <ol className="list-decimal space-y-2 pl-5 text-sm">
            <li>前往 <strong>Google AI Studio</strong>。</li>
            <li>點擊左下角的 <strong>Get API key</strong>。</li>
            <li>點擊 <strong>Create API key</strong>。</li>
            <li>名字隨意，專案選擇 <strong>Gemini API</strong> 後點選 Create。</li>
            <li>複製生成的 Key 並貼回本系統。</li>
          </ol>
          <button className="btn-primary mt-4" onClick={() => setModal(null)}>💾 儲存並關閉</button>
        </Modal>
      )}
    </div>
  );
}

function SidebarSection({ title, children }) {
  return (
    <section className="border-b border-white/10 py-4">
      <h2 className="mb-3 text-lg font-semibold">{title}</h2>
      {children}
    </section>
  );
}

function FieldLabel({ children }) {
  return <label className="mb-1 mt-3 block text-sm font-semibold">{children}</label>;
}

function RadioGroup({ name, value, options, captions, onChange }) {
  return (
    <div className="grid gap-2">
      {options.map((option, index) => (
        <label key={option} className="grid grid-cols-[18px_1fr] gap-2 rounded-md border border-white/10 bg-slate-800/70 p-2 text-sm text-slate-100">
          <input type="radio" name={name} checked={value === option} onChange={() => onChange(option)} className="mt-1" />
          <span>{option}{captions?.[index] && <small className="block text-slate-400">{captions[index]}</small>}</span>
        </label>
      ))}
    </div>
  );
}

function StatusPanel({ job }) {
  const messages = job.messages || [];
  const isActive = job.status === "queued" || job.status === "running";
  return (
    <section className="mb-5 rounded-lg border border-white/10 bg-slate-900 p-4 shadow-lg shadow-black/20">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">分析狀態</h2>
        <span className="text-sm text-slate-400">{job.status === "idle" ? "尚未開始" : job.status}</span>
      </div>
      <div className="mt-3 max-h-48 overflow-auto">
        {messages.map((message, index) => {
          const isCurrent = isActive && message.level === "info" && index === messages.length - 1;
          const isCompletedInfo = message.level === "info" && !isCurrent;
          return (
          <div key={`${message.time}-${index}`} className={`mb-1 grid grid-cols-[70px_76px_1fr] gap-2 rounded-md bg-slate-950/70 px-2 py-1.5 text-sm ${messageClass(message.level, isCompletedInfo)}`}>
            <span>{message.time}</span>
            <strong>{messageLabel(message.level, isCompletedInfo, isCurrent)}</strong>
            <span>{message.message}{isCurrent && <AnimatedDots />}</span>
          </div>
        )})}
      </div>
    </section>
  );
}

function AnimatedDots() {
  return (
    <span className="inline-flex w-6 justify-start pl-1 text-blue-300" aria-hidden="true">
      <span className="loading-dots">...</span>
    </span>
  );
}

function DownloadPanel({ pdf }) {
  return (
    <section className="mb-5 rounded-lg border border-white/10 bg-slate-900 p-4 shadow-lg shadow-black/20">
      <button className="btn-primary" onClick={() => downloadPdf(pdf)}>📥 下載智財分析報告 (.pdf)</button>
    </section>
  );
}

function Results({ result, form, activeTab, setActiveTab }) {
  return (
    <section className="rounded-lg border border-white/10 bg-slate-900 shadow-lg shadow-black/20">
      <nav className="flex flex-wrap gap-2 border-b border-white/10 p-3">
        {tabs.map(([key, label]) => (
          <button key={key} className={`rounded-md border px-3 py-2 text-sm font-semibold ${activeTab === key ? "border-blue-400/40 bg-blue-500/15 text-blue-200" : "border-white/10 bg-slate-800/70 text-slate-300 hover:bg-slate-700/70"}`} onClick={() => setActiveTab(key)}>
            {label}
          </button>
        ))}
      </nav>
      <div className="min-h-[420px] p-5">
        <TabContent tab={activeTab} result={result} form={form} />
      </div>
    </section>
  );
}

function TabContent({ tab, result, form }) {
  if (tab === "query") {
    return <><h2 className="mb-3 text-lg font-semibold">布林檢索式</h2><CodeBlock>{result.query || form.query}</CodeBlock></>;
  }

  if (tab === "keywords") {
    const matrix = result.matrix || form.matrix || defaultMatrix();
    return (
      <>
        <h2 className="mb-3 text-lg font-semibold">矩陣分析關鍵字</h2>
        <div className="grid gap-5 xl:grid-cols-2">
          <KeywordColumn title="技術分析" items={matrix.technologies || []} />
          <KeywordColumn title="功效分析" items={matrix.efficacies || []} />
        </div>
      </>
    );
  }

  const figure = result.figures?.[tab];
  if (!figure) {
    return <p className="text-amber-300">找不到圖表</p>;
  }
  return <PlotlyChart figure={figure} />;
}

function PlotlyChart({ figure }) {
  const chartRef = useRef(null);
  const [error, setError] = useState("");
  const [plotly, setPlotly] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    let loadedPlotly = null;
    const node = chartRef.current;
    setError("");
    setReady(false);
    loadPlotly()
      .then((Plotly) => {
        loadedPlotly = Plotly;
        if (!cancelled && node) {
          const layout = {
            ...(figure.layout || {}),
            autosize: true,
            paper_bgcolor: "#0f172a",
            plot_bgcolor: "#111827",
            font: {
              family: "Microsoft JhengHei, Segoe UI, Arial, sans-serif",
              color: "#e5e7eb",
              ...((figure.layout || {}).font || {})
            }
          };
          setPlotly(Plotly);
          return Plotly.react(node, figure.data || [], layout, {
            responsive: true,
            displaylogo: false,
            scrollZoom: false
          }).then(() => {
            if (!cancelled) setReady(true);
          });
        }
        return null;
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err?.message || String(err));
        }
      });
    return () => {
      cancelled = true;
      if (loadedPlotly && node) {
        try {
          loadedPlotly.purge(node);
        } catch {
          // Plotly can throw during rapid tab switches; the DOM node is already leaving.
        }
      }
    };
  }, [figure]);

  function downloadImage() {
    if (!plotly || !chartRef.current) return;
    plotly.toImage(chartRef.current, {
      format: "png",
      width: 1200,
      height: 800,
      scale: 2
    }).then((url) => {
      const link = document.createElement("a");
      link.href = url;
      link.download = "專利分析圖表.png";
      link.click();
    }).catch((err) => {
      setError(err?.message || String(err));
    });
  }

  return (
    <>
      {error && <p className="mb-3 text-sm text-red-300">圖表渲染失敗：{error}</p>}
      <button className="mb-3 rounded-md border border-white/10 bg-slate-800 px-3 py-2 text-sm font-semibold text-slate-100 hover:bg-slate-700 disabled:cursor-progress disabled:opacity-50" onClick={downloadImage} disabled={!ready}>
        下載圖表 PNG
      </button>
      <div ref={chartRef} className="min-h-[420px] rounded-md bg-slate-950" />
    </>
  );
}

function MatrixEditor({ title, items, onChange, labelPrefix }) {
  const fixedItems = fillSix(items);
  function update(index, key, value) {
    const next = fixedItems.map((item, i) => i === index ? { ...item, [key]: value } : item);
    onChange(next);
  }

  return (
    <div>
      <h3 className="mb-3 text-base font-semibold">{title}</h3>
      <div className="grid gap-2">
        {fixedItems.map((item, index) => (
          <div key={index} className="grid gap-2 sm:grid-cols-[minmax(110px,1fr)_3fr]">
            <input className="input" value={item.label} onChange={(e) => update(index, "label", e.target.value)} placeholder={`${labelPrefix} ${index + 1}`} />
            <textarea className="input min-h-24" value={item.boolean} onChange={(e) => update(index, "boolean", e.target.value)} placeholder={`布林式 ${index + 1}`} />
          </div>
        ))}
      </div>
    </div>
  );
}

function KeywordColumn({ title, items }) {
  return (
    <div>
      <h3 className="mb-3 text-base font-semibold">{title}</h3>
      <div className="grid gap-2">
        {items.map((item, index) => (
          <div key={index} className="grid gap-2 sm:grid-cols-[1fr_3fr]">
            <CodeBlock>{item.label}</CodeBlock>
            <CodeBlock>{item.boolean}</CodeBlock>
          </div>
        ))}
      </div>
    </div>
  );
}

function CodeBlock({ children }) {
  return <pre className="max-h-80 overflow-auto whitespace-pre-wrap break-words rounded-md border border-white/10 bg-slate-950/70 p-3 text-sm text-slate-200">{children || ""}</pre>;
}

function Modal({ title, children, onClose, wide = false }) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/70 p-4">
      <div className={`max-h-[90vh] w-full overflow-auto rounded-lg border border-white/10 bg-slate-900 p-5 text-slate-100 shadow-2xl shadow-black/50 ${wide ? "max-w-6xl" : "max-w-2xl"}`}>
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="text-xl font-semibold">{title}</h2>
          <button className="rounded-md border border-white/10 bg-slate-800 px-3 py-1.5 text-slate-200 hover:bg-slate-700" onClick={onClose}>關閉</button>
        </div>
        {children}
      </div>
    </div>
  );
}

function defaultForm() {
  return {
    topic_select: "自訂",
    topic: "",
    gpss_id: "",
    gpss_pw: "",
    gemini_api_key: "",
    login_mode: "自動辨識驗證碼",
    search_mode: "搜尋布林檢索式",
    matrix_mode: "關鍵字規則 (Rule-based)",
    query: "",
    source: "",
    conf_source: "",
    matrix: defaultMatrix(),
    name: "",
    student_id: ""
  };
}

function mapDefaults(defaults) {
  return {
    topic: defaults.topic || "",
    gpss_id: defaults.gpss_id || "",
    gpss_pw: defaults.gpss_pw || "",
    gemini_api_key: defaults.gemini_api_key || "",
    name: "",
    student_id: "",
    login_mode: "自動辨識驗證碼",
    search_mode: defaults.search_mode || "搜尋布林檢索式",
    matrix_mode: defaults.matrix_mode || "關鍵字規則 (Rule-based)",
    query: defaults.query || "",
    source: defaults.source || "",
    conf_source: defaults.conf_source || "",
    matrix: normalizeMatrix(defaults.matrix || defaultMatrix())
  };
}

function defaultMatrix() {
  return { technologies: [], efficacies: [] };
}

function normalizeMatrix(matrix) {
  return {
    technologies: fillSix(matrix?.technologies || []),
    efficacies: fillSix(matrix?.efficacies || [])
  };
}

function fillSix(items) {
  const next = Array.from({ length: 6 }, (_, index) => ({
    label: items[index]?.label || "",
    boolean: items[index]?.boolean || ""
  }));
  return next;
}

function compactItems(items) {
  return fillSix(items).filter((item) => item.label && item.boolean).slice(0, 6);
}

function messageClass(level, isCompletedInfo = false) {
  if (isCompletedInfo) return "text-emerald-300";
  if (level === "success") return "text-emerald-300";
  if (level === "warning") return "text-amber-300";
  if (level === "error") return "text-red-300";
  return "text-slate-300";
}

function messageLabel(level, isCompletedInfo = false, isCurrent = false) {
  if (isCurrent) return "進行中";
  if (isCompletedInfo || level === "success") return "完成";
  if (level === "warning") return "注意";
  if (level === "error") return "錯誤";
  return level;
}

function downloadPdf(pdf) {
  const binary = atob(pdf);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i);
  }
  const blob = new Blob([bytes], {
    type: "application/pdf"
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "智財分析報告.pdf";
  link.click();
  URL.revokeObjectURL(url);
}

let plotlyPromise = null;
function loadPlotly() {
  if (!plotlyPromise) {
    plotlyPromise = import("plotly.js-dist-min").then((module) => module.default || module);
  }
  return plotlyPromise;
}

createRoot(document.getElementById("root")).render(<App />);
