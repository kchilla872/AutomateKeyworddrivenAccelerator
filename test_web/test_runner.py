import pytest
import yaml
from playwright.sync_api import Page
from test_web.keywords.actions import KeywordActions

def load_test_steps(yaml_file_path):
    with open(yaml_file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_steps(actions, steps):
    for step in steps:
        keyword = step.get("keyword")
        args = step.get("args", [])
        print(f"\n=== Executing keyword: {keyword} with args: {args} ===")
        if not hasattr(actions, keyword):
            pytest.fail(f"Keyword '{keyword}' not implemented in KeywordActions.")
        method = getattr(actions, keyword)
        try:
            method(*args)
        except Exception as e:
            pytest.fail(f"Step failed: keyword={keyword}, args={args}\nException: {e}")


def test_keyword_execution(page: Page):
    test_files = [
        "test_web/data/login_search_checkout.yml"
    ]
    actions = KeywordActions(page)
    for test_file in test_files:
        steps = load_test_steps(test_file)
        run_steps(actions, steps)
