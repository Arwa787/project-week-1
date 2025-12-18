#  CSV Profiler

Generate a profiling report for a CSV file.

# Features
- CLI: JSON + Markdown report
- Streamlit GUI: upload CSV + export reports

# Setup
uv venv -p 3.11
uv pip install -r requirements.txt
# Run CLI
  -# If you have a src/ folder:
  -#   Mac/Linux: export PYTHONPATH=src
  -#   Windows:   $env:PYTHONPATH="src"
uv run python -m csv_profiler.cli profile data/sample.csv --out-dir outputs

# Run GUI
  -# If you have a src/ folder:
  -#   Mac/Linux: export PYTHONPATH=src
  -#   Windows:   $env:PYTHONPATH="src"
   uv run streamlit run app.py

# Output Files
  The CLI writes:- `outputs/report.json`- `outputs/report.md`
  The Streamlit app can:- preview the report
   download JSON + Markdown   