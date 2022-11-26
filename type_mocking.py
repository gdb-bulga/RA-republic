from selenium.webdriver.common.by import By
from __future__ import annotations

class WebElement:
    '''[ 假造型態 ] 網頁元素'''
    def find_element(self, by = By.ID, value = None):
        # type: (str, str | None) -> WebElement
        return self
    def find_elements(self, by = By.ID, value = None):
        # type: (str, str | None) -> list[WebElement]
        return [self]
    def get_attribute(self, name):
        # type: (str) -> str
        return ''

class WebDriver:
    '''[ 假造型態 ] 網頁讀取器'''
    def find_element(self, by = By.ID, value = None):
        # type: (str, str | None) -> WebElement
        return WebElement()
    def find_elements(self, by = By.ID, value = None):
        # type: (str, str | None) -> list[WebElement]
        return [WebElement()]

WebContainer = WebElement | WebDriver
'''[ 假造型態 ] 網頁容器統稱'''
