import json
import os
import re
import pytest


HERE = os.path.dirname(__file__)
TC_FILE = os.path.join(HERE, "..", "testcases.json")


def load_cases():
    with open(os.path.abspath(TC_FILE), "r", encoding="utf-8") as f:
        return json.load(f)


cases = load_cases()


def extract_path(steps: str):
    m = re.search(r"BASE_URL(/[^\s>]*)", steps)
    if m:
        return m.group(1)
    return "/"


@pytest.mark.parametrize("case", cases, ids=[f"TC{c['id']}" for c in cases])
def test_case(driver, base_url, case):
    path = extract_path(case.get("steps", ""))
    url = base_url.rstrip("/") + path
    try:
        driver.get(url)
        body = driver.find_element("tag name", "body")
        assert body is not None
    except Exception as e:
        pytest.fail(f"TC{case['id']} failed navigating to {url}: {e}")
