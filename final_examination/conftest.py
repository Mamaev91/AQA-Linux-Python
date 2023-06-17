from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pytest
import yaml


with open("testdata.yaml") as f2:
    user_set = yaml.safe_load(f2)


@pytest.fixture(scope="session")
def browser():
    service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture()
def login():
    response = requests.post(user_set['url'], data={'user': user_set['user'], 'passwd': user_set['passwd']})
    response.encoding = 'utf-8'
    return response.json()['token']


@pytest.fixture()
def answer_code():
    return "32px"