import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/path/chromedriver.exe')
    pytest.driver.set_window_size(800, 600)
    pytest.driver.maximize_window()
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    pytest.driver.find_element_by_id('email').send_keys('agonik@mi.com')
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.nav-link[href="/my_pets"]'))
        )
    pytest.driver.find_element_by_css_selector('a.nav-link[href="/my_pets"]').click()

    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'
    yield
    pytest.driver.quit()


# Проверка карточек "Мои питомцы"
def test_my_pets():
    pytest.driver.implicitly_wait(5)
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-tittle')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


# проверяем присутствие всех питомцев
def test_all_pets():
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    pets = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    count_stats = statistic[0].text.split('\n')
    count_stats = count_stats[1].split(' ')
    count_stats = int(count_stats[1])
    count_cards = len(pets)
    assert count_stats == count_cards

# проверяем наличие клички, возраста и породы
def test_having_description():
        WebDriverWait(pytest.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
        data = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
        for i in range(len(data)):
            assert len(data[i].text.replace('\n', '').split(' ')) == 3


# проверяем наличие не менее половины фото питомцев
def test_count_of_foto():
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    statistic = pytest.driver.find_elements_by_css_selector(".\\.col-sm-4.left")
    images = pytest.driver.find_elements_by_css_selector('.table.table-hover img')
    count_stats = statistic[0].text.split('\n')
    count_stats = count_stats[1].split(' ')
    count_stats = int(count_stats[1])
    count_cards_with_foto = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            count_cards_with_foto += 1
    assert count_cards_with_foto >= count_stats/2


# проверка на совпадении клички
def test_names():
    WebDriverWait(pytest.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    data = pytest.driver.find_elements_by_css_selector('.table.table-hover tbody tr')
    pets_name = []
    for i in range(len(data)):
        pets_name.append(data[i].text.replace('\n', '').split(' ')[0])
    pets_name_set = set(pets_name)
    assert len(pets_name) == len(pets_name_set)







# python -m pytest -v --driver Chrome --driver-path c:/path/chromedriver.exe  test.py
