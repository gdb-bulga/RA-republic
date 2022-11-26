from selenium.webdriver.common.by import By
from .type_mocking import WebElement, WebContainer
from typing import overload

@overload
def get_attr_list_str(elements, attr):
    # type: (None, str) -> None
    ...
@overload
def get_attr_list_str(elements, attr):
    # type: (list[WebElement], str) -> str
    ...
def get_attr_list_str(elements, attr):
    # type: (list[WebElement] | None, str) -> str | None
    '''獲取elements陣列中指定的attr, 並以","相連形成字串'''

    if elements == None:
        return None
    attrList = [] # type: list[str]
    for e in elements:
        attrList.append(e.get_attribute(attr).strip())
    return ','.join(attrList)

@overload
def find_element_attr(source, selector, attr_target = None):
    # type: (WebContainer, str, None) -> WebElement | None
    ...
@overload
def find_element_attr(source, selector, attr_target):
    # type: (WebContainer, str, str) -> str
    ...
def find_element_attr(source, selector, attr_target = None):
    # type: (WebContainer, str, str | None) -> WebElement | str | None
    '''回傳element, 若給定attr_target, 改給予指定attr'''
    try:
        element = source.find_element(By.CSS_SELECTOR, selector)
        if attr_target == None:
            return element
        return element.get_attribute(attr_target).strip()
    except:
        if attr_target == None:
            return None
        return ''

@overload
def find_element_attr_list(source, selector, attr_target = None):
    # type: (WebContainer, str, None) -> list[WebElement]
    ...
@overload
def find_element_attr_list(source, selector, attr_target):
    # type: (WebContainer, str, str) -> list[str]
    ...
def find_element_attr_list(source, selector, attr_target = None):
    # type: (WebContainer, str, str | None) -> list[WebElement] | list[str]
    '''回傳element陣列, 若給定attr_target, 改給予指定attr陣列'''

    elementList = source.find_elements(By.CSS_SELECTOR, selector)
    if attr_target == None:
        return elementList
    attrList = [] # type: list[str]
    for e in elementList:
        attrList.append(e.get_attribute(attr_target).strip())
    return attrList

def try_slice(input, slicer):
    # type: (str | None, slice) -> str
    '''獲取指定位置substr, input為None時回傳空字串'''

    if input == None:
        return ''
    return input[slicer]

def cut_span(k, temp):
    '''小助手1: 把 <span 到 > 之間全部切掉'''
    j = k+5
    while temp[j] != '>':
        j += 1
    return temp[:k] + temp[j+1:]