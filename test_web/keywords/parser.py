import yaml
import csv

def parse_yaml(file_path):
    """
    Parses a YAML test file and returns a list of test steps.
    Each step is a dict with 'keyword' and 'args' keys.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Validate that 'data' is a list of dicts and contains required keys
    if not isinstance(data, list):
        raise ValueError("YAML test file should contain a list of steps")
    for step in data:
        if "keyword" not in step:
            raise ValueError("Each step must have 'keyword'")
        if "args" not in step:
            # Ensure args is at least empty list if missing
            step["args"] = []
    return data


def parse_csv(file_path):
    """
    Parses a CSV test file and returns a list of test steps.
    Expected CSV format: columns 'keyword', 'arg1', 'arg2', ...
    Converts each row into dict with 'keyword' and 'args' list.
    """
    steps = []
    with open(file_path, "r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "keyword" not in row or not row["keyword"]:
                # Skip empty or malformed rows
                continue
            keyword = row["keyword"].strip()
            args = []
            for i in range(1, 20):  # assume max 20 args max
                key = f"arg{i}"
                # Check row[key] is not None before stripping
                if key in row and row[key] is not None and row[key].strip() != "":
                    args.append(row[key].strip())
                else:
                    break
            steps.append({"keyword": keyword, "args": args})
    return steps
