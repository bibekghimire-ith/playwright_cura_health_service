# TC010 : Tokyo CURA Healthcare Center, apply for hospital readmission, medicare, 14/2/2020, this a comment
#  : tokyo,  do not apply for hospital readmission, none, 5/3/2020, this a comment
#  : Seoul CURA Healthcare Center, apply for hospital readmission, medcare, 20/5/2019, this a comment
#  : Hongkong CURA Healthcare Center, do not apply for hospital readmission, medicaid, 5/8/2022, this a comment

    
import pytest
from playwright.sync_api import expect, Page
from pageObjects.appointmentPage import AppointmentPage
from pageObjects.loginPage import LoginPage
from utilities.readConfig import ReadConfig

import logging
from utilities.customLogger import customLogen

class TestAppointmentPage:
    baseURL = ReadConfig.getApplicationURL()
    appointmentPageURL = f"{baseURL}/#appointment"
    user ={
            "username": ReadConfig.getUsername(),
            "password": ReadConfig.getPassword()
        }
    # logger initialization
    loggen = customLogen()
    
    @pytest.mark.regression
    def test_createAppointment_TC010(self, page: Page) -> None:
        logger = self.loggen.customLogger("test_createAppointment_TC010", logging.INFO)
        logger.info('Starting Test "test_createAppointment_TC010"')
        login = LoginPage(page)
        login.load_loginPage()
        login.login(self.user)

        test_data = [{"facility_value":"Tokyo CURA Healthcare Center","readmission":"True","noneProgram":"False","medicareProgram":"True","medicaidProgram":"False","visitDate":"14/2/2020","comment":"Tokyo CURA Healthcare Center"},{"facility_value":"Tokyo CURA Healthcare Center","readmission":"False","noneProgram":"True","medicareProgram":"False","medicaidProgram":"False","visitDate":"5/3/2020","comment":"Tokyo CURA Healthcare Center 2"},{"facility_value":"Seoul CURA Healthcare Center","readmission":"True","noneProgram":"False","medicareProgram":"True","medicaidProgram":"False","visitDate":"20/5/2019","comment":"Seoul CURA Healthcare Center"},{"facility_value":"Hongkong CURA Healthcare Center","readmission":"False","noneProgram":"False","medicareProgram":"False","medicaidProgram":"True","visitDate":"5/8/2022","comment":"Hongkong CURA Healthcare Center"}]
        result = []
        # test_data = [{"facility_value":"Hongkong CURA Healthcare Center","readmission":"False","noneProgram":"False","medicareProgram":"False","medicaidProgram":"True","visitDate":"","comment":"Hongkong CURA Healthcare Center"}]

        # test_data = [{"facility_value":"Tokyo CURA Healthcare Center","readmission":"True","noneProgram":"False","medicareProgram":"True","medicaidProgram":"False","visitDate":"14/2/2020","comment":"Tokyo CURA Healthcare Center"},{"facility_value":"Tokyo CURA Healthcare Center","readmission":"False","noneProgram":"True","medicareProgram":"False","medicaidProgram":"False","visitDate":"5/3/2020","comment":"Tokyo CURA Healthcare Center 2"},{"facility_value":"Seoul CURA Healthcare Center","readmission":"True","noneProgram":"False","medicareProgram":"True","medicaidProgram":"False","visitDate":"20/5/2019","comment":"Seoul CURA Healthcare Center"},{"facility_value":"Hongkong CURA Healthcare Center","readmission":"False","noneProgram":"False","medicareProgram":"False","medicaidProgram":"True","visitDate":"5/8/2022","comment":"Hongkong CURA Healthcare Center"}]
        i = 1
        for data in test_data:
            page.goto(self.appointmentPageURL)
            appointment = AppointmentPage(page)
            # page.pause()
            appointment.create_appointment(data)
            # Conformation page
            if page.inner_text("h2") == "Appointment Confirmation":
                logger.info(f'Test passed for data: {data}')
                result.append("Pass")
            else:
                # Take screenshot on fail
                logger.error(f'Test failed for data: {data}')
                # TODO: image path needs to be updated. For this, "id" field should be added in the test_data and same should be concatenated 
                # to the image path
                image_path = f"./Report/Screenshots/test_createAppointment_TC010_{i}.png"
                page.screenshot(path=image_path, full_page=True)
                result.append("Fail")
            i = i + 1
        # page.pause()
        if "Fail" not in result:
            logger.info('Test "test_createAppointment_TC010" passed')
            assert True
        else:
            logger.error('Test "test_createAppointment_TC010" failed')
            assert False
        logger.info('Test "test_createAppointment_TC010" completed')

    @pytest.mark.regression
    def test_appointment_conformation_TC011(self, page: Page) -> None:
        logger = self.loggen.customLogger("test_appointment_conformation_TC011")
        logger.info('Test "test_appointment_conformation_TC011" started')

        login = LoginPage(page)
        login.load_loginPage()
        login.login(self.user)

        # result = []
        test_data = {"facility_value":"Hongkong CURA Healthcare Center","readmission":"False","noneProgram":"False","medicareProgram":"False","medicaidProgram":"True","visitDate":"05/08/2022","comment":"Hongkong CURA Healthcare Center"}
        

        page.goto(self.appointmentPageURL)
        appointment = AppointmentPage(page)
        # page.pause()
        appointment.create_appointment(test_data)
        # Conformation page
        if page.inner_text("h2") == "Appointment Confirmation":
            expect(page.locator("p.lead")).to_have_text("Please be informed that your appointment has been booked as following:")
            conformation_details = {}
            conformation_details["facility_value"] = page.inner_text('p#facility')
            conformation_details["readmission"] = page.inner_text('p#hospital_readmission')
            conformation_details["program"] = page.inner_text('p#program')
            conformation_details["visitDate"] = page.inner_text('p#visit_date')
            conformation_details["comment"] = page.inner_text('p#comment')
            program = ""
            for key, value in test_data.items():
                if key == "noneProgram" and value == "True":
                    program = "None"
                elif key == "medicareProgram" and value == "True":
                    program = "Medicare"
                elif key == "medicaidProgram" and value == "True":
                    program = "Medicaid"
            # page.pause()
            assert conformation_details["facility_value"] == test_data["facility_value"]
            assert conformation_details["readmission"] == "Yes" if test_data["readmission"]=="True" else "No"
            assert conformation_details["visitDate"] == test_data["visitDate"]
            assert conformation_details["comment"] == test_data["comment"]
            assert conformation_details["program"] == program
            logger.info('Test "test_appointment_conformation_TC011" passed')
        else:
            # log error "Failed to create appointment"
            logger.warning("Failed to create appointment")
            logger.error('Test "test_appointment_conformation_TC011" failed')
            # Take screenshot on fail
            page.screenshot(path="./Report/Screenshots/test_appointment_conformation_TC011.png", full_page=True)
            assert False
        logger.info('Test "test_appointment_conformation_TC011" completed')