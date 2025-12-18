import json
from pathlib import Path
import typer

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import basic_profile as profile_rows
from csv_profiler.render import write_markdown as render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    try:
        rows = read_csv_rows(input_path)
    except FileNotFoundError:
        typer.echo(f"Error: file not found: {input_path}")
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    report = profile_rows(rows)

    md_content = render_markdown(report)

    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / f"{report_name}.json"
    with open(json_path, "w", encoding="utf8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    md_path = out_dir / f"{report_name}.md"
    with open(md_path, "w", encoding="utf8") as f:
        f.write(md_content)

    if preview:
        typer.echo(f"Rows: {report['n_rows']}, Columns: {report['n_cols']}")
        for col in report["columns"]:
            typer.echo(f"- {col}: type={report['columns'][col]['type']}, missing={report['columns'][col]['stats'].get('missing', 0)}")

    typer.echo(f"Report saved: {json_path} and {md_path}")

if __name__ == "__main__":
    app()
