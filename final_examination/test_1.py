import yaml
import time
from TestPage import OperationsHelper
import logging

with open("testdata.yaml") as f:
    testdata = yaml.safe_load(f)


def test_step1(browser, answer_code):
    logging.info("Test 1 Starting")
    test_page = OperationsHelper(browser)
    test_page.go_to_site()
    test_page.enter_login(testdata["user"])
    test_page.enter_pass(testdata["passwd"])
    test_page.click_login_button()
    test_page.click_about_button()
    time.sleep(3)
    field = test_page.get_about_page_font()
    assert field == answer_code