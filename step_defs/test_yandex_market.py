from pytest_bdd import scenarios, given, when, then
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
import time

YANDEX_MARKET_URL = 'https://market.yandex.ru/'
scenarios('../feature/yandex_market.feature')


@given("the yandex market page is opened")
def yandex_market_home(browser):
    browser.get(YANDEX_MARKET_URL)
    timeout = 60  # Время ожидания загрузки страницы, может появится капча
    logging.warning('Возможно появление капчи')
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//span[text()="Каталог"]'))
        WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        raise Exception("Timed out waiting for page to load")


@when("I select the category 'Электроника'")
def select_category(browser, actions):
    catalog = browser.find_element(By.CSS_SELECTOR, '#catalogPopupButton')
    actions.move_to_element(catalog).click().perform()
    time.sleep(3)

    category_xpath = '//div[@data-apiary-widget-name="@MarketNode/HeaderCatalog"]//ul//span[text()="Электроника"]'
    category = browser.find_element(By.XPATH, category_xpath)
    actions.move_to_element(category).perform()
    time.sleep(3)


@when("I select the subcategory 'Смартфоны'")
def select_subcategory(browser, actions):
    subcategory = browser.find_element(By.CSS_SELECTOR, "a[href*='/catalog--smartfony/']")
    actions.move_to_element(subcategory).click().perform()
    time.sleep(3)


@then("page with the subcategory 'Смартфоны' is opened")
@given("page with the subcategory 'Смартфоны' is opened")
def check_page_category(browser):
    assert 'Смартфоны' in browser.title


@when("I click on the 'Все фильтры' button")
def select_all_filters(browser, actions):
    all_filters = browser.find_element(By.XPATH, '//span[text()="Все фильтры"]')
    # browser.execute_script("arguments[0].scrollIntoView();", all_filters)
    # time.sleep(1)
    all_filters.click()
    time.sleep(2)


@then("the 'Все фильтры' page is opened")
@given("the 'Все фильтры' page is opened")
def check_page_title(browser):
    assert 'Все фильтры' in browser.title


@when("I set the max price filter to '20000 roubles'")
def set_price(browser):
    browser.implicitly_wait(3)
    price_input = browser.find_element(By.XPATH, '//div[@data-prefix="до"]//input')
    price_input.send_keys('20000')
    time.sleep(3)


@when("I set the minimal screen size filter to '3 inches'")
def set_screen_size(browser):
    button = browser.find_element(By.XPATH, "//h4[starts-with(text(), 'Диагональ экрана (точно)')]/..")
    browser.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    time.sleep(3)
    screen_size_input = browser.find_elements(By.XPATH, '//div[@data-prefix="от"]//input')[1]
    time.sleep(3)
    screen_size_input.send_keys('3')


@then("the max price filter is set to '20000 roubles'")
@given("the max price filter is set to '20000 roubles'")
def check_price(browser):
    price_input = browser.find_element(By.XPATH, '//div[@data-prefix="до"]//input').get_attribute("value")
    assert price_input == '20000'


@then("the minimal screen size filter is set to '3 inches'")
@given("the minimal screen size filter is set to '3 inches'")
def check_screen_size(browser):
    screen_size_input = browser.find_elements(By.XPATH, '//div[@data-prefix="от"]//input')[1].get_attribute("value")
    assert screen_size_input == '3'


@when("I select 5 different manufacturers")
def select_manufactures(browser, actions):
    table = browser.find_element(By.XPATH, "//h4[text()='Производитель']/../../div/div[@data-tid]/div[@data-tid]")
    browser.execute_script("arguments[0].scrollIntoView();", table)
    manufacturers = table.find_elements(By.XPATH, "./div")
    for manufacturer in manufacturers[:5]:
        checkbox = manufacturer.find_element(By.XPATH, "./label")
        actions.move_to_element(checkbox).click().perform()
        time.sleep(3)


@then("5 different manufacturers are selected")
@given("5 different manufacturers are selected")
def check_manufacturers_selection(browser):
    table = browser.find_element(By.XPATH, "//h4[text()='Производитель']/../../div/div[@data-tid]/div[@data-tid]")
    manufacturers = table.find_elements(By.XPATH, "./div")
    for manufacturer in manufacturers[:5]:
        checkbox = manufacturer.find_element(By.XPATH, "./label/input")
        assert checkbox.is_selected()
        browser.implicitly_wait(3)


@when("I click on the 'Показать' button")
def press_apply(browser, actions):
    links = browser.find_element(By.XPATH, "//a[text()='Отменить и вернуться']/..")
    time.sleep(3)
    apply_button = links.find_element(By.XPATH, "./a[2]")
    actions.move_to_element(apply_button).click().perform()
    time.sleep(3)


@then("the 'Смартфоны' page is opened")
@given("the filtered page is opened")
def check_filtered_page(browser):
    assert 'Смартфоны' in browser.title


@when("I count the number of phones")
def count_phones(actions, browser, memory_cell):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    phones = browser.find_elements(By.XPATH, "//article")
    memory_cell['number_of_phones'] = len(phones)


@then("the number of phones is printed to the console")
def log_number_of_phones(memory_cell):
    logging.info(f'Количество телефонов на странице: {memory_cell["number_of_phones"]}')


@when("I remember the name of the last phone")
def remember_last_phone(browser, memory_cell):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    phones = browser.find_elements(By.XPATH, "//article")
    browser.execute_script("arguments[0].scrollIntoView();", phones[-1])
    memory_cell["phone"] = phones[-1].find_element(By.XPATH, ".//span").text
    logging.info(f'Последний телефон в списке: {phones[-1].find_element(By.XPATH, ".//span").text}')
    time.sleep(3)


@then("the name of last phone is saved to the memory")
def check_last_phone_in_memory(browser, memory_cell):
    assert memory_cell["phone"] is not None


@when("I change the sorting to 'по рейтингу'")
def change_sorting(browser, actions):
    button = browser.find_element(By.XPATH, "//button[text()='по рейтингу']")
    actions.move_to_element(button).click().perform()
    time.sleep(3)


@then("the sorting is changed to 'по рейтингу'")
@given("the page is sorted by 'по рейтингу'")
def check_sorting(browser):
    button = browser.find_element(By.XPATH, "//button[text()='по рейтингу']")
    assert button.is_enabled() is False


@when("I search for the remembered phone on the page by name")
def search_phone(actions, browser, memory_cell):
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        try:
            phone = browser.find_element(By.XPATH, f"//span[text()='{memory_cell['phone']}']")
            break
        except NoSuchElementException:
            next_page = browser.find_element(By.XPATH, "//span[text()='Вперёд']")
            actions.move_to_element(next_page).click().perform()
            time.sleep(3)
        except Exception as e:
            raise e


@then("the remembered phone is found")
def find_the_phone(actions, browser, memory_cell):
    phone = browser.find_element(By.XPATH, f"//span[text()='{memory_cell['phone']}']/..")
    browser.execute_script("arguments[0].scrollIntoView();", phone)
    time.sleep(3)


@then("I click on the remembered phone")
def click_on_the_phone(actions, browser, memory_cell):
    phone = browser.find_element(By.XPATH, f"//span[text()='{memory_cell['phone']}']/..")
    # не работает, т.к. элемент не кликабен через selenium
    # actions.move_to_element(phone).click().perform()
    # phone.click()
    browser.execute_script("arguments[0].click();", phone)
    time.sleep(3)


@given("the remembered phone is found")
@when("I save raing of the remembered phone")
def save_rating(browser, memory_cell):
    try:
        memory_cell['rating'] = browser.find_element(By.XPATH, "//span[@data-auto='rating-badge-value']").text
    except NoSuchElementException:
        pass


@then("the rating is printed to the console")
def log_rating(browser, memory_cell):
    logging.info(f'Рейтинг телефона: {memory_cell["rating"]}')

