def basic_profile(rows: list[dict[str, str]]) -> dict:
    result = {}

    row_count = len(rows)

    if row_count == 0:
        return {
            "rows": 0,
            "columns": {}
        }

    columns = list(rows[0].keys())
    columns_info = {}

    for col in columns:
        missing = 0
        values = []

        for row in rows:
            value = row[col].strip()
            if value == "":
                missing += 1
            else:
                values.append(value)

        col_type = "number"
        for v in values:
            try:
                float(v)
            except ValueError:
                col_type = "text"
                break

        columns_info[col] = {
            "missing": missing,
            "type": col_type
        }

    result["rows"] = row_count
    result["columns"] = columns_info

    return result 

MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]


def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))
    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": (sum(nums) / count) if count else None,
    }

def text_stats(values: list[str], top_k: int = 5) -> dict:
    """Compute count, missing, unique, and top_k most common values."""
    
    usable = [v for v in values if not is_missing(v)]
    
    missing = sum(1 for v in values if is_missing(v))
    
    unique = len(set(usable))
    
    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
    
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    
    return {
        "count": len(values),
        "missing": missing,
        "unique": unique,
        "top": top
    }

