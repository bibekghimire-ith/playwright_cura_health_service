# TODO: Logout flow
# GO Back (<-) action should redirect to login page
# Test: should not be able to access "Make Appointment Page"
import pytest
from playwright.sync_api import expect, Page
from pageObjects.loginPage import LoginPage
from utilities.readConfig import ReadConfig

import logging
from utilities.customLogger import customLogen

logen = customLogen()
logger = logen.customLogger("test_logout", logging.INFO)

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
    

    def test_logout_TC008(self, page: Page, setup_login) -> None:
        login = setup_login
        logger.info("Started test 'test_logout_TC008'")
        # login = LoginPage(page)
        # login.load_loginPage()
        # login.login(self.user)

        # page = setup_teardown_login

        if "appointment" in page.url:
            page.locator(self.link_toggle_id).click()
            try:
                page.locator(self.link_logout_xpath).wait_for()
                page.locator(self.link_logout_xpath).click()
                expect(page).to_have_url(self.baseURL)
                logger.info("Test 'test_logout_TC008' passed")
                # assert page.locator(self.btn_bookAppointment_id).is_visible()
            except Exception as e:
                # Add Exception insted of assertion
                logger.exception(e)
                logger.error("Test 'test_logout_TC008' failed")
                assert False
        else:
            # log error "Login Failed"
            logger.error("Test 'test_logout_TC008' failed")
            # Take screenshot
            page.screenshot(path="./Report/Screenshots/test_logout_TC008.png", full_page=True)
            assert False
        logger.info("Completed test 'test_logout_TC008'")

    # Failing test case..
    def test_navigate_back_TC009(self, page: Page) -> None:
        """After logging out, if back arrow of browser is clicked, page should not be router to "Appointment Page"
            TC Steps:
            1. Login 
            2. Logout
            3. Click page back arrow (<-) of browser
        Args:
            page (Page): _description_
        """
        logger.info("Started test 'test_navigate_back_TC009'")
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
                logger.info("Test 'test_navigate_back_TC009' passed")
                assert True
            else:
                # log error
                logger.error("Test 'test_navigate_back_TC009' failed")
                # Take screenshot
                page.screenshot(path="./Report/Screenshots/test_navigate_back_TC009.png", full_page=True)
                assert False
        except Exception as e:
            logger.exception(e)
            logger.error("Test 'test_navigate_back_TC009' failed")
            logger.info("Completed test 'test_navigate_back_TC009'")
            # Take screenshot
            page.screenshot(path="./Report/Screenshots/test_navigate_back_TC009_exception.png", full_page=True)
            assert False
        logger.info("Completed test 'test_navigate_back_TC009'")
        