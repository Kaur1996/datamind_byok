# 🧠 DataMind

**Turn raw data into business insights in seconds.**

DataMind is an AI-powered data analysis tool that takes any CSV dataset and returns ranked, actionable business insights with confidence scores — plus auto-generated Plotly visualizations to support them. No SQL, no dashboards, no data science degree required.

🔗 **[Live Demo](#)** *(add your Hugging Face Space URL here once deployed)*

---

## What It Does

Upload a CSV, and DataMind will:

1. **Profile your data** — row/column counts, data types, null percentages, and smart categorical/numeric classification
2. **Generate 10 ranked insights** — each with a business category, supporting numeric evidence, a concrete recommendation, and an LLM confidence score
3. **Auto-generate 3–5 charts** — the LLM decides which chart types (bar, line, histogram, scatter) and column pairings best support the insights it found

Tested on datasets as different as retail sales (Superstore, 21 columns) and survival data (Titanic, 12 columns) — the pipeline adapts its analysis to whatever structure it's given.

---

## Demo

| Insights View | Charts View |
|---|---|
| 10 ranked insight cards with recommendations and confidence scores | Auto-generated Plotly charts matched to the dataset's structure |

*(Add screenshots here)*

---

## Architecture

```
CSV Upload
    │
    ▼
file_router.py       → detects file type (CSV/PDF), extracts filename
    │
    ▼
csv_processor.py      → statistical profiling: dtypes, nulls, groupby aggregations
    │
    ▼
insight_engine.py     → LLM generates 10 ranked insights (JSON)
    │
    ▼
chart_engine.py        → LLM selects chart types + column mappings (JSON)
    │
    ▼
chart_renderer.py     → renders Plotly figures from chart config
    │
    ▼
app.py (Streamlit UI) → displays insight cards + interactive charts
```

Each stage is a single-responsibility module — the router only detects file type, the processor only computes statistics, the insight engine only talks to the LLM for insights, and so on. This makes the pipeline easy to test in isolation and easy to extend (e.g. adding a PDF processor without touching anything else).

---

## Tech Stack

| Component | Choice |
|---|---|
| LLM | Anthropic Claude / Google Gemini |
| Data processing | pandas, numpy |
| Visualization | Plotly Express |
| UI | Streamlit |
| Deployment | Hugging Face Spaces |

---

## Key Engineering Decisions

**Why pass a statistical summary to the LLM instead of raw data?**
Context window limits and cost. A CSV with tens of thousands of rows can't fit in a prompt — a statistical summary captures the signal (distributions, categorical breakdowns, outliers) without the noise.

**Why groupby aggregations, not just `.describe()`?**
Raw summary statistics (mean, std) produce generic insights. Category-level and region-level aggregations let the LLM make specific, evidence-backed claims — e.g. *"Technology has 9x the average profit of Furniture"* — instead of vague generalities.

**Why LLM-chosen chart types instead of hardcoded charts?**
The chart engine acts as a planner: it reads the dataset's columns and the insights already generated, then decides which chart type and column pairing best visualizes each finding. This means the same code works on a 21-column sales dataset and a 12-column survival dataset without modification.

**Why is "confidence" an LLM confidence score, not a statistical one?**
It's explicitly qualitative — how strongly the visible data supports a claim — not a p-value or margin of error. This is labeled clearly in the UI to avoid misleading users into thinking it's a formal statistical measure.

**Why isolate insight generation and chart generation into separate try/except blocks?**
Failure isolation. If the LLM returns malformed chart configuration, the user should still see their 10 insights rather than the entire app breaking. Each pipeline stage fails independently and shows a clear, specific error message rather than crashing the whole page.

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Kaur1996/datamind.git
cd datamind

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key(s) to a .env file
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# Run the app
streamlit run app.py
```

---

## Project Status

✅ Core pipeline complete (file routing → stats → insights → charts → UI)
✅ Tested end-to-end on multiple dataset structures
🔧 PDF support — planned
🔧 Conversational follow-up layer — planned

---

## Author

**Kavleen Kaur** — [GitHub](https://github.com/Kaur1996)

Built as a portfolio project to demonstrate LLM application engineering: prompt design for structured JSON output, statistical data profiling, and building resilient multi-stage pipelines around unpredictable LLM outputs.
