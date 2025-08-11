import pytest
from playwright.sync_api import sync_playwright
import allure
import socket
import getpass
from datetime import datetime
import os

# -------------------
# Playwright fixtures
# -------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)  # ➡️ set True in CI
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

# -------------------
# Allure hooks & env info
# -------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """
    Wrap each test call in an Allure step with test name, user, and timestamp.
    """
    test_name = item.name
    user = getpass.getuser()
    with allure.step(f"Test: {test_name} | Run by: {user} | Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"):
        yield


def pytest_configure(config):
    """
    Creates an Allure environment.properties file with run info.
    """
    user = getpass.getuser()
    hostname = socket.gethostname()

    env_dir = os.path.join(os.getcwd(), 'allure-results')
    os.makedirs(env_dir, exist_ok=True)
    env_file_path = os.path.join(env_dir, 'environment.properties')

    with open(env_file_path, 'w') as f:
        f.write(f"User={user}\n")
        f.write(f"Run Timestamp={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
