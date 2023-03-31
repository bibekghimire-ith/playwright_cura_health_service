*Generated by CHAT-GPT*
### pytest-html report
To generate a pytest-html report with a unique name, you can use the --html command line option along with a filename that includes a unique identifier. One way to generate a unique identifier is to use the current date and time.
`pip3 install pytest-html`

Here is an example implementation that generates a unique filename for the pytest-html report:
```
import pytest
import datetime


@pytest.fixture(scope="session")
def pytest_html_report_title(request):
    """
    Set the title of the report
    """
    return "My Test Report"


@pytest.fixture(scope="session")
def pytest_html_results_summary(prefix, summary, postfix):
    """
    Add a timestamp to the report summary
    """
    prefix.extend([f"<h4>Report generated at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h4>"])


def pytest_html_report_title(report):
    """
    Modify the report title to include a timestamp
    """
    report.title = f"My Test Report ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"


def pytest_configure(config):
    """
    Add a unique identifier to the pytest-html report filename
    """
    config.option.htmlpath = f"reports/pytest_html_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
```
=> So, the filename for your fixture file should be conftest.py. This file should be placed in a directory that is on the Python module search path, usually at the root of your project or in a directory that contains your test files.

This implementation includes the following changes:

    A **pytest_html_report_title** fixture is defined to set the title of the report.
    A **pytest_html_results_summary** fixture is defined to add a timestamp to the report summary.
    A **pytest_html_report_title** hook is defined to modify the report title to include a timestamp.
    A **pytest_configure** hook is defined to add a unique identifier to the pytest-html report filename.

With these changes, each time you run your tests, a new pytest-html report will be generated with a filename that includes a timestamp. The report title and summary will also include a timestamp.

To run your tests and generate the report, simply run:
`pytest --html=reports/pytest_html_report.html`
*Not required -> fixture added works*

This will generate a pytest-html report with a filename that includes a timestamp, in the reports directory.