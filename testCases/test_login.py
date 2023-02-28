import pytest
from pageObjects.loginPage import LoginPage
from playwright.sync_api import expect, Page
from utilities import ExcelUtils

class TestLogin:
    """ This class includes TCs for all login scenarios
    """
    file_path = "./testData/login_data.xlsx"
    user = {
            "username": "John Doe",
            "password": "ThisIsNotAPassword"
        }
    
    # def test_navigate_to_loginPage(self, page: Page) -> None:
    #     """ Navigate to login page from homepage

    #     Args:
    #         page (Page): Page object
    #     """
    #     login_page = LoginPage()
    #     login_page.navigate_login()


    # def test_001_login_UI(self, page: Page) -> None:
    #     login_page = LoginPage(page)
        
    #     login_page.navigate_login()

    #     # Verify login page
    #     expect(page).to_have_title("CURA Healthcare Service")
    #     assert "login" in page.url
    #     assert page.inner_text("h2") == "Login"

    #     # Verify form-field labels
    #     expect(page.locator('//label[contains(@for,"txt-username")]')).to_have_text("Username")
    #     expect(page.locator('//label[@for="txt-password"]')).to_have_text("Password")
    #     expect(page.locator('#btn-login')).to_have_attribute("type", "submit")
    #     expect(page.locator('#btn-login')).to_have_text("Login")

    #     # Verify Placeholders
    #     expect(page.locator('//input[@id="txt-username"]')).to_have_attribute("placeholder", "Username")
    #     # expect(page.locator('//input[@id="txt-password"]')).to_have_attribute("placeholder", "Password")
    #     assert page.locator('//input[@id="txt-password"]').get_attribute("placeholder") == "Password"

    # def test_valid_login(page: Page, login_page: LoginPage) -> None:
    # def test_002_valid_login(self, page: Page) -> None:
    #     login_page = LoginPage(page)
        
    #     login_page.load_loginPage()
        
    #     login_page.login(self.user)
    #     # assert page.inner_text("h2") == "Make Appointment"
    #     actual_title = page.inner_text("h2")
    #     expected_title = "Make Appointment"
    #     if actual_title == expected_title:
    #         # logger info -> login pass
    #         assert True
    #     else:
    #         # logger error -> login fail
    #         # Take screenshot
    #         assert False

    # def test_003_invalid_login(self, page: Page) -> None:
    #     """_summary_

    #     Args:
    #         page (Page): _description_
    #     """
    #     # Use ddt for Invalid login checks:=> username, password, message, status(pass/fail)

    #     login_page = LoginPage(page)
    #     login_page.load_loginPage()

    #     sheetName = "InvalidCreds"
    #     rows = ExcelUtils.getRowCount(self.file_path, sheetName)
    #     status = []

    #     for row in range(2, rows+1):
    #         self.user["username"] = ExcelUtils.readData(self.file_path, sheetName, row, 1)
    #         self.user["password"] = ExcelUtils.readData(self.file_path, sheetName, row, 2)
    #         expected_error_msg = ExcelUtils.readData(self.file_path, sheetName, row, 3)
    #         test_desc = ExcelUtils.readData(self.file_path, sheetName, row, 5)
            
    #         login_page.login(self.user)
    #         text_error_xpath = "p.lead.text-danger"
    #         actual_error_msg = page.inner_text(text_error_xpath)

    #         if expected_error_msg == actual_error_msg:
    #             # log msg
    #             status.append("Pass")
    #         else:
    #             # log test_desc Test failed
    #             # Take screenshot
    #             status.append("Fail")
    #     # Checks
    #     if "Fail" not in status:
    #         # log info Test passed
    #         assert True
    #     else:
    #         # log infor Test failed
    #         assert False

    
    def test_004_login_input_validation(self, page: Page) -> None:
        """ Verify validation messages for empty field, char length, other validation

        Args:
            page (Page): _description_
        """
        # inputValidation
        login_page = LoginPage(page)
        login_page.load_loginPage()

        sheetName = "inputValidation"
        rows = ExcelUtils.getRowCount(self.file_path, sheetName)
        status = []

        # page.pause()
        for row in range(2, rows+1):
            self.user["username"] = ExcelUtils.readData(self.file_path, sheetName, row, 1)
            self.user["password"] = ExcelUtils.readData(self.file_path, sheetName, row, 2)
            expected_error_msg = ExcelUtils.readData(self.file_path, sheetName, row, 3)
            test_desc = ExcelUtils.readData(self.file_path, sheetName, row, 5)
            
            login_page.login(self.user)
            text_error_xpath = "p.lead.text-danger"
            actual_error_msg = page.inner_text(text_error_xpath)

            if expected_error_msg == actual_error_msg:
                # log msg
                status.append("Pass")
            else:
                # log test_desc Test failed
                # Take screenshot
                status.append("Fail")
        # Checks
        if "Fail" not in status:
            # log info Test passed
            assert True
        else:
            # log infor Test failed
            assert False

    # def test_005_login_security(self, page: Page) -> None:
    #     """ Verify limit of unsuccessful login attempts to prevent Brute-force attacks
    #         Verify "invalid username or password is displayed" for invalid credentials, instead of exact message, such as "invalid username is displayed"
    #         Check the duration of the login session timeout. Once a user is in, they can’t be verified for a lifetime.
    #         Make sure that when users are logged in and click the back button, they aren’t logged out.

    #     Args:
    #         page (Page): _description_
    #     """
    #     # loginSecurity

    def test_006_if_password_field_masked(self, page: Page) -> None:
        """ Check if password entered is displayed as "*" instead of actual string

        Args:
            page (Page): _description_
        """
        login_page = LoginPage(page)
        
        login_page.navigate_login()
        expect(page.locator('//input[@id="txt-password"]')).to_have_attribute("type", "password")

    
    def test_007_access_dashboard_without_login(self, page: Page) -> None:
        """_summary_

        Args:
            page (Page): _description_
        """
        page.goto("https://katalon-demo-cura.herokuapp.com/#appointment")
        btn_bookAppointment_id = "#btn-book-appointment"
        check = page.locator(btn_bookAppointment_id).is_visible(timeout=40000)
        if check == False:
            # Page is not navigated to Appointment page
            # Test passed
            assert True
        else:
            # log error
            assert False