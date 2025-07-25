import pytest
import os
import json
import shutil
import allure
import getpass
import socket
import datetime
import subprocess
from pathlib import Path
from playwright.sync_api import Playwright

# =============== Pytest CLI Options ===============
def pytest_addoption(parser):
    parser.addoption("--hidden", action='store_true', default=False)
    parser.addoption("--runZap", action='store_true', default=False)
    parser.addoption("--add_video", action='store_true', default=False)
    parser.addoption(
        "--custom-browser",
        action='store',
        default="chromium",
        help="Browser to run tests on: chromium, chrome, firefox, webkit"
    )

# =============== Helper for Git Info ===============
def get_git_info():
    """Fetches current Git branch and short commit hash."""
    branch, commit = "unknown", "unknown"
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=os.getcwd()).decode().strip()
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=os.getcwd()).decode().strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass # Git not found or not a git repo
    return branch, commit

# =============== Parallel Browser ===============

def pytest_configure(config):
    """Configure pytest for parallel browser execution"""
    if not hasattr(config, 'workerinput'):
        custom_browser = config.getoption("custom_browser")
        if custom_browser:
            config._browser_queue = [custom_browser]
        else:
            config._browser_queue = ['chromium', 'firefox', 'webkit', 'chrome']

def pytest_configure_node(node):
    """Configure each worker node with a specific browser"""
    if hasattr(node.config, '_browser_queue') and node.config._browser_queue:
        browser = node.config._browser_queue.pop(0)
        node.workerinput['browser'] = browser
        print(f"Worker {node.gateway.id if hasattr(node, 'gateway') else 'main'} assigned browser: {browser}")


# =============== Allure Environment, Executors, Trend, Categories ===============

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    allure_results = os.path.join(os.getcwd(), 'allure-results')
    os.makedirs(allure_results, exist_ok=True)

    # --- Environment Info ---
    raw_browser = session.config.getoption('custom_browser')
    browser = raw_browser.upper() if raw_browser else "CHROMIUM"

    os_name = os.name
    os_display = "WINDOWS" if os_name == "nt" else "LINUX" if os_name == "posix" else os_name.upper()

    python_version = os.sys.version.split()[0]

    env_path = os.path.join(allure_results, 'environment.properties')
    with open(env_path, 'w') as f:
        f.write(f"BROWSER={browser}\n")
        f.write(f"OS={os_display}\n")
        f.write(f"PYTHON_VERSION={python_version}\n")
        f.write(f"TEST_ENV=QA\n") # Example custom field

    # --- Executors Info ---
    branch, commit = get_git_info()
    executor_info = {
        "name": getpass.getuser(),
        "type": "manual",
        "url": "",
        "buildOrder": int(datetime.datetime.now().timestamp()),
        "buildName": f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}",
        "buildUrl": "",
        "reportUrl": "",
        "branch": branch,
        "commit": commit
    }
    exec_path = os.path.join(allure_results, 'executor.json')
    with open(exec_path, 'w') as f:
        json.dump(executor_info, f, indent=4)

    # --- Custom Categories ---
    categories = [
        {
            "name": "Product Defects",
            "matchedStatuses": ["failed"],
            "messageRegex": ".*failed for a known bug.*",
            "description": "Tests failing due to actual product bugs."
        },
        {
            "name": "Test Environment Issues",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*(connection|timeout|environment|setup).*",
            "description": "Tests broken due to issues with the test environment."
        },
        {
            "name": "Test Infrastructure Flaky",
            "matchedStatuses": ["broken"],
            "messageRegex": ".*(element not found|stale element|network error).*",
            "description": "Tests broken due to flaky infrastructure or transient errors."
        },
        {
            "name": "Other Issues",
            "matchedStatuses": ["failed", "broken", "skipped"]
        }
    ]
    categories_path = os.path.join(allure_results, 'categories.json')
    with open(categories_path, 'w') as f:
        json.dump(categories, f, indent=4)

    # --- Trend/History ---
    prev_report_history_path = os.path.join(os.getcwd(), 'allure-report', 'history')
    current_results_history_path = os.path.join(allure_results, 'history')

    if os.path.exists(prev_report_history_path) and os.path.isdir(prev_report_history_path):
        print(f"Copying previous history from {prev_report_history_path} to {current_results_history_path}")
        if os.path.exists(current_results_history_path):
            shutil.rmtree(current_results_history_path)
        shutil.copytree(prev_report_history_path, current_results_history_path)
    else:
        print("No previous Allure report history found. Trends will be generated from the next run.")

# =============== Playwright Fixtures ===============


@pytest.fixture(scope="session")
def browser_name(request):
    if hasattr(request.config, 'workerinput'):
        return request.config.workerinput.get('browser', 'chromium')
    else:
        return request.config.getoption("custom_browser")


@pytest.fixture(scope="function")
def browser(playwright: Playwright, request, browser_name):
    hidden = request.config.getoption("hidden")
    runZap = request.config.getoption("runZap")
    launch_args = ['--no-sandbox', '--disable-setuid-sandbox']

    if runZap:
        launch_args.append('--ignore-certificate-errors')
    proxy = {"server": 'localhost:8080'} if runZap else None

    print(f" Launching {browser_name} browser...")

    if browser_name == "chrome":
        chrome_path = shutil.which("chrome") or shutil.which("google-chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if not os.path.exists(chrome_path):
            raise Exception(f"Chrome not found at {chrome_path}. Add it to PATH or check path.")
        browser = playwright.chromium.launch(
            headless=hidden,
            args=launch_args,
            executable_path=chrome_path,
            proxy=proxy
        )
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(
            headless=hidden,
            args=launch_args,
            proxy=proxy
        )
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(
            headless=hidden,
            args=launch_args,
            proxy=proxy
        )
    else:  # chromium (default)
        browser = playwright.chromium.launch(
            headless=hidden,
            args=launch_args,
            proxy=proxy
        )

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser, request, browser_name):
    storage_path = "test.json"
    add_video = request.config.getoption("add_video")

    context_args = {}
    if os.path.exists(storage_path):
        try:
            with open(storage_path, 'r') as f:
                json.load(f)
            context_args["storage_state"] = storage_path
        except json.JSONDecodeError:
            print(f"⚠️ Invalid JSON in {storage_path}. Ignoring.")

    if add_video:
        video_dir = f"videos/{browser_name}/"
        os.makedirs(video_dir, exist_ok=True)
        context_args["record_video_dir"] = video_dir

    context = browser.new_context(**context_args)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.set_default_timeout(60000)
    page.goto("https://www.amazon.in", wait_until="domcontentloaded")

    yield page

    trace_path = f"traces/{browser_name}/test_{request.node.name}.zip"
    os.makedirs(os.path.dirname(trace_path), exist_ok=True)
    context.tracing.stop(path=trace_path)
    page.close()
    context.close()

# =============== Allure Metadata: Browser & Worker ===============

@pytest.fixture(autouse=True)
def add_browser_and_worker_info(request, browser_name):
    # Add browser label/marker
    if hasattr(request.node, 'add_marker'):
        request.node.add_marker(pytest.mark.browser(browser_name))
    # Add Allure labels for browser, worker, and process id
    worker_id = getattr(request.config, "workerinput", {}).get("workerid", "master")
    allure.dynamic.label("browser", browser_name)
    allure.dynamic.label("worker", worker_id)
    allure.dynamic.label("pid", str(os.getpid()))

# =============== Allure Screenshot Attachments ===============

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_path = screenshot_dir / f"{item.nodeid.replace('::', '_')}.png"
            if not page.is_closed():
                try:
                    page.screenshot(path=screenshot_path)
                    allure.attach.file(
                        str(screenshot_path),
                        name="screenshot",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as e:
                    print(f"Warning: Could not take screenshot for {item.nodeid}: {e}")
