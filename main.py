#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from .type_mocking import WebDriver, WebElement
from .utils import find_element_attr, find_element_attr_list, get_attr_list_str, try_slice
driver: WebDriver = webdriver.Chrome('./chromedriver') # type: ignore

def title():
    # type: () -> dict[str, str] | None
    title = find_element_attr(driver, 'div[data-rc="offerings/show/header/title"]')
    if title == None:
        return None
    return {
        'title_img': find_element_attr(title, 'img', 'src'),
        'title_maintitle': find_element_attr(title, 'h1', 'innerHTML'),
        'title_subtitle': find_element_attr(title, '.c-subtitle', 'innerHTML'),
        'title_tags': get_attr_list_str(find_element_attr_list(title, 'div[data-rc="offerings/shared/tags"] a'), 'innerHTML'),
    }

def media():
    # type: () -> dict[str, str] | None
    media = find_element_attr(driver, 'div[data-rc="offerings/show/header/media_react"]')
    if media == None:
        return None
    return {
        'main_img': get_attr_list_str(find_element_attr_list(media, 'img'), 'img'),
        'main_yt': get_attr_list_str(find_element_attr_list(media, 'iframe'), 'img'),
        'main_video': get_attr_list_str(find_element_attr_list(media, 'video source'), 'img'),
    }

def sidebar():
    # type: () -> dict[str, str] | None
    sidebar = find_element_attr(driver, 'div[data-rc="offerings/show/header/sidebar"]')
    if sidebar == None:
        return None

    # 募得幣別、募得金額、底下副標題（成功％數）
    sidebar_raised_type = find_element_attr(sidebar, '.offerings-show-header-raised_amount__title', 'innerHTML')
    sidebar_raised_amount = try_slice(find_element_attr(sidebar, '.offerings-show-header-raised_amount__title', 'innerHTML', ), slice(2, -1))
    sidebar_raised_subtitle = find_element_attr(driver, '.offerings-show-header-raised_amount__subtitle', 'innerHTML')

    # 贊助人數、底下副標題
    sidebar_investors = find_element_attr(driver, '.offerings-show-header-investors__title', 'innerHTML')
    sidebar_investors_subtitle = find_element_attr(driver, '.offerings-show-header-investors__subtitle', 'innerHTML')

    # 募資剩餘時間
    sidebar_left = try_slice(find_element_attr(driver, '.offerings-show-header-deadline__title', 'innerHTML'), slice(1, -6))

    # 募資結束時間、募資是否成功
    sidebar_closed_date = try_slice(find_element_attr(sidebar, 'div[data-rc="offerings/show/header/message_successfully_funded"] span', 'innerHTML'), slice(4, -2))
    if sidebar_closed_date == '':
        sidebar_success = '0'
    else:
        sidebar_success = '1'

    return {
        'sidebar_raised_type': sidebar_raised_type,
        'sidebar_raised_amount': sidebar_raised_amount,
        'sidebar_raised_subtitle': sidebar_raised_subtitle,
        'sidebar_investors': sidebar_investors,
        'sidebar_investors_subtitle': sidebar_investors_subtitle,
        'sidebar_left': sidebar_left,
        'sidebar_closed_date': sidebar_closed_date,
        'sidebar_success': sidebar_success
    }

def co_investors():
    # type: () -> dict[str, list[str]]
    # 先抓出 co-investors 的 block
    external = find_element_attr_list(driver, 'div[data-rc="external_investors/shared/investor"]')
    # 抓共同贊助者主標、副標
    external_investors = []     # type: list[str]
    external_subtitle = []      # type: list[str]
    external_description = []   # type: list[str]
    external_img = []           # type: list[str]
    external_also = []          # type: list[str]
    for e in external:
        [investors, subtitle] = find_element_attr_list(e, '.s-marginLeft1_5 div', 'innerHTML') + ['', '']
        external_investors.append(investors[1:-1])
        external_subtitle.append(subtitle[1:-1])
        # 抓共同贊助者介紹，如果太長，要分兩段抓
        description = find_element_attr(e, '.external_investors-shared-investor__description', 'innerHTML')
        temp = find_element_attr(e, 'span[style="display: none;"]', 'innerHTML')
        if temp != '':
            external_description.append((try_slice(description, slice(0, 174)) + temp)[1:-1])
        else:
            external_description.append(description.strip())
        # 抓共同贊助者縮圖、其他贊助專案
        [img, also] = find_element_attr_list(e, 'img', 'src') + ['', '']
        external_img.append(img)
        external_also.append(also)

    return {
        'external_investors': external_investors,
        'external_subtitle': external_subtitle,
        'external_description': external_description,
        'external_img': external_img,
        'external_also': external_also
    }

def deal_terms():
    #
    try:
        # 先抓出 deal_terms 的 block
        deal = find_element_attr(driver, 'div[id="deal-terms"] .terms-block')
        if deal == None:
            return None
        # 抓 valuation_cap 幣別、valuation_cap 金額，先看看有沒有 special
        try:
            valuation_cap = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/valuation_cap"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
            valuation_cap_type, valuation_cap = valuation_cap[0], valuation_cap[1:]
        except:
            valuation_cap_type, valuation_cap = None, None
        # 抓 discount
        try:
            discount = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/discount"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
        except:
            discount = None
        # 抓 最小/最大投資 幣別、金額
        try:
            min_investment = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/min_investment"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
            min_investment_type, min_investment = min_investment[0], min_investment[1:]
        except:
            min_investment_type, min_investment = None, None
        try:
            max_investment = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/max_investment"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
            max_investment_type, max_investment = max_investment[0], max_investment[1:]
        except:
            max_investment_type, max_investment = None, None
        # 抓募資目標 幣別、金額、抓截止日期
        funding_goal = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/raise_amounts"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
        funding_goal_type, funding_goal = funding_goal[0], funding_goal[1:]
        deadline = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/deadline"] .js-localtime_year').get_attribute('data-time')
        # 安全型別、提案人
        try:
            security = cut_span(deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/securities"] .c-deal-term__content').get_attribute('innerHTML')[1:])[:-2]
        except:
            security = None
        try:
            nominee = deal.find_element(By.CSS_SELECTOR,'[data-rc="offerings/show/deal_terms/nominee"] .c-deal-term__content').get_attribute('innerHTML')[1:-1]
        except:
            nominee = None
    except:
        valuation_cap_type, valuation_cap, discount, min_investment_type, min_investment, max_investment_type, max_investment, funding_goal_type, funding_goal, deadline, security, nominee = None, None, None, None, None, None, None, None, None, None, None, None
    return valuation_cap_type, valuation_cap, discount, min_investment_type, min_investment, max_investment_type, max_investment, funding_goal_type, funding_goal, deadline, security, nominee


