import streamlit as st
import csv
from io import StringIO
from pathlib import Path
import json
from csv_profiler.profiling import basic_profile
from csv_profiler.render import write_markdown

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → profile → export JSON + Markdown")
st.sidebar.header("Inputs")

rows = None
report = st.session_state.get("report")

uploaded = st.file_uploader("Upload a CSV", type=["csv"])
show_preview = st.sidebar.checkbox("Show preview", value=True)

if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

if rows is not None and len(rows) > 0:
    if show_preview:
        st.subheader("Preview")
        st.write(rows[:5])

    if st.button("Generate report"):
        st.session_state["report"] = basic_profile(rows)
else:
    st.info("Upload a CSV to begin.")

report = st.session_state.get("report")

if report is not None:
    cols = st.columns(2)
    cols[0].metric("Rows", report.get("n_rows", 0))
    cols[1].metric("Columns", report.get("n_cols", 0))

    st.subheader("Columns")
    st.write(report["columns"])

    md_path = Path("outputs/temp_report.md")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    write_markdown(report, md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    with st.expander("Markdown preview", expanded=False):
        st.code(md_text, language="markdown")

    report_name = st.sidebar.text_input("Report name", value="report")
    json_file = report_name + ".json"
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    md_file = report_name + ".md"
    md_path_final = Path("outputs") / md_file
    write_markdown(report, md_path_final)

    c1, c2 = st.columns(2)
    c1.download_button("Download JSON", data=json_text, file_name=json_file)
    c2.download_button("Download Markdown", data=open(md_path_final, "r", encoding="utf-8").read(), file_name=md_file)

    if st.button("Save to outputs/"):
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / json_file).write_text(json_text, encoding="utf-8")
        (out_dir / md_file).write_text(open(md_path_final, "r", encoding="utf-8").read(), encoding="utf-8")
        st.success(f"Saved {json_file} & {md_file} in outputs/")
