from playwright.sync_api import expect, Page

class AppointmentPage:
    # Locators
    select_facilityCenter_id = "#combo_facility"
    checkbox_hospitalReadmission_xpath = '//input[@id="chk_hospotal_readmission"]'
    radio_medicareProgram_id = "#radio_program_medicare"
    radio_medicaidProgram_id = "#radio_program_medicaid"
    radio_noneProgram_id = "#radio_program_none"
    input_visitDate_id = "#txt_visit_date"
    textarea_comment_id = "#txt_comment"
    btn_bookAppointment_id = "#btn-book-appointment"

    def __init__(self, page: Page) -> None:
        self.page = page
    
    def create_appointment(self, data: dict) -> None:
        self.page.locator(self.select_facilityCenter_id).select_option(value=data.get("facility_value"))
        if data.get("readmission", "False") == "True":
            self.page.locator(self.checkbox_hospitalReadmission_xpath).check()
        else:
            self.page.locator(self.checkbox_hospitalReadmission_xpath).uncheck()
        if data.get("medicareProgram", False) == "True":
            self.page.locator(self.radio_medicareProgram_id).check()
        elif data.get("medicaidProgram",False) == "True":
            self.page.locator(self.radio_medicaidProgram_id).check()
        elif data.get("noneProgram",False) == "True":
            self.page.locator(self.radio_noneProgram_id).check()
        # self.page.locator(self.input_visitDate_id).click()
        # self.page.locator(self.input_visitDate_id).fill(data.get("visitDate"))
        self.page.get_by_placeholder("dd/mm/yyyy").click()
        self.page.get_by_placeholder("dd/mm/yyyy").type(data.get("visitDate"))
        self.page.locator(self.textarea_comment_id).click()
        self.page.locator(self.textarea_comment_id).fill(data.get("comment", ""))
        self.page.locator(self.btn_bookAppointment_id).click()
        