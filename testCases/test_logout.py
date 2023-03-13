# TODO: Logout flow
# GO Back (<-) action should redirect to login page
# Test: should not be able to access "Make Appointment Page"
import pytest
from playwright.sync_api import expect, Page
from pageObjects.loginPage import LoginPage
from utilities.readConfig import ReadConfig

class TestLogout:
    # Locators
    link_toggle_id = "#menu-toggle"
    link_logout_xpath = '//a[@href="authenticate.php?logout"]'
    btn_bookAppointment_id = "#btn-book-appointment"

    baseURL = ReadConfig.getApplicationURL()
    user = {
            "username": ReadConfig.getUsername(),
            "password": ReadConfig.getPassword()
        }
    
    def test_logout_TC008(self, page: Page) -> None:
        login = LoginPage(page)
        login.load_loginPage()
        login.login(self.user)

        if "appointment" in page.url:
            page.locator(self.link_toggle_id).click()
            try:
                page.locator(self.link_logout_xpath).wait_for()
                page.locator(self.link_logout_xpath).click()
                expect(page).to_have_url(self.baseURL)
                # assert page.locator(self.btn_bookAppointment_id).is_visible()
            except Exception as e:
                # Add Exception insted of assertion
                assert False
        else:
            # log error "Login Failed"
            # Take screenshot
            page.screenshot(path="./Report/Screenshots/test_logout_TC008.png", full_page=True)
            assert False

    def test_navigate_back_TC009(self, page: Page) -> None:
        """After logging out, if back arrow of browser is clicked, page should not be router to "Appointment Page"
            TC Steps:
            1. Login 
            2. Logout
            3. Click page back arrow (<-) of browser
        Args:
            page (Page): _description_
        """
        login = LoginPage(page)
        login.load_loginPage()
        login.login(self.user)

        # Logout
        page.locator(self.link_toggle_id).click()
        page.locator(self.link_logout_xpath).wait_for()
        page.locator(self.link_logout_xpath).click()

        try: 
            page.go_back()
            expect(page).to_have_url(self.baseURL)
            btn_bookAppointment_id = "#btn-book-appointment"
            check = page.locator(btn_bookAppointment_id).is_visible(timeout=40000)
            if check == False:
                # Page is not navigated to Appointment page
                # Test passed
                assert True
            else:
                # log error
                # Take screenshot
                page.screenshot(path="./Report/Screenshots/test_navigate_back_TC009.png", full_page=True)
                assert False
        except Exception as e:
            print(e)
        