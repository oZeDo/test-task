import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def memory_cell():
    yield {'phone': None, 'rating': None, 'number_of_phones': None}


@pytest.fixture(scope='module')
def browser():
    opts = Options()
    opts.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/10"
                      "5.0.0.0 Safari/537.36")
    opts.add_argument("--disable-blink-features")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=opts)
    chrome_driver.maximize_window()

    yield chrome_driver
    chrome_driver.close()


@pytest.fixture
def actions(browser):
    actions = ActionChains(browser)
    return actions
