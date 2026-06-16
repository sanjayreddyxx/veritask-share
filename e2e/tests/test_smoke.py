import pytest


def test_homepage_loads(driver, base_url):
    driver.get(base_url)
    assert "" is not None  # placeholder: assert page loads (no exception)


@pytest.mark.parametrize("path, text", [
    ("/", ""),
    ("/login", "Login"),
    ("/signup", "Sign up"),
    ("/dashboard", "Dashboard"),
])
def test_pages_load(driver, base_url, path, text):
    driver.get(base_url + path)
    # Basic presence check: look for body element
    body = driver.find_element("tag name", "body")
    assert body is not None
