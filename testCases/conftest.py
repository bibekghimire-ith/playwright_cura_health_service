from playwright.sync_api import expect, Page
from utilities.readConfig import ReadConfig
import pytest

# Default pytest fixture is function...
# ! Better not to use fixtures with pytest-playwright
@pytest.fixture(scope="function")
def setup_teardown(page: Page) -> None:
    from pageObjects.loginPage import LoginPage
    login_page = LoginPage(page)
    login_page.load_loginPage()
    yield page


# pytest-playwright provides fixtures by default
# -> "page" fixture covers most of the functionality required
# https://www.lambdatest.com/blog/end-to-end-tutorial-for-pytest-fixtures-with-examples/
@pytest.fixture()
def setup_login(page: Page) -> None:
    from pageObjects.loginPage import LoginPage
    username = ReadConfig.getUsername()
    password = ReadConfig.getPassword()

    user = {
        "username": username,
        "password": password
    }

    login_page = LoginPage(page)
    login_page.load_loginPage()
    login_page.login(user)
    
    yield login_page
    page.close()


# Fixture for "pytest-html" report configuration
import datetime


@pytest.fixture(scope="session")
def pytest_html_report_title(request):
    """
    Set the title of the report
    """
    return "CURA HEALTH SERVICE Test Report"


# @pytest.fixture(scope="session")
def pytest_html_results_summary(prefix, summary, postfix):
    """
    Add a timestamp to the report summary
    """
    prefix.extend([f"<h4>Report generated at {datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}</h4>"])


def pytest_html_report_title(report):
    """
    Modify the report title to include a timestamp
    """
    report.title = f"CURA HEALTH SERVICE Test Report: ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"


def pytest_configure(config):
    """
    Add a unique identifier to the pytest-html report filename
    """
    config.option.htmlpath = f"./Reports/smoke_test_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.html"