Feature: Yandex market
  Tests for the 'https://market.yandex.ru/' page

  Scenario: Select the category and subcategory
    Given the yandex market page is opened
    When I select the category 'Электроника'
    And I select the subcategory 'Смартфоны'
    Then page with the subcategory 'Смартфоны' is opened

  Scenario: Navigate to all filters
    Given page with the subcategory 'Смартфоны' is opened
    When I click on the 'Все фильтры' button
    Then the 'Все фильтры' page is opened

  Scenario: Select price and screen size filters
    Given the 'Все фильтры' page is opened
    When I set the max price filter to '20000 roubles'
    And I set the minimal screen size filter to '3 inches'
    Then the max price filter is set to '20000 roubles'
    And the minimal screen size filter is set to '3 inches'

  Scenario: Select phone manufacturer
    Given the 'Все фильтры' page is opened
    When I select 5 different manufacturers
    Then 5 different manufacturers are selected

  Scenario: Apply the filters
    Given the max price filter is set to '20000 roubles'
    And the minimal screen size filter is set to '3 inches'
    And 5 different manufacturers are selected
    When I click on the 'Показать' button
    Then the 'Смартфоны' page is opened

  Scenario: Count the number of phones
    Given the filtered page is opened
    When I count the number of phones
    Then the number of phones is printed to the console

  Scenario: Remember last phone
    Given the filtered page is opened
    When I remember the name of the last phone
    Then the name of last phone is saved to the memory

  Scenario: Change sorting
    Given the filtered page is opened
    When I change the sorting to 'по рейтингу'
    Then the sorting is changed to 'по рейтингу'

  Scenario: Find remembered phone
    Given the page is sorted by 'по рейтингу'
    When I search for the remembered phone on the page by name
    Then the remembered phone is found
    And I click on the remembered phone

  Scenario: Print out the phone rating
    Given the remembered phone is found
    When I save raing of the remembered phone
    Then the rating is printed to the console