import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "http://localhost:5000")


@pytest.fixture(scope="session")
def driver():
    opts = Options()
    # run headless by default for CI
    if os.environ.get("HEADLESS", "1") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1366,768")

    driver = webdriver.Chrome(options=opts)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
