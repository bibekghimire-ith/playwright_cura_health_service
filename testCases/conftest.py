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