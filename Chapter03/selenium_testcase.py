# Code Listing - #10
# Selenium を使うコードのテストコードの例。興味深い。

"""
Module selenium_testcase - Example of implementing an automated UI test using selenium framework
"""

from selenium import webdriver
import pytest

@pytest.fixture(scope='session') # 意味：テスト全体で一度しか実行しない
def driver():
    # 右辺は自分の環境に置き換えていい。
    #driver = webdriver.Firefox()
    driver = webdriver.Edge()
    yield driver
    driver.quit()


def test_python_dotorg(driver):
    """ Test details of python.org website URLs """

    # 以降のコードは Selenium に慣れていれば問題ないだろう。

    driver.get('http://www.python.org')
    # Some tests
    assert driver.title == 'Welcome to Python.org'
    # Find out the 'Community' link
    comm_elem = driver.find_elements_by_link_text('Community')[0]
    # Get the URL
    comm_url = comm_elem.get_attribute('href')
    # Visit it
    print('Community URL=>', comm_url)
    driver.get(comm_url)
    # Assert its title
    assert driver.title == 'Our Community | Python.org'
    assert comm_url == 'https://www.python.org/community/'
