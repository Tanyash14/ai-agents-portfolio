import ollama
from pydantic import BaseModel
from enum import Enum
from collections import Counter


# ---------- Schema definitions ----------

class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Category(str, Enum):
    AIRFLOW = "airflow"
    SPARK = "spark"
    DBT = "dbt"
    API_INGESTION = "api_ingestion"
    PERMISSIONS = "permissions"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


class LogClassification(BaseModel):
    severity: Severity
    category: Category
    likely_cause: str
    needs_immediate_action: bool


# ---------- Core logic ----------

def classify_log_line(log_line: str) -> LogClassification:
    """Send ONE log line to the model and get back a structured object."""
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "user", "content": f"Classify this log line: {log_line}"}
        ],
        format=LogClassification.model_json_schema(),
    )
    return LogClassification.model_validate_json(response["message"]["content"])


def main():
    # Step 1: read the real file from disk, line by line
    with open("sample_logs.txt", "r") as f:
        log_lines = f.readlines()

    print(f"Loaded {len(log_lines)} log lines.\n")

    # Step 2: pre-filter -- only send ERROR lines to the LLM (Day 1 cost lesson)
    error_lines = [line for line in log_lines if "ERROR" in line]
    print(f"Filtered down to {len(error_lines)} ERROR lines (skipped INFO/WARNING to save tokens).\n")

    # Step 3: classify only the filtered lines
    results = []
    for line in error_lines:
        classification = classify_log_line(line.strip())
        results.append((line.strip(), classification))
        print(f"✓ Classified: {classification.severity} | {classification.category}")

    # Step 4: print a simple summary report
    print("\n=== Daily Incident Summary ===")
    action_needed = [r for line, r in results if r.needs_immediate_action]
    print(f"Total errors processed: {len(results)}")
    print(f"Requiring immediate action: {len(action_needed)}")
    for line, r in results:
        flag = "🚨" if r.needs_immediate_action else "  "
        print(f"{flag} [{r.category.value}] {r.likely_cause}")

    # Step 5: aggregate counts by category -- only reliable because
    # category is now an Enum, not free text
    print("\n=== Errors by Category ===")
    category_counts = Counter(r.category for line, r in results)
    for cat, count in category_counts.most_common():
        print(f"{cat.value}: {count}")


if __name__ == "__main__":
    main()
