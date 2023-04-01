# playwright_cura_health_service
pytest-playwrigh project for the Cura Health Service demo site







# Grouping Tests
**Marking tests and classes**
```
Exapmles: https://www.lambdatest.com/blog/end-to-end-tutorial-for-pytest-fixtures-with-examples/ 
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.skip   ##### Skip test
@pytest.mark.run(order=1)      ##### Marking test run order
```
=> For ordering execution/run of tests, `pip3 install pytest-ordering`

**Running Tests with markers:**
```
pytest -m smoke
pytest -m "not regression"
pytest -m "smoke and regression"
pytest -m "smoke or regression"      #### Runs test with either of the markers
```