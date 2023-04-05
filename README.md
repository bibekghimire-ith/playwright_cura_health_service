# playwright_cura_health_service
pytest-playwright project for the Cura Health Service demo site
<hr>
<hr>
<br>
<br>

### Step 1: Create a new project and install required packages
```sh
# Configuration of playwright
pip3 install playwright
pip3 install pytest-palywright
playwright install

pip3 install pytest
pip3 install pytest-html     ### HTML Reporter
pip3 install pytest-xdist    ### Run tests in parallel
pip3 install openpyxl
```
<br>
<hr>
<br>

### Step 2: Create Folder Structure
- Configurations/
    - config.conf
- Logs/
- pageObjects/
    - __init__.py
    - loginPage.py
- Reports/
- Screenshots/
- testCases/
    - __init__.py
    - conftest.py
    - test_login.py
- testData/
    - login_data.xlsx
- utilities/
    - __init__.py
    - customLogger.py
    - ExcelUtils.py
    - readConfig.py
- pytest.ini
- requirements.txt
- README.md
<br>
<br>
<hr>
<br>

### Step 3: Automating first testcase (login)
1. Create LoginPage object class under "pageObjects" directory, i.e. "pageObjects/loginPage.py"
2. Create testcase for login in folder "testCase", i.e. "testCase/test_login.py"

**Note:** Since, pytest is used:
* testcase filename should be in format `test_{testcase}.py`
* test function should be in format `test_{test_name}_testCaseID()` => e.g. `test_valid_login_TC0001()`
<br>

### Sample LoginPage object
```py
# pageObjects/loginPage.py
from playwright.sync_api import Page

class LoginPage:
    url = "https://katalon-demo-cura.herokuapp.com/"
    # Locators 
    textbox_username_id = '#txt-username'
    textbox_password_id = '#txt-password'
    btn_login_id = '#btn-login'

    # Initiating locators
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_field = self.page.locator(self.textbox_username_id)
        self.password_field = self.page.locator(self.textbox_password_id)
        self.login_btn = self.page.locator(self.btn_login_id)

    def load_loginPage(self) -> None:
        url = self.url + "profile.php#login"
        self.page.goto(url)
    
    def login(self, user: dict) -> None:
        self.username_field.fill(user["username"])
        self.password_field.fill(user["password"])
        self.login_btn.click()

```
<br>

### Sample login test case
```py
# testCases/test_login.py
import pytest
from pageObjects.loginPage import LoginPage   # Importing LoginPage object from the pageObjects/loginPage
from playwright.sync_api import expect, Page

class TestLogin:
    user = {
            "username": "John Doe",
            "password": "ThisIsNotAPassword"
        }

    def test_valid_login_TC001(self, page: Page) -> None:
        # Initializing the login_page variable
        login_page = LoginPage(page)
        login_page.load_loginPage()
        
        login_page.login(self.user)
        actual_title = page.inner_text("h2")
        expected_title = "Make Appointment"
        if actual_title == expected_title:
            assert True
        else:
            assert False
```
<br>
<hr>
<br>

### Step 4: Capture screenshot on failure
*Update testcases to take screenshots on failure.*
Syntax for taking screenshot: `page.screenshot(path="./Screenshots/test_failed.png", full_page=True)`
=> Screenshot can have extenstions png, jpg, and jpeg.
<br>

**Updated "test_valid_login_TC001" test:**
```py
def test_valid_login_TC001(self, page: Page) -> None:
        # Initializing the login_page variable
        login_page = LoginPage(page)
        login_page.load_loginPage()
        
        login_page.login(self.user)
        actual_title = page.inner_text("h2")
        expected_title = "Make Appointment"
        if actual_title == expected_title:
            assert True
        else:
            page.screenshot(path="./Screenshots/test_valid_login.png_TC001", full_page=True)
            assert False
```
<br>
<hr>
<br>

### Step 5: Reading common values from config file
1. Create "config.conf" file in folder "Configurations"
2. Create "readConfig.py" file under "utilities" package to read common data from config file
3. Replace hardcoded values in pageObjects and test cases
<br>

**config.conf file**
```conf
[common fields]
baseURL = https://katalon-demo-cura.herokuapp.com/
username = John Doe
password = ThisIsNotAPassword
```
<br>

**readConfig.py file**
```python
from configparser import RawConfigParser, ConfigParser

config = ConfigParser()
config.read("./Configurations/config.conf")

class ReadConfig:
    @staticmethod
    def getApplicationURL() -> str:
        url = config.get("common fields", "baseURL")
        return url   
    ...
```
<br>

**Updated login testcase:**
```py
# testCases/test_login.py
import pytest
from pageObjects.loginPage import LoginPage   # Importing LoginPage object from the pageObjects/loginPage
from playwright.sync_api import expect, Page
from utilities.readConfig import ReadConfig   # Importing utility file for reading config data

class TestLogin:
    user = {
            "username": ReadConfig.getUsername(), # Reading username from config file
            "password": ReadConfig.getPassword()  # Reading password from config file
        }

    def test_valid_login_TC001(self, page: Page) -> None:
        # Initializing the login_page variable
        login_page = LoginPage(page)
        login_page.load_loginPage()
        
        login_page.login(self.user)
        actual_title = page.inner_text("h2")
        expected_title = "Make Appointment"
        if actual_title == expected_title:
            assert True
        else:
            page.screenshot(path="./Screenshots/test_valid_login.png_TC001", full_page=True)
            assert False
```
<br>
<hr>
<br>

### Step 6: Adding custom logs to test cases 
1. Create "customLogger.py" file under utilities package
2. Configuring logger and adding logs to the test cases
<br>

**customLogger.py file**
```py
import logging
import datetime

class customLogen:
    now = datetime.datetime.now()
    current_date = now.strftime("%Y_%m_%d_T%H:%M:%S")
    log_file = f"./Logs/automation_{current_date}.log"

    def customLogger(self, logger_name: str, log_level=logging.DEBUG):
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        # Create console/file handler and set the log level
        file_handler = logging.FileHandler(filename=self.log_file, mode="a")
        # Create formatter - how you want your logs to be formatted
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        # Add formatter to console of file handler
        file_handler.setFormatter(formatter)
        # Add console handler to logger
        logger.addHandler(file_handler)

        return logger
```
<br>

**Updated login test with logger configured:**
```py
# testCases/test_login.py
import pytest
from pageObjects.loginPage import LoginPage   # Importing LoginPage object from the pageObjects/loginPage
from playwright.sync_api import expect, Page
from utilities.readConfig import ReadConfig   # Importing utility file for reading config data

class TestLogin:
    user = {
            "username": ReadConfig.getUsername(), # Reading username from config file
            "password": ReadConfig.getPassword()  # Reading password from config file
        }
    # Logger initialization...
    loggen = customLogen()

    def test_valid_login_TC001(self, page: Page) -> None:
        logger = self.loggen.customLogger("test_valid_login_TC001", logging.INFO)
        logger.info("Starting test 'test_valid_login_TC001'")

        # Initializing the login_page variable
        login_page = LoginPage(page)
        login_page.load_loginPage()
        
        login_page.login(self.user)
        actual_title = page.inner_text("h2")
        expected_title = "Make Appointment"
        if actual_title == expected_title:
            logger.info("Test 'test_002_valid_login' passed")
            assert True
        else:
            logger.error('Test "test_002_valid_login" failed')
            page.screenshot(path="./Screenshots/test_valid_login.png_TC001", full_page=True)
            assert False
        logger.info("Completed test 'test_002_valid_login'")
```
<br>
<hr>
<br>

### Step 7: Adding command line arguments used while running tests to **pytest.ini** file
**Note:** `pytest.ini` file should be in root directory
```ini
[pytest]
addopts = --browser firefox --headed
```
**Running tests:**
`pytest`

*Running particular test in firefox browser:* `pytest -s -v testCases/test_login.py --browser firefox`

*Running tests in parallel:* `pytest -s -v -n=3 testCases/test_login.py --browser chrome`

**Note:** n=3 (maximum)
<br>
<hr>
<br>

### Step 8: Generating HTML reports
Installing *pytest-html* package: `pip3 install pytest-html`
`pytest --html=Reports/report.html`
<br>

**Fixture can be added in `conftest.py` so that the report name can be generated uniquely each time the test is run**
```py
# testCases/conftest.py

# Fixture for "pytest-html" report configuration
import datetime

@pytest.fixture(scope="session")
def pytest_html_report_title(request):
    """
    Set the title of the report
    """
    return "CURA HEALTH SERVICE Test Report"

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
```
<br>
<hr>
<br>

### Step 9: Automating Data Driven tests
1. Prepare test data in excel sheet, and place it in TestData folder.
2. Create `ExcelUtils.py` utility class under utilities package.
3. Create LoginDataDrivenTest under testCases.
<br>

**Format of test data in excel file:**

`Username | Password | Exp (Pass/Fail)`
<br>

**ExcelUtils.py file to read data from excel file:**
```py
import openpyxl

def getRowCount(file, sheetName) -> int:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook[sheetName]
    return (sheet.max_row)

def getColumnCount(file, sheetName) -> int:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook[sheetName]
    return (sheet.max_column)

def readData(file, sheetName, rowNum, colNum) -> str:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook[sheetName]
    data = sheet.cell(row=rowNum, column=colNum).value
    return "" if data == None else data

def writeData(file, sheetName, rowNum, colNum, data) -> None:
    workbook = openpyxl.load_workbook(file)
    sheet = workbook[sheetName]
    sheet.cell(row=rowNum, column=colNum).value = data
    workbook.save(file)
```
<br>

**Sample Data Driven test:**
```py
def test_login_DDT_TC002(self, page: Page) -> None:
    login_page = LoginPage(page)
    login_page.load_loginPage()

    sheetName = "InvalidCreds"
    rows = ExcelUtils.getRowCount(self.file_path, sheetName)
    status = []

    for row in range(2, rows+1):
        self.user["username"] = ExcelUtils.readData(self.file_path, sheetName, row, 1)
        self.user["password"] = ExcelUtils.readData(self.file_path, sheetName, row, 2)
        expected_error_msg = ExcelUtils.readData(self.file_path, sheetName, row, 3)
        
        login_page.login(self.user)
        text_error_xpath = "p.lead.text-danger"
        actual_error_msg = page.inner_text(text_error_xpath)

        if expected_error_msg == actual_error_msg:
            status.append("Pass")
        else:
            status.append("Fail")
        
    # Checks
    if "Fail" not in status:
        assert True
    else:
        assert False
```
<br>
<hr>
<br>

### Step 10: Add other tests, e.g. logout, appointment, etc.
<br>
<hr>
<br>

### Step 11: Grouping Tests
**Marking tests and classes**
```sh
Examples: https://www.lambdatest.com/blog/end-to-end-tutorial-for-pytest-fixtures-with-examples/ 
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.skip   ##### Skip test
@pytest.mark.run(order=1)      ##### Marking test run order
```
=> For ordering execution/run of tests, `pip3 install pytest-ordering`
<br>

**Running Tests with markers:**
```sh
pytest -m smoke
pytest -m "not regression"
pytest -m "smoke and regression"
pytest -m "smoke or regression"      #### Runs test with either of the markers
```
<br>

**Configuring `pytest.ini` file for markers:**
```ini
[pytest]
markers = 
    smoke: mark a test as a smoke test
    regression: mark a test as a regression test
addopts = --browser firefox -m smoke
```
<br>
<hr>
<br>

### Step 12: Run tests in command line or create bash script
`pytest -s -v -m "sanity" --html=./Reports/report.html testCases/`
<br>
<hr>
<hr>
<br>

### Best Practices:
1. **Use clear and descriptive class names:** e.g. **TestLoginPage**
2. **Use clear and descriptive function names:** For example, if you're testing the login functionality, you could create a function called **"test_valid_login_TC001"**, where TC001 is test case id.
3. **Use fixtures to set up test data:** Use fixtures to set up test data that is required for multiple tests. This will help keep your tests organized and reduce duplication of code.
4. **Use markers to categorize tests:** Use markers to categorize your tests into groups such as smoke tests, regression tests, and integration tests.
5. **Use assertions:** Use assertions to check the expected results of your tests. This will help you identify issues and quickly fix them. 
6. **Use good coding practices:** Follow good coding practices such as writing clean code, commenting your code, and keeping your tests small and focused.
7. **Use test data files:** Use test data files to store test data that is required for your tests. This will help keep your tests organized and reduce duplication of code.
8. **Use parameterized tests:** Use parameterized tests to test different scenarios with the same test code. This will help reduce duplication of code and make your tests more efficient.
9. **Use logging and reporting:** Use logging and reporting to help you identify issues and track your test results. This will help you quickly fix issues and improve the quality of your tests.
<hr>