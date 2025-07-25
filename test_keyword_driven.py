import pytest
from test_executor import execute_test_case

@pytest.mark.smoke
def test_TC001(page):
    execute_test_case('TC001', page)

@pytest.mark.smoke
def test_TC002(page):
    execute_test_case('TC002', page)

@pytest.mark.smoke
def test_TC003(page):
    execute_test_case('TC003', page)

@pytest.mark.regression
def test_TC004(page):
    execute_test_case('TC004', page)

@pytest.mark.regression
def test_TC005(page):
    execute_test_case('TC005', page)

@pytest.mark.regression
def test_TC006(page):
    execute_test_case('TC006', page)

@pytest.mark.order(7)
def test_TC007(page):
    execute_test_case('TC007', page)

@pytest.mark.order(8)
def test_TC008(page):
    execute_test_case('TC008', page)
