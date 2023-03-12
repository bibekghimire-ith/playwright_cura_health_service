from playwright.sync_api import Page
from utilities.readConfig import ReadConfig

class LoginPage:
    url = ReadConfig.getApplicationURL()
    # Locators 
    textbox_username_id = '#txt-username'
    textbox_password_id = '#txt-password'
    btn_login_id = '#btn-login'

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_field = self.page.locator(self.textbox_username_id)
        self.password_field = self.page.locator(self.textbox_password_id)
        self.login_btn = self.page.locator(self.btn_login_id)

    def load_loginPage(self) -> None:
        url = self.url + "profile.php#login"
        self.page.goto(url)

    def navigate_login(self) -> None:
        self.page.goto(self.url)
        self.page.wait_for_load_state()
        self.page.wait_for_selector('id=menu-toggle').click()
        self.page.locator("a", has_text="Login").click()
    
    def login(self, user: dict) -> None:
        self.username_field.fill(user["username"])
        self.password_field.fill(user["password"])
        self.login_btn.click()
