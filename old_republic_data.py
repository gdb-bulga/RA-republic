#!/usr/bin/env python
# coding: utf-8

# ### 設定 selenium

# In[78]:


from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome('./chromedriver')


# ### 底下開始把所有資料的抓取方法定義成一個一個不同的 function

# 這邊是等一下會一直用到的功能，主要是把 list 中的內容一個一個拔出來的迴圈們

# In[79]:


# 把每一個 html 裡的內容去頭去尾取出來（頭尾通常是換行符號）
# 為了儲存方便，通通用逗號連起來
def break_elements(elements):
    l = ''
    for i in elements:
        l = l + i.get_attribute('innerHTML')[1:-1] + ','
    return l[:-1]

# 把每一個 html 裡的內容直接取出來，不去頭去尾
# 為了儲存方便，通通用逗號連起來
def break_elements_within_cut(elements):
    l = ''
    for i in elements:
        l = l + i.get_attribute('innerHTML') + ','
    return l[:-1]

# 把每一個 html 裡的 src 內容取出來，會是一個圖片網址
# 為了儲存方便，通通用逗號連起來
def break_imgs(imgs):
    l = ''
    for i in imgs:
        l = l + i.get_attribute('src') + ','
    return l[:-1]

# 把每一個 html 裡的 style 內容取出來，會是一個圖片網址
# 為了儲存方便，通通用逗號連起來
def break_video_cover(imgs):
    l = ''
    for i in imgs:
        l = l + i.get_attribute('style') + ','
    return l[:-1]


# In[80]:


# 把 <div 切掉
def cut_div(temp):
    for k in range(len(temp)):
        while (temp[k:k+4] == '<div'):
            temp = temp[:k]
    return temp

# 把 <div 切掉 + 把每一個 html 裡的內容去頭去尾取出來的 function
def break_elements_cut_div(elements):
    l = ''
    for i in elements:
        l = l + cut_div(i.get_attribute('innerHTML')[1:-1]) + ','
    return l[:-1]


# 這是把文字整理乾淨的 function 跟他的小助手們

# In[81]:


def strong(k, temp):
    l = ''
    j = k+8
    while temp[j:j+9] != '</strong>':
        j += 1
    l = temp[k+8:j]
    return temp[:k] + l + temp[j+9:], l
    
def ahref(k, temp):
    l_url = ''
    l = ''
    j = k+9
    while temp[j] != '"':
        j += 1
    l_url = temp[k+8:j+1]
    while temp[j] != '>':
        j += 1
    m = j+1
    while temp[m:m+4] != '</a>':
        m += 1
    l = temp[j+1:m]
    return temp[:k] + l + temp[m+4:], l,  l_url

def em(k, temp):
    l = ''
    j = k+4
    while temp[j:j+5] != '</em>':
        j += 1
    l = temp[k+4:j]
    return temp[:k] + l + temp[j+5:], l
# 小助手1:把 <span 到 > 之間全部切掉
def cut_span(k, temp):
    j = k+5
    while temp[j] != '>':
        j += 1
    return temp[:k] + temp[j+1:]

# 小助手2:把 <img 到 > 之間全部切掉
def cut_img(k, temp):
    j = k+4
    while temp[j] != '>':
        j += 1
    return temp[:k] + temp[j+1:]
    
# 小助手3:把 <iframe 到 > 之間全部切掉
def cut_iframe(k, temp):
    j = k+7
    while temp[j] != '>':
        j += 1
    return temp[:k] + temp[j+1:]

# 號召以上助手們一起整理文字的 function
def break_section_text_elements(elements):
    l = ''
    l_strong = ''
    l_a = ''
    l_a_url = ''
    l_em = ''
    for i in elements:
        temp = i.get_attribute('innerHTML')
        for k in range(len(temp)):
            while 1:
                t = temp
                
                if temp[k:k+4] == '<br>':
                    temp = temp[:k] + temp[k+4:]
                if temp[k:k+6] == '&nbsp;':
                    temp = temp[:k] + temp[k+6:]
                if (temp[k:k+4] == '<img'):
                    temp = cut_img(k, temp)
                if (temp[k:k+5] == '<span'):
                    temp = cut_span(k, temp)
                if temp[k:k+7] == '</span>':
                    temp = temp[:k] + temp[k+7:]
                if (temp[k:k+7] == '<iframe'):
                    temp = cut_iframe(k, temp)
                if temp[k:k+9] == '</iframe>':
                    temp = temp[:k] + temp[k+9:]
                
                if temp[k:k+8] == '<strong>':
                    temp, t_strong = strong(k, temp)
                    l_strong = l_strong + t_strong + '\n'
                if temp[k:k+8] == '<a href=':
                    temp, t_a, a_url = ahref(k, temp)
                    l_a = l_a + t_a + '\n'
                    l_a_url = l_a_url + a_url + '\n'
                if temp[k:k+4] == '<em>':
                    temp, t_em = em(k, temp)
                    l_em = l_em + t_em + '\n'
                
                if temp == t:
                    break
        
        # 如果頭尾是換行也刪掉
        if len(temp) == 0:
            continue
        while temp[0] == '\n':
            temp = temp[1:]
        while temp[-1] == '\n':
            temp = temp[:-1]
            
        # 全部用換行符號連起來
        l = l + temp + '\n'
    return l[:-1], l_strong[:-1], [l_a[:-1], l_a_url[:-1]], l_em[:-1]


# ## 網頁的各個區塊

# In[651]:


# 標題區域
def title():
    # 先抓出 title 的 block
    title = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/title"]')
    # 再分別抓頭貼、主標題、副標題
    try:
        title_img = title.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
    except:
        title_img = None
    try:
        title_maintitle = title.find_element(By.TAG_NAME, "h1").get_attribute('innerHTML')[1:-1]
    except:
        title_maintitle = None
    try:
        title_subtitle = title.find_element(By.CLASS_NAME, 'c-subtitle').get_attribute('innerHTML')[1:-1]
    except:
        title_subtitle = None
    # 抓 tag
    try:
        title_tags = break_elements_within_cut(title.find_elements(By.CSS_SELECTOR,'div[data-rc="offerings/shared/tags"] a'))
    except:
        title_tags = None
    return title_img, title_maintitle, title_subtitle, title_tags


# In[652]:


def media():
    # 先抓出 media 的 block
    media = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/media_react"]')
    try:
        main_img = break_imgs(media.find_elements(By.CSS_SELECTOR, ' img'))
        main_yt = break_imgs(media.find_elements(By.CSS_SELECTOR, ' iframe'))
        main_video = break_imgs(media.find_elements(By.CSS_SELECTOR, ' video source'))
    except:
        main_img, main_yt, main_video = None, None
    return main_img, main_yt, main_video


# In[653]:


# 募資金額（標題旁邊）區域
def sidebar():
    # 先抓出 sidebar 的 block
    sidebar = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/sidebar"]')
    # 募得幣別、募得金額、底下副標題（成功％數）
    try:
        sidebar_raised_type = sidebar.find_element(By.CSS_SELECTOR, '.offerings-show-header-raised_amount__title').get_attribute('innerHTML')[1]
        sidebar_raised_amount = sidebar.find_element(By.CSS_SELECTOR, '.offerings-show-header-raised_amount__title').get_attribute('innerHTML')[2:-1]
        sidebar_raised_subtitle = driver.find_element(By.CSS_SELECTOR, '.offerings-show-header-raised_amount__subtitle').get_attribute('innerHTML')[1:-1]
    except:
        sidebar_raised_type, sidebar_raised_amount, sidebar_raised_subtitle = None, None, None
    
    # 贊助人數、底下副標題
    try:
        sidebar_investors = driver.find_element(By.CSS_SELECTOR, '.offerings-show-header-investors__title').get_attribute('innerHTML')[1:-1]
        sidebar_investors_subtitle = driver.find_element(By.CSS_SELECTOR, '.offerings-show-header-investors__subtitle').get_attribute('innerHTML')[1:-1]
    except:
        sidebar_investors, sidebar_investors_subtitle = None, None
        
    # 募資剩餘時間
    try:
        sidebar_left = driver.find_element(By.CSS_SELECTOR, '.offerings-show-header-deadline__title').get_attribute('innerHTML')[1:-6]
    except:
        sidebar_left = None    
    # 募資結束時間、募資是否成功
    try:
        sidebar_closed_date = sidebar.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/message_successfully_funded"] span').get_attribute('innerHTML')[4:-2]
        sidebar_success = 1
    except:
        sidebar_closed_date = None
        sidebar_success = 0
    return sidebar_raised_type, sidebar_raised_amount, sidebar_raised_subtitle, sidebar_investors, sidebar_investors_subtitle, sidebar_left, sidebar_closed_date, sidebar_success


# In[654]:


# co-investors 區域
def co_investors():
    # 先抓出 co-investors 的 block
    external = driver.find_elements(By.CSS_SELECTOR,'div[data-rc="external_investors/shared/investor"]')
    # 抓共同贊助者主標、副標
    external_investors, external_subtitle, external_description, external_img, external_also = [], [], [], [], [] 
    for i in external:
        try:
            external_investors.append(i.find_elements(By.CSS_SELECTOR, '.s-marginLeft1_5 div')[0].get_attribute('innerHTML')[1:-1])
        except:    
            external_investors.append('')
        try:
            external_subtitle.append(i.find_elements(By.CSS_SELECTOR, '.s-marginLeft1_5 div')[1].get_attribute('innerHTML')[1:-1])
        except:
            external_subtitle.append('')
        # 抓共同贊助者介紹，如果太長，要分兩段抓
        try:
            temp = i.find_element(By.CSS_SELECTOR, '.external_investors-shared-investor__description').get_attribute('innerHTML')[:174]
            temp += i.find_element(By.CSS_SELECTOR, 'span[style="display: none;"]').get_attribute('innerHTML')
            external_description.append(temp[1:-1])
        except:
            try:
                external_description.append(i.find_element(By.CSS_SELECTOR, '.external_investors-shared-investor__description').get_attribute('innerHTML')[1:-1])
            except:
                external_description.append('')
        # 抓共同贊助者縮圖、其他贊助專案
        try:
            external_img.append(external.find_elements(By.CSS_SELECTOR,'img')[0].get_attribute('src'))
        except:
            external_img.append('')
        try:
            external_also.append(external.find_elements(By.CSS_SELECTOR,'img')[1].get_attribute('src'))
        except:
            external_also.append('')
    return external_investors, external_subtitle, external_description, external_img, external_also


# In[655]:


# pitch_deal_terms
def deal_terms():
    try:
        # 先抓出 deal_terms 的 block
        deal = driver.find_element(By.CSS_SELECTOR,'div[id="deal-terms"] .terms-block')
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


# In[656]:


# pitch_document
def document():
    # 先抓出 document 的 block
    document = driver.find_elements(By.CSS_SELECTOR,'div[data-rc="offerings/shared/documents_section"] .offerings-shared-documents_section__document_container')
    # 抓 Reg 類型
    doc_type = document[0].find_element(By.CSS_SELECTOR,'.u-colorGray8').get_attribute('innerHTML')[1:-1]
    # 抓檔案
    try:
        link = document[1].find_elements(By.CSS_SELECTOR,' a')
        name = document[1].find_elements(By.CSS_SELECTOR,' a span')
        doc_link, doc_name = [], []
        for i in link:
            doc_link.append(i.get_attribute('href'))
        for i in name:
            doc_name.append(i.get_attribute('innerHTML')[1:-1])
    except:
        doc_link, doc_name = None, None
    return doc_type, doc_link, doc_name


# In[657]:


# pitch_bonus_perks
def bonus_perks():
    try:
        perks = driver.find_elements(By.CSS_SELECTOR,'div[id="perks"] .offerings-show-perk__perk-content')
        perk_investor = []
        perk_amount = []
        perk_amount_type = []
        perk_receive = []
        perk_limit = []

        for i in perks:
            try:
                perk_investor.append(i.find_element(By.CSS_SELECTOR,'.offerings-show-perk__investor-counter').get_attribute('innerHTML')[1:-11])
            except:
                perk_investor.append(None)
            try:
                perk_amount.append(i.find_element(By.CSS_SELECTOR,'.offerings-show-perk__amount').get_attribute('innerHTML')[2:-1])
            except:
                perk_amount.append(None)
            try:
                perk_amount_type.append(i.find_element(By.CSS_SELECTOR,'.offerings-show-perk__amount').get_attribute('innerHTML')[1])
            except:
                perk_amount_type.append(None)
            try:
                perk_receive.append(break_elements_cut_div(i.find_elements(By.CSS_SELECTOR,' ul li')))
            except:
                perk_receive.append(None)
            try:
                perk_limit.append(i.find_element(By.CSS_SELECTOR,' li div').get_attribute('innerHTML')[10:-2])
            except:
                perk_limit.append(None)
    except:
        perk_investor, perk_amount, perk_amount_type, perk_receive, perk_limit = None, None, None, None, None
    return perk_investor, perk_amount, perk_amount_type, perk_receive, perk_limit


# In[658]:


# pitch_highlights
def highlights():
    highlight = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/pitch_highlights"]')
    try:
        highlight_title = break_elements(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__title'))
        highlight_description = break_elements(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__description'))
        highlight_icon = break_imgs(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__icon img'))
    except:
        highlight_title = None
        highlight_description = None
        highlight_icon = None

    highlight_content = break_elements_within_cut(highlight.find_elements(By.CSS_SELECTOR,'.offerings-show-pitch_highlights__content li'))
    return highlight_title, highlight_description, highlight_icon, highlight_content


# 以下的格式全都一樣，很讚

# In[659]:


# pitch_problem
def problem():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            problem = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Problem"] div.js-pitch_content_details')
        except:
            problem = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Problem"] div.js-pitch_content')

        problem_h2, problem_h2_strong, problem_h2_a, problem_h2_em = break_section_text_elements(problem.find_elements(By.CSS_SELECTOR,'h2'))
        problem_h2_img = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h2 img'))
        problem_h2_yt = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        problem_h2_video = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        problem_h3, problem_h3_strong, problem_h3_a, problem_h3_em = break_section_text_elements(problem.find_elements(By.CSS_SELECTOR,'h3'))
        problem_h3_img = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h3 img'))
        problem_h3_yt = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        problem_h3_video = break_imgs(problem.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        problem_p, problem_p_strong, problem_p_a, problem_p_em = break_section_text_elements(problem.find_elements(By.CSS_SELECTOR,'p'))
        problem_p_img = break_imgs(problem.find_elements(By.CSS_SELECTOR,'p img'))
        problem_p_yt = break_imgs(problem.find_elements(By.CSS_SELECTOR,'p iframe'))
        problem_p_video = break_imgs(problem.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        problem_h2, problem_h2_strong, problem_h2_a, problem_h2_em, problem_h2_img, problem_h2_yt, problem_h2_video = None, None, None, None, None, None, None
        problem_h3, problem_h3_strong, problem_h3_a, problem_h3_em, problem_h3_img, problem_h3_yt, problem_h3_video = None, None, None, None, None, None, None
        problem_p, problem_p_strong, problem_p_a, problem_p_em, problem_p_img, problem_p_yt, problem_p_video = None, None, None, None, None, None, None
    
    return problem_h2, problem_h2_strong, problem_h2_a, problem_h2_em, problem_h2_img, problem_h2_yt, problem_h2_video, problem_h3, problem_h3_strong, problem_h3_a, problem_h3_em, problem_h3_img, problem_h3_yt, problem_h3_video, problem_p, problem_p_strong, problem_p_a, problem_p_em, problem_p_img, problem_p_yt, problem_p_video


# In[660]:


# pitch_solution
def solution():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            solution = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Solution"] div.js-pitch_content_details')
        except:
            solution = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Solution"] div.js-pitch_content')

        solution_h2, solution_h2_strong, solution_h2_a, solution_h2_em = break_section_text_elements(solution.find_elements(By.CSS_SELECTOR,'h2'))
        solution_h2_img = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h2 img'))
        solution_h2_yt = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        solution_h2_video = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        solution_h3, solution_h3_strong, solution_h3_a, solution_h3_em = break_section_text_elements(solution.find_elements(By.CSS_SELECTOR,'h3'))
        solution_h3_img = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h3 img'))
        solution_h3_yt = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        solution_h3_video = break_imgs(solution.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        solution_p, solution_p_strong, solution_p_a, solution_p_em = break_section_text_elements(solution.find_elements(By.CSS_SELECTOR,'p'))
        solution_p_img = break_imgs(solution.find_elements(By.CSS_SELECTOR,'p img'))
        solution_p_yt = break_imgs(solution.find_elements(By.CSS_SELECTOR,'p iframe'))
        solution_p_video = break_imgs(solution.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        solution_h2, solution_h2_strong, solution_h2_a, solution_h2_em, solution_h2_img, solution_h2_yt, solution_h2_video = None, None, None, None, None, None, None
        solution_h3, solution_h3_strong, solution_h3_a, solution_h3_em, solution_h3_img, solution_h3_yt, solution_h3_video = None, None, None, None, None, None, None
        solution_p, solution_p_strong, solution_p_a, solution_p_em, solution_p_img, solution_p_yt, solution_p_video = None, None, None, None, None, None, None
    
    return solution_h2, solution_h2_strong, solution_h2_a, solution_h2_em, solution_h2_img, solution_h2_yt, solution_h2_video, solution_h3, solution_h3_strong, solution_h3_a, solution_h3_em, solution_h3_img, solution_h3_yt, solution_h3_video, solution_p, solution_p_strong, solution_p_a, solution_p_em, solution_p_img, solution_p_yt, solution_p_video


# In[661]:


# pitch_product
def product():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            product = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Product"] div.js-pitch_content_details')
        except:
            product = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Product"] div.js-pitch_content')
        
        product_h2, product_h2_strong, product_h2_a, product_h2_em = break_section_text_elements(product.find_elements(By.CSS_SELECTOR,'h2'))
        product_h2_img = break_imgs(product.find_elements(By.CSS_SELECTOR,'h2 img'))
        product_h2_yt = break_imgs(product.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        product_h2_video = break_imgs(product.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        product_h3, product_h3_strong, product_h3_a, product_h3_em = break_section_text_elements(product.find_elements(By.CSS_SELECTOR,'h3'))
        product_h3_img = break_imgs(product.find_elements(By.CSS_SELECTOR,'h3 img'))
        product_h3_yt = break_imgs(product.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        product_h3_video = break_imgs(product.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        product_p, product_p_strong, product_p_a, product_p_em = break_section_text_elements(product.find_elements(By.CSS_SELECTOR,'p'))
        product_p_img = break_imgs(product.find_elements(By.CSS_SELECTOR,'p img'))
        product_p_yt = break_imgs(product.find_elements(By.CSS_SELECTOR,'p iframe'))
        product_p_video = break_imgs(product.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        product_h2, product_h2_strong, product_h2_a, product_h2_em, product_h2_img, product_h2_yt, product_h2_video = None, None, None, None, None, None, None
        product_h3, product_h3_strong, product_h3_a, product_h3_em, product_h3_img, product_h3_yt, product_h3_video = None, None, None, None, None, None, None
        product_p, product_p_strong, product_p_a, product_p_em, product_p_img, product_p_yt, product_p_video = None, None, None, None, None, None, None
    
    return product_h2, product_h2_strong, product_h2_a, product_h2_em, product_h2_img, product_h2_yt, product_h2_video, product_h3, product_h3_strong, product_h3_a, product_h3_em, product_h3_img, product_h3_yt, product_h3_video, product_p, product_p_strong, product_p_a, product_p_em, product_p_img, product_p_yt, product_p_video


# In[662]:


# pitch_traction
def traction():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            traction = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Traction"] div.js-pitch_content_details')
        except:
            traction = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Traction"] div.js-pitch_content')

        traction_h2, traction_h2_strong, traction_h2_a, traction_h2_em = break_section_text_elements(traction.find_elements(By.CSS_SELECTOR,'h2'))
        traction_h2_img = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h2 img'))
        traction_h2_yt = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        traction_h2_video = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        traction_h3, traction_h3_strong, traction_h3_a, traction_h3_em = break_section_text_elements(traction.find_elements(By.CSS_SELECTOR,'h3'))
        traction_h3_img = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h3 img'))
        traction_h3_yt = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        traction_h3_video = break_imgs(traction.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        traction_p, traction_p_strong, traction_p_a, traction_p_em = break_section_text_elements(traction.find_elements(By.CSS_SELECTOR,'p'))
        traction_p_img = break_imgs(traction.find_elements(By.CSS_SELECTOR,'p img'))
        traction_p_yt = break_imgs(traction.find_elements(By.CSS_SELECTOR,'p iframe'))
        traction_p_video = break_imgs(traction.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        traction_h2, traction_h2_strong, traction_h2_a, traction_h2_em, traction_h2_img, traction_h2_yt, traction_h2_video = None, None, None, None, None, None, None
        traction_h3, traction_h3_strong, traction_h3_a, traction_h3_em, traction_h3_img, traction_h3_yt, traction_h3_video = None, None, None, None, None, None, None
        traction_p, traction_p_strong, traction_p_a, traction_p_em, traction_p_img, traction_p_yt, traction_p_video = None, None, None, None, None, None, None
    
    return traction_h2, traction_h2_strong, traction_h2_a, traction_h2_em, traction_h2_img, traction_h2_yt, traction_h2_video, traction_h3, traction_h3_strong, traction_h3_a, traction_h3_em, traction_h3_img, traction_h3_yt, traction_h3_video, traction_p, traction_p_strong, traction_p_a, traction_p_em, traction_p_img, traction_p_yt, traction_p_video


# In[663]:


# pitch_customers
def customers():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            customers = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Customers"] div.js-pitch_content_details')
        except:
            customers = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Customers"] div.js-pitch_content')

        customers_h2, customers_h2_strong, customers_h2_a, customers_h2_em = break_section_text_elements(customers.find_elements(By.CSS_SELECTOR,'h2'))
        customers_h2_img = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h2 img'))
        customers_h2_yt = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        customers_h2_video = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        customers_h3, customers_h3_strong, customers_h3_a, customers_h3_em = break_section_text_elements(customers.find_elements(By.CSS_SELECTOR,'h3'))
        customers_h3_img = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h3 img'))
        customers_h3_yt = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        customers_h3_video = break_imgs(customers.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        customers_p, customers_p_strong, customers_p_a, customers_p_em = break_section_text_elements(customers.find_elements(By.CSS_SELECTOR,'p'))
        customers_p_img = break_imgs(customers.find_elements(By.CSS_SELECTOR,'p img'))
        customers_p_yt = break_imgs(customers.find_elements(By.CSS_SELECTOR,'p iframe'))
        customers_p_video = break_imgs(customers.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        customers_h2, customers_h2_strong, customers_h2_a, customers_h2_em, customers_h2_img, customers_h2_yt, customers_h2_video = None, None, None, None, None, None, None
        customers_h3, customers_h3_strong, customers_h3_a, customers_h3_em, customers_h3_img, customers_h3_yt, customers_h3_video = None, None, None, None, None, None, None
        customers_p, customers_p_strong, customers_p_a, customers_p_em, customers_p_img, customers_p_yt, customers_p_video = None, None, None, None, None, None, None
    
    return customers_h2, customers_h2_strong, customers_h2_a, customers_h2_em, customers_h2_img, customers_h2_yt, customers_h2_video, customers_h3, customers_h3_strong, customers_h3_a, customers_h3_em, customers_h3_img, customers_h3_yt, customers_h3_video, customers_p, customers_p_strong, customers_p_a, customers_p_em, customers_p_img, customers_p_yt, customers_p_video


# In[664]:


# pitch_biz
def biz():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            biz = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Biz. model"] div.js-pitch_content_details')
        except:
            biz = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Biz. model"] div.js-pitch_content')

        biz_h2, biz_h2_strong, biz_h2_a, biz_h2_em = break_section_text_elements(biz.find_elements(By.CSS_SELECTOR,'h2'))
        biz_h2_img = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h2 img'))
        biz_h2_yt = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        biz_h2_video = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        biz_h3, biz_h3_strong, biz_h3_a, biz_h3_em = break_section_text_elements(biz.find_elements(By.CSS_SELECTOR,'h3'))
        biz_h3_img = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h3 img'))
        biz_h3_yt = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        biz_h3_video = break_imgs(biz.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        biz_p, biz_p_strong, biz_p_a, biz_p_em = break_section_text_elements(biz.find_elements(By.CSS_SELECTOR,'p'))
        biz_p_img = break_imgs(biz.find_elements(By.CSS_SELECTOR,'p img'))
        biz_p_yt = break_imgs(biz.find_elements(By.CSS_SELECTOR,'p iframe'))
        biz_p_video = break_imgs(biz.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        biz_h2, biz_h2_strong, biz_h2_a, biz_h2_em, biz_h2_img, biz_h2_yt, biz_h2_video = None, None, None, None, None, None, None
        biz_h3, biz_h3_strong, biz_h3_a, biz_h3_em, biz_h3_img, biz_h3_yt, biz_h3_video = None, None, None, None, None, None, None
        biz_p, biz_p_strong, biz_p_a, biz_p_em, biz_p_img, biz_p_yt, biz_p_video = None, None, None, None, None, None, None
    
    return biz_h2, biz_h2_strong, biz_h2_a, biz_h2_em, biz_h2_img, biz_h2_yt, biz_h2_video, biz_h3, biz_h3_strong, biz_h3_a, biz_h3_em, biz_h3_img, biz_h3_yt, biz_h3_video, biz_p, biz_p_strong, biz_p_a, biz_p_em, biz_p_img, biz_p_yt, biz_p_video


# In[665]:


# pitch_market
def market():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            market = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Market"] div.js-pitch_content_details')
        except:
            market = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Market"] div.js-pitch_content')

        market_h2, market_h2_strong, market_h2_a, market_h2_em = break_section_text_elements(market.find_elements(By.CSS_SELECTOR,'h2'))
        market_h2_img = break_imgs(market.find_elements(By.CSS_SELECTOR,'h2 img'))
        market_h2_yt = break_imgs(market.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        market_h2_video = break_imgs(market.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        market_h3, market_h3_strong, market_h3_a, market_h3_em = break_section_text_elements(market.find_elements(By.CSS_SELECTOR,'h3'))
        market_h3_img = break_imgs(market.find_elements(By.CSS_SELECTOR,'h3 img'))
        market_h3_yt = break_imgs(market.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        market_h3_video = break_imgs(market.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        market_p, market_p_strong, market_p_a, market_p_em = break_section_text_elements(market.find_elements(By.CSS_SELECTOR,'p'))
        market_p_img = break_imgs(market.find_elements(By.CSS_SELECTOR,'p img'))
        market_p_yt = break_imgs(market.find_elements(By.CSS_SELECTOR,'p iframe'))
        market_p_video = break_imgs(market.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        market_h2, market_h2_strong, market_h2_a, market_h2_em, market_h2_img, market_h2_yt, market_h2_video = None, None, None, None, None, None, None
        market_h3, market_h3_strong, market_h3_a, market_h3_em, market_h3_img, market_h3_yt, market_h3_video = None, None, None, None, None, None, None
        market_p, market_p_strong, market_p_a, market_p_em, market_p_img, market_p_yt, market_p_video = None, None, None, None, None, None, None
    
    return market_h2, market_h2_strong, market_h2_a, market_h2_em, market_h2_img, market_h2_yt, market_h2_video, market_h3, market_h3_strong, market_h3_a, market_h3_em, market_h3_img, market_h3_yt, market_h3_video, market_p, market_p_strong, market_p_a, market_p_em, market_p_img, market_p_yt, market_p_video


# In[666]:


# pitch_competition
def competition():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            competition = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Competition"] div.js-pitch_content_details')
        except:
            competition = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Competition"] div.js-pitch_content')

        competition_h2, competition_h2_strong, competition_h2_a, competition_h2_em = break_section_text_elements(competition.find_elements(By.CSS_SELECTOR,'h2'))
        competition_h2_img = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h2 img'))
        competition_h2_yt = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        competition_h2_video = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        competition_h3, competition_h3_strong, competition_h3_a, competition_h3_em = break_section_text_elements(competition.find_elements(By.CSS_SELECTOR,'h3'))
        competition_h3_img = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h3 img'))
        competition_h3_yt = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        competition_h3_video = break_imgs(competition.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        competition_p, competition_p_strong, competition_p_a, competition_p_em = break_section_text_elements(competition.find_elements(By.CSS_SELECTOR,'p'))
        competition_p_img = break_imgs(competition.find_elements(By.CSS_SELECTOR,'p img'))
        competition_p_yt = break_imgs(competition.find_elements(By.CSS_SELECTOR,'p iframe'))
        competition_p_video = break_imgs(competition.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        competition_h2, competition_h2_strong, competition_h2_a, competition_h2_em, competition_h2_img, competition_h2_yt, competition_h2_video = None, None, None, None, None, None, None
        competition_h3, competition_h3_strong, competition_h3_a, competition_h3_em, competition_h3_img, competition_h3_yt, competition_h3_video = None, None, None, None, None, None, None
        competition_p, competition_p_strong, competition_p_a, competition_p_em, competition_p_img, competition_p_yt, competition_p_video = None, None, None, None, None, None, None
    
    return competition_h2, competition_h2_strong, competition_h2_a, competition_h2_em, competition_h2_img, competition_h2_yt, competition_h2_video, competition_h3, competition_h3_strong, competition_h3_a, competition_h3_em, competition_h3_img, competition_h3_yt, competition_h3_video, competition_p, competition_p_strong, competition_p_a, competition_p_em, competition_p_img, competition_p_yt, competition_p_video


# In[667]:


# pitch_vision
def vision():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            vision = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Vision and strategy"] div.js-pitch_content_details')
        except:
            vision = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Vision and strategy"] div.js-pitch_content')

        vision_h2, vision_h2_strong, vision_h2_a, vision_h2_em = break_section_text_elements(vision.find_elements(By.CSS_SELECTOR,'h2'))
        vision_h2_img = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h2 img'))
        vision_h2_yt = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        vision_h2_video = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        vision_h3, vision_h3_strong, vision_h3_a, vision_h3_em = break_section_text_elements(vision.find_elements(By.CSS_SELECTOR,'h3'))
        vision_h3_img = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h3 img'))
        vision_h3_yt = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        vision_h3_video = break_imgs(vision.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        vision_p, vision_p_strong, vision_p_a, vision_p_em = break_section_text_elements(vision.find_elements(By.CSS_SELECTOR,'p'))
        vision_p_img = break_imgs(vision.find_elements(By.CSS_SELECTOR,'p img'))
        vision_p_yt = break_imgs(vision.find_elements(By.CSS_SELECTOR,'p iframe'))
        vision_p_video = break_imgs(vision.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        vision_h2, vision_h2_strong, vision_h2_a, vision_h2_em, vision_h2_img, vision_h2_yt, vision_h2_video = None, None, None, None, None, None, None
        vision_h3, vision_h3_strong, vision_h3_a, vision_h3_em, vision_h3_img, vision_h3_yt, vision_h3_video = None, None, None, None, None, None, None
        vision_p, vision_p_strong, vision_p_a, vision_p_em, vision_p_img, vision_p_yt, vision_p_video = None, None, None, None, None, None, None
    
    return vision_h2, vision_h2_strong, vision_h2_a, vision_h2_em, vision_h2_img, vision_h2_yt, vision_h2_video, vision_h3, vision_h3_strong, vision_h3_a, vision_h3_em, vision_h3_img, vision_h3_yt, vision_h3_video, vision_p, vision_p_strong, vision_p_a, vision_p_em, vision_p_img, vision_p_yt, vision_p_video


# In[668]:


# pitch_impact
def impact():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            impact = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Impact"] div.js-pitch_content_details')
        except:
            impact = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Impact"] div.js-pitch_content')

        impact_h2, impact_h2_strong, impact_h2_a, impact_h2_em = break_section_text_elements(impact.find_elements(By.CSS_SELECTOR,'h2'))
        impact_h2_img = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h2 img'))
        impact_h2_yt = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        impact_h2_video = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        impact_h3, impact_h3_strong, impact_h3_a, impact_h3_em = break_section_text_elements(impact.find_elements(By.CSS_SELECTOR,'h3'))
        impact_h3_img = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h3 img'))
        impact_h3_yt = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        impact_h3_video = break_imgs(impact.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        impact_p, impact_p_strong, impact_p_a, impact_p_em = break_section_text_elements(impact.find_elements(By.CSS_SELECTOR,'p'))
        impact_p_img = break_imgs(impact.find_elements(By.CSS_SELECTOR,'p img'))
        impact_p_yt = break_imgs(impact.find_elements(By.CSS_SELECTOR,'p iframe'))
        impact_p_video = break_imgs(impact.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        impact_h2, impact_h2_strong, impact_h2_a, impact_h2_em, impact_h2_img, impact_h2_yt, impact_h2_video = None, None, None, None, None, None, None
        impact_h3, impact_h3_strong, impact_h3_a, impact_h3_em, impact_h3_img, impact_h3_yt, impact_h3_video = None, None, None, None, None, None, None
        impact_p, impact_p_strong, impact_p_a, impact_p_em, impact_p_img, impact_p_yt, impact_p_video = None, None, None, None, None, None, None
    
    return impact_h2, impact_h2_strong, impact_h2_a, impact_h2_em, impact_h2_img, impact_h2_yt, impact_h2_video, impact_h3, impact_h3_strong, impact_h3_a, impact_h3_em, impact_h3_img, impact_h3_yt, impact_h3_video, impact_p, impact_p_strong, impact_p_a, impact_p_em, impact_p_img, impact_p_yt, impact_p_video


# In[669]:


# pitch_funding
def funding():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            funding = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Funding"] div.js-pitch_content_details')
        except:
            funding = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Funding"] div.js-pitch_content')

        funding_h2, funding_h2_strong, funding_h2_a, funding_h2_em = break_section_text_elements(funding.find_elements(By.CSS_SELECTOR,'h2'))
        funding_h2_img = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h2 img'))
        funding_h2_yt = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        funding_h2_video = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        funding_h3, funding_h3_strong, funding_h3_a, funding_h3_em = break_section_text_elements(funding.find_elements(By.CSS_SELECTOR,'h3'))
        funding_h3_img = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h3 img'))
        funding_h3_yt = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        funding_h3_video = break_imgs(funding.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        funding_p, funding_p_strong, funding_p_a, funding_p_em = break_section_text_elements(funding.find_elements(By.CSS_SELECTOR,'p'))
        funding_p_img = break_imgs(funding.find_elements(By.CSS_SELECTOR,'p img'))
        funding_p_yt = break_imgs(funding.find_elements(By.CSS_SELECTOR,'p iframe'))
        funding_p_video = break_imgs(funding.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        funding_h2, funding_h2_strong, funding_h2_a, funding_h2_em, funding_h2_img, funding_h2_yt, funding_h2_video = None, None, None, None, None, None, None
        funding_h3, funding_h3_strong, funding_h3_a, funding_h3_em, funding_h3_img, funding_h3_yt, funding_h3_video = None, None, None, None, None, None, None
        funding_p, funding_p_strong, funding_p_a, funding_p_em, funding_p_img, funding_p_yt, funding_p_video = None, None, None, None, None, None, None
    
    return funding_h2, funding_h2_strong, funding_h2_a, funding_h2_em, funding_h2_img, funding_h2_yt, funding_h2_video, funding_h3, funding_h3_strong, funding_h3_a, funding_h3_em, funding_h3_img, funding_h3_yt, funding_h3_video, funding_p, funding_p_strong, funding_p_a, funding_p_em, funding_p_img, funding_p_yt, funding_p_video


# In[670]:


# pitch_founders
def founders():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            founders = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Founders"] div.js-pitch_content_details')
        except:
            founders = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Founders"] div.js-pitch_content')

        founders_h2, founders_h2_strong, founders_h2_a, founders_h2_em = break_section_text_elements(founders.find_elements(By.CSS_SELECTOR,'h2'))
        founders_h2_img = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h2 img'))
        founders_h2_yt = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        founders_h2_video = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        founders_h3, founders_h3_strong, founders_h3_a, founders_h3_em = break_section_text_elements(founders.find_elements(By.CSS_SELECTOR,'h3'))
        founders_h3_img = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h3 img'))
        founders_h3_yt = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        founders_h3_video = break_imgs(founders.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        founders_p, founders_p_strong, founders_p_a, founders_p_em = break_section_text_elements(founders.find_elements(By.CSS_SELECTOR,'p'))
        founders_p_img = break_imgs(founders.find_elements(By.CSS_SELECTOR,'p img'))
        founders_p_yt = break_imgs(founders.find_elements(By.CSS_SELECTOR,'p iframe'))
        founders_p_video = break_imgs(founders.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        founders_h2, founders_h2_strong, founders_h2_a, founders_h2_em, founders_h2_img, founders_h2_yt, founders_h2_video = None, None, None, None, None, None, None
        founders_h3, founders_h3_strong, founders_h3_a, founders_h3_em, founders_h3_img, founders_h3_yt, founders_h3_video = None, None, None, None, None, None, None
        founders_p, founders_p_strong, founders_p_a, founders_p_em, founders_p_img, founders_p_yt, founders_p_video = None, None, None, None, None, None, None
    
    return founders_h2, founders_h2_strong, founders_h2_a, founders_h2_em, founders_h2_img, founders_h2_yt, founders_h2_video, founders_h3, founders_h3_strong, founders_h3_a, founders_h3_em, founders_h3_img, founders_h3_yt, founders_h3_video, founders_p, founders_p_strong, founders_p_a, founders_p_em, founders_p_img, founders_p_yt, founders_p_video


# In[671]:


# pitch_summary
def summary():
    # 找找看有沒有這個區塊
    try:
        # 看看這個區塊有沒有 read more 那種一開始沒顯示的，有的話優先讀他
        try:
            summary = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Summary"] div.js-pitch_content_details')
        except:
            summary = driver.find_element(By.CSS_SELECTOR,'section[data-section-name="Summary"] div.js-pitch_content')

        summary_h2, summary_h2_strong, summary_h2_a, summary_h2_em = break_section_text_elements(summary.find_elements(By.CSS_SELECTOR,'h2'))
        summary_h2_img = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h2 img'))
        summary_h2_yt = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h2 iframe'))
        summary_h2_video = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h2 video source'))
        
        summary_h3, summary_h3_strong, summary_h3_a, summary_h3_em = break_section_text_elements(summary.find_elements(By.CSS_SELECTOR,'h3'))
        summary_h3_img = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h3 img'))
        summary_h3_yt = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h3 iframe'))
        summary_h3_video = break_imgs(summary.find_elements(By.CSS_SELECTOR,'h3 video source'))
        
        summary_p, summary_p_strong, summary_p_a, summary_p_em = break_section_text_elements(summary.find_elements(By.CSS_SELECTOR,'p'))
        summary_p_img = break_imgs(summary.find_elements(By.CSS_SELECTOR,'p img'))
        summary_p_yt = break_imgs(summary.find_elements(By.CSS_SELECTOR,'p iframe'))
        summary_p_video = break_imgs(summary.find_elements(By.CSS_SELECTOR,'p video source'))
    
    except:
        summary_h2, summary_h2_strong, summary_h2_a, summary_h2_em, summary_h2_img, summary_h2_yt, summary_h2_video = None, None, None, None, None, None, None
        summary_h3, summary_h3_strong, summary_h3_a, summary_h3_em, summary_h3_img, summary_h3_yt, summary_h3_video = None, None, None, None, None, None, None
        summary_p, summary_p_strong, summary_p_a, summary_p_em, summary_p_img, summary_p_yt, summary_p_video = None, None, None, None, None, None, None
    
    return summary_h2, summary_h2_strong, summary_h2_a, summary_h2_em, summary_h2_img, summary_h2_yt, summary_h2_video, summary_h3, summary_h3_strong, summary_h3_a, summary_h3_em, summary_h3_img, summary_h3_yt, summary_h3_video, summary_p, summary_p_strong, summary_p_a, summary_p_em, summary_p_img, summary_p_yt, summary_p_video


# 一樣的格式到此為止

# In[672]:


# pitch_about
def about():
    about = driver.find_elements(By.CSS_SELECTOR,'div[id="about"] .offerings-show-about_section__row')
    try:
        about_name = about[0].find_elements(By.CSS_SELECTOR,'div')[1].get_attribute('innerHTML')[1:-1]
    except:
        about_name = None
    try:
        about_founded = about[1].find_elements(By.CSS_SELECTOR,'div')[1].get_attribute('innerHTML')[1:-1]
    except:
        about_founded = None
    try:
        about_form = about[2].find_elements(By.CSS_SELECTOR,'div')[1].get_attribute('innerHTML')[1:-1]
    except:
        about_form = None
    try:    
        about_employees = about[3].find_elements(By.CSS_SELECTOR,'div')[1].get_attribute('innerHTML')[1:-1]
    except:
        about_employees = None
    try:
        about_website = about[4].find_element(By.CSS_SELECTOR,'div a').get_attribute('href')
    except:
        about_website = None
    try:
        about_fb = about[5].find_element(By.CSS_SELECTOR,'div a[title="Facebook"]').get_attribute('href')
    except:
        about_fb = None
    try:
        about_twitter = about[5].find_element(By.CSS_SELECTOR,'div a[title="Twitter"]').get_attribute('href')
    except:
        about_twitter = None
    try:
        about_ig = about[5].find_element(By.CSS_SELECTOR,'div a[title="Instagram"]').get_attribute('href')
    except:
        about_ig = None
    try:
        about_yt = about[5].find_element(By.CSS_SELECTOR,'div a[title="Youtube"]').get_attribute('href')
    except:
        about_yt = None
    try:
        about_linkedin = about[5].find_element(By.CSS_SELECTOR,'div a[title="Linkedin"]').get_attribute('href')
    except:
        about_linkedin = None
    try:
        about_map = driver.find_element(By.CSS_SELECTOR,'div[id="about"] .offerings-show-about_section__address img').get_attribute('src')
    except:
        about_map = None
    try:
        about_addr = driver.find_element(By.CSS_SELECTOR,'div[id="about"] .offerings-show-about_section__address div').get_attribute('innerHTML')[1:-1]    
    except:    
        about_addr = None
    return about_name, about_founded, about_form, about_employees, about_website, about_fb, about_twitter, about_ig, about_yt, about_linkedin, about_map, about_addr


# In[673]:


# pitch_team
def team():
    try:
        team = driver.find_elements(By.CSS_SELECTOR,'div[id="team"] .offerings-show-team_section__featured_team_member')
        team_img = []
        team_name = []
        team_position = []
        team_descript = []
        team_twitter = []
        team_linkedin = []
        team_angellist = []

        for i in team:
            try:
                team_img.append(i.find_element(By.CSS_SELECTOR,'img').get_attribute('src'))
            except:
                team_img.append(None)
            try:
                team_name.append(i.find_element(By.CSS_SELECTOR,'.s-marginTop1.s-fontSize20').get_attribute('innerHTML')[1:-1])
            except:
                team_name.append(None)
            try:
                team_position.append(i.find_element(By.CSS_SELECTOR,'.u-fontWeight400.s-fontSize16.u-colorGray7').get_attribute('innerHTML')[1:-1])
            except:
                team_position.append(None)
            try:
                team_descript.append(i.find_element(By.CSS_SELECTOR,'.s-fontSize14.u-fontWeight400.s-marginTop0_5').get_attribute('innerHTML')[1:-1])
            except:
                team_descript.append(None)
            try:
                team_twitter.append(i.find_element(By.CSS_SELECTOR,'a.c-link--twitter').get_attribute('href'))
            except:
                team_twitter.append(None)
            try:
                team_linkedin.append(i.find_element(By.CSS_SELECTOR,'a.c-link--linkedin').get_attribute('href'))
            except:
                team_linkedin.append(None)
            try:
                team_angellist.append(i.find_element(By.CSS_SELECTOR,'a.c-link--angellist').get_attribute('href'))
            except:
                team_angellist.append(None)
    except:
        team_img, team_name, team_position, team_descript, team_twitter, team_linkedin, team_angellist = None, None, None, None, None, None, None
    return team_img, team_name, team_position, team_descript, team_twitter, team_linkedin, team_angellist


# In[674]:


# pitch_press
def press():
    try:
        press = driver.find_elements(By.CSS_SELECTOR,'div[id="press"] a.press-article__article_link')
        press_link = []
        press_img = []
        press_title = []
        press_info_img = []
        press_info = []
        press_info_date = []
        press_p = []

        for i in press:
            try:
                press_link.append(i.get_attribute('href'))
            except:
                press_link.append(None)    
            try:
                press_img.append(i.find_element(By.CSS_SELECTOR,'div').get_attribute('style')[23:-3])
            except:
                press_img.append(None)
            try:
                press_title.append(i.find_element(By.CSS_SELECTOR,'.press-article__title').get_attribute('innerHTML')[1:-1])
            except:
                press_title.append(None)
            try:
                press_info_img.append(i.find_element(By.CSS_SELECTOR,'img').get_attribute('src'))
            except:
                press_info_img.append(None)
            try:
                press_info.append(i.find_element(By.CSS_SELECTOR,'img').get_attribute('title'))
            except:
                press_info.append(None)
            try:
                press_info_date.append(i.find_element(By.CSS_SELECTOR,'.press-article__info .u-displayInlineBlock.u-verticalAlignMiddle.u-colorGray8').get_attribute('innerHTML')[1:-1])
            except:
                press_info_date.append(None)
            try:
                press_p.append(i.find_element(By.CSS_SELECTOR,'p').get_attribute('innerHTML')[1:-1])
            except:
                press_p.append(None)
    except:
        press_link, press_img, press_title, press_info_img, press_info, press_info_date, press_p = None, None, None, None, None, None, None
    return press_link, press_img, press_title, press_info_img, press_info, press_info_date, press_p


# In[675]:


# pitch_FAQ
def FAQ():
    try:
        faq = driver.find_elements(By.CSS_SELECTOR,'div[id="faq"] .offerings-show-questions_section__question_container')
        faq_h4 = []
        faq_p = []

        for i in faq:
            try:
                faq_h4.append(i.find_element(By.CSS_SELECTOR,' h4').get_attribute('innerHTML')[1:-1])
            except:
                faq_h4.append(None)    
            try:
                faq_p.append(i.find_element(By.CSS_SELECTOR,' p').get_attribute('innerHTML'))
            except:
                faq_p.append(None)
    except:
        faq_h4, faq_p = None, None
    return faq_h4, faq_p


# In[676]:


# pitch_risks
def risks():
    try:
        risks = driver.find_elements(By.CSS_SELECTOR,'div[id="risks"] .offerings-show-risks_section__risk')
        risk_a = []
        risk_text = []

        for i in risks:
            try:
                risk_a.append(i.find_element(By.CSS_SELECTOR,' a').get_attribute('innerHTML'))
            except:
                risk_a.append(None)    
            try:
                risk_text.append(i.find_element(By.CSS_SELECTOR,' div').get_attribute('innerHTML')[1:-1])
            except:
                risk_text.append(None)
    except:
        risk_a, risk_text = None, None
    return risk_a, risk_text


# In[ ]:


# pitch_deal_terms_for_accredited_only
def deal_terms_accredited():
    deal_type, Round, Valuation, Allocation, Deadline, Instrument, Minimum_investment, Security_type, Valuation_cap, Pre_money_valuation = '', '', '', '', '', '', '', '', '', ''
    try:
        # 先抓出 deal_terms 的 block
        deal = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/flexible_deal_terms/item"]')
        deal = driver.find_elements(By.CSS_SELECTOR,'div[data-rc="offerings/show/flexible_deal_terms/item"]')
        
        for i in deal:
            
            temp = i.find_element(By.CSS_SELECTOR,'div.u-flexGrow.u-colorGray3').get_attribute('innerHTML')[1:-1]
            if temp[:10] == 'This is an':
                deal_type = temp
            else:
                temp_1 = i.find_element(By.CSS_SELECTOR,'div.offerings-show-flexible_deal_terms-item__value').get_attribute('innerHTML')[1:-1]
                if temp == 'Round':
                    Round = temp_1
                elif temp == 'Valuation':
                    Valuation = temp_1
                elif temp == 'Allocation':
                    Allocation = temp_1
                elif temp == 'Deadline' or temp == 'Closes on':
                    Deadline = temp_1
                elif temp == 'Instrument':
                    Instrument = temp_1
                elif temp == 'Minimum investment' or temp == 'Min. investment':
                    Minimum_investment = temp_1
                elif temp == 'Security type':
                    Security_type = temp_1
                elif temp == 'Valuation cap':
                    Valuation_cap = temp_1
                elif temp[:4] == 'Pre-':
                    Pre_money_valuation = temp_1
   
    except:
        deal = driver.find_elements(By.CSS_SELECTOR,'div.offerings-show-header-private_deal_terms__item')
        
        for i in deal:

            temp = i.find_element(By.CSS_SELECTOR,'div.u-fontWeight400.u-flexGrow').get_attribute('innerHTML')[1:-1]
            if temp[:10] == 'This is an':
                deal_type = temp
            else:
                temp_1 = i.find_element(By.CSS_SELECTOR,'div.offerings-show-header-private_deal_terms__value').get_attribute('innerHTML')[1:-1]
                for j in range(len(temp_1)):
                    if temp_1[j:j+2] == '<i':
                        temp_1 = temp_1[:j-1]
                        break
                if temp == 'Round':
                    Round = temp_1
                elif temp == 'Valuation':
                    Valuation = temp_1
                elif temp == 'Allocation':
                    Allocation = temp_1
                elif temp == 'Deadline' or temp == 'Closes on':
                    Deadline = i.find_element(By.CSS_SELECTOR,'div.offerings-show-header-private_deal_terms__value span').get_attribute('innerHTML')
                elif temp == 'Instrument':
                    Instrument = temp_1
                elif temp == 'Minimum investment' or temp == 'Min. investment':
                    Minimum_investment = temp_1
                elif temp == 'Security type':
                    Security_type = temp_1
                elif temp == 'Valuation cap':
                    Valuation_cap = temp_1
                elif temp[:4] == 'Pre-':
                    Pre_money_valuation = temp_1     
            
    return deal_type, Round, Valuation, Allocation, Deadline, Instrument, Minimum_investment, Security_type, Valuation_cap, Pre_money_valuation


# In[ ]:


# pitch_highlights_for_accredited_only
def highlight_summary():
    highlight = driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/pitch_highlights"]')
    try:
        highlight_title = break_elements(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__title'))
        highlight_description = break_elements(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__description'))
        highlight_icon = break_imgs(highlight.find_elements(By.CSS_SELECTOR,'.c-tag-highlight__icon img'))
    except:
        highlight_title = None
        highlight_description = None
        highlight_icon = None
    highlight_summary = highlight.find_element(By.CSS_SELECTOR,'.offerings-show-summary__content p').get_attribute('innerHTML')[1:-1]
    highlight_content = break_elements_within_cut(highlight.find_elements(By.CSS_SELECTOR,'.offerings-show-pitch_highlights__content li'))
    return highlight_title, highlight_description, highlight_icon, highlight_summary, highlight_content


# ## 爬！

# ### Funding

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome('./chromedriver')


# In[543]:


def run_funding_accredited(url):
    
    csv = []
    csv_co = []
    csv_doc = []
    csv_team = []
    csv_press = []
    csv_FAQ = []
    csv_risk = []
    
    csv.append(url)
    
    x = title()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    x = sidebar()
    for y in range(8):
        csv.append(x[y])

    x = co_investors()
    if x != ([], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_co.append([])
            csv_co[y].append(url)
            for z in range(5):
                if x[z] != []:
                    csv_co[y].append(x[z][y])
                else:
                    csv_co[y].append([])

    x = deal_terms()
    for y in range(8):
        csv.append(x[y])
    if x[8] == None:
        csv.append(None)
        for y in range(8, 12):
            csv.append(x[y])
    else:
        temp = x[8].split(' – ')
        csv.append(temp[0])
        csv.append(temp[1][1:])
        csv.append(x[9])
        csv.append(x[10])
        csv.append(x[11])
        
    x = document()
    csv.append(x[0])
    if x[1] != []:
        for y in range(len(x[1])):
            csv_doc.append([])
            csv_doc[y].append(url)
            csv_doc[y].append(x[1][y])
            csv_doc[y].append(x[2][y])
            
    x = bonus_perks()
    for y in range(5):
        csv.append(x[y])
        
    x = highlights()
    for y in range(4):
        csv.append(x[y])
    
    l = []  
    l.append(problem())
    l.append(solution())
    l.append(product())
    l.append(traction())
    l.append(customers())
    l.append(biz())
    l.append(market())
    l.append(competition())
    l.append(vision())
    l.append(impact())
    l.append(funding())
    l.append(founders())
    l.append(summary())
    
    for y in range(13):
        for z in range(21):
            csv.append(l[y][z])
    
    x = about()
    for y in range(12):
        csv.append(x[y])
        
    x = team()
    for y in range(len(x[0])):
        csv_team.append([])
        csv_team[y].append(url)
        for z in range(7):
            csv_team[y].append(x[z][y])
            
    x = press()
    if x != ([], [], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_press.append([])
            csv_press[y].append(url)
            for z in range(7):
                csv_press[y].append(x[z][y])

    x = FAQ()
    if x != ([], []):
        for y in range(len(x[0])):
            csv_FAQ.append([])
            csv_FAQ[y].append(url)
            csv_FAQ[y].append(x[0][y])
            csv_FAQ[y].append(x[1][y])
            
    x = risks()
    if x != ([], []):
        for y in range(len(x[0])):
            csv_risk.append([])
            csv_risk[y].append(url)
            csv_risk[y].append(x[0][y])
            csv_risk[y].append(x[1][y])
            
    x = media()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    # followers, now
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/footer"] span.follows-shared-follow_offering__bubble-counter').get_attribute('innerHTML')[1:-1])    
        csv.append(time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()))
    except:
        csv.append([])
        csv.append([])
    
    # discussion, updates, reviews num
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#discussion"] span').get_attribute('innerHTML')[1:-1])  
    except:
        csv.append([])
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#updates"] span').get_attribute('innerHTML')[1:-1])
    except:
        csv.append([])
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#reviews"] span').get_attribute('innerHTML')[1:-1])    
    except:
        csv.append([])
    
    return csv, csv_co, csv_doc, csv_team, csv_FAQ, csv_risk, csv_press


# In[543]:


def run_funding(url):
    
    csv = []
    csv_co = []
    csv_doc = []
    csv_team = []
    csv_press = []
    csv_FAQ = []
    csv_risk = []
    
    csv.append(url)
    
    x = title()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    x = sidebar()
    for y in range(8):
        csv.append(x[y])

    x = co_investors()
    if x != ([], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_co.append([])
            csv_co[y].append(url)
            for z in range(5):
                if x[z] != []:
                    csv_co[y].append(x[z][y])
                else:
                    csv_co[y].append([])

    x = deal_terms()
    for y in range(8):
        csv.append(x[y])
    if x[8] == None:
        csv.append(None)
        for y in range(8, 12):
            csv.append(x[y])
    else:
        temp = x[8].split(' – ')
        csv.append(temp[0])
        csv.append(temp[1][1:])
        csv.append(x[9])
        csv.append(x[10])
        csv.append(x[11])
        
    x = document()
    csv.append(x[0])
    if x[1] != []:
        for y in range(len(x[1])):
            csv_doc.append([])
            csv_doc[y].append(url)
            csv_doc[y].append(x[1][y])
            csv_doc[y].append(x[2][y])
            
    x = bonus_perks()
    for y in range(5):
        csv.append(x[y])
        
    x = highlights()
    for y in range(4):
        csv.append(x[y])
    
    l = []  
    l.append(problem())
    l.append(solution())
    l.append(product())
    l.append(traction())
    l.append(customers())
    l.append(biz())
    l.append(market())
    l.append(competition())
    l.append(vision())
    l.append(impact())
    l.append(funding())
    l.append(founders())
    l.append(summary())
    
    for y in range(13):
        for z in range(21):
            csv.append(l[y][z])
    
    x = about()
    for y in range(12):
        csv.append(x[y])
        
    x = team()
    for y in range(len(x[0])):
        csv_team.append([])
        csv_team[y].append(url)
        for z in range(7):
            csv_team[y].append(x[z][y])
            
    x = press()
    if x != ([], [], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_press.append([])
            csv_press[y].append(url)
            for z in range(7):
                csv_press[y].append(x[z][y])

    x = FAQ()
    if x != ([], []):
        for y in range(len(x[0])):
            csv_FAQ.append([])
            csv_FAQ[y].append(url)
            csv_FAQ[y].append(x[0][y])
            csv_FAQ[y].append(x[1][y])
            
    x = risks()
    if x != ([], []):
        for y in range(len(x[0])):
            csv_risk.append([])
            csv_risk[y].append(url)
            csv_risk[y].append(x[0][y])
            csv_risk[y].append(x[1][y])
            
    x = media()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    # followers, now
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/footer"] span.follows-shared-follow_offering__bubble-counter').get_attribute('innerHTML')[1:-1])    
        csv.append(time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()))
    except:
        csv.append([])
        csv.append([])
    
    # discussion, updates, reviews num
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#discussion"] span').get_attribute('innerHTML')[1:-1])  
    except:
        csv.append([])
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#updates"] span').get_attribute('innerHTML')[1:-1])
    except:
        csv.append([])
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#reviews"] span').get_attribute('innerHTML')[1:-1])    
    except:
        csv.append([])
    
    return csv, csv_co, csv_doc, csv_team, csv_FAQ, csv_risk, csv_press


# In[413]:


import pandas as pd

df = pd.read_csv('Funding.csv')

fail = []
csv = []
csv_co = []
csv_doc = []
csv_team = []
csv_FAQ = []
csv_risk = []
csv_press = []

s = set()
project_tags = []

for i in df['project_url']:
    print()
    print()
    print()
    driver.get(i)
    
    try:
        temp = run_funding(i)
    except Exception as e:
        print(e)
        temp = ([], [], [], [], [], [], [])
        fail.append(i)
    
    csv.append(temp[0])
    csv_co.append(temp[1])
    csv_doc.append(temp[2])
    csv_team.append(temp[3])
    csv_FAQ.append(temp[4])
    csv_risk.append(temp[5])
    csv_press.append(temp[6])
    
    l = []
    try:
        tags = driver.find_elements(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/title"] div[data-rc="offerings/shared/tags"] a')
        for i in tags:
            l.append(i.get_attribute('innerHTML'))
            s.add(i.get_attribute('innerHTML'))
    except:
        fail2.append(i)
    project_tags.append(l)
    print(l)
    


# In[439]:


tags = dict.fromkeys(s, 0)
tags.values()


# In[440]:


l = []
for i in project_tags:
    tags = dict.fromkeys(s, 0)
    for j in i:
        tags[j] = 1
    l.append(tuple(tags.values()))


# In[447]:


ss ={'tag_Special',
 'tag_AAPI Founders',
 'tag_AI & Machine Learning',
 'tag_Adtech',
 'tag_Apparel & Accessories',
 'tag_Apps',
 'tag_Architecture & Design Services',
 'tag_Arts & Entertainment',
 'tag_Automotive',
 'tag_Aviation',
 'tag_B2B',
 'tag_B2C',
 'tag_Big Data',
 'tag_Biotechnology',
 'tag_Black Founders',
 'tag_Blockchain',
 'tag_Cannabis',
 'tag_Charity',
 'tag_Childhood Education',
 'tag_Cloud Computing',
 'tag_Combat Carbon',
 'tag_Coming Soon',
 'tag_Consumer Electronics',
 'tag_Consumer Goods & Retail',
 'tag_Creator Economy',
 'tag_Crowd SAFE',
 'tag_Crypto',
 'tag_Cyber Security & Privacy',
 'tag_D2C',
 'tag_Debt',
 'tag_Deep Tech',
 'tag_Delivery Services',
 'tag_Disaster Relief',
 'tag_Diverse Founders',
 'tag_Diversity & Inclusion',
 'tag_Drinks',
 'tag_Edtech',
 'tag_Edtech & Education',
 'tag_Electric Vehicles (EVs)',
 'tag_Ethically Made',
 'tag_Fashion',
 'tag_Fintech',
 'tag_Fitness',
 'tag_Food',
 'tag_Food & Drinks',
 'tag_Fundraising',
 'tag_Green Power',
 'tag_Hardware',
 'tag_Health & Wellness',
 'tag_Healthcare',
 'tag_Healthcare Facilities & Equipment',
 'tag_Healthcare Services',
 'tag_Healthtech',
 'tag_Hotels & Hospitality',
 'tag_Household Goods',
 'tag_Immigrant Founders',
 'tag_Industrial Automation',
 'tag_Industrial Operations & Management',
 'tag_Insuretech',
 'tag_IoT',
 'tag_Kids',
 'tag_LGBTQIA+ Founders',
 'tag_Latinx Founders',
 'tag_Local',
 'tag_Luxury',
 'tag_Manufacturing',
 'tag_Marketplace',
 'tag_Media Production & Curation',
 'tag_Mental Wellness',
 'tag_Music',
 'tag_Nutrition',
 'tag_P2P',
 'tag_Personal Care',
 'tag_Pharmaceauticals & Medicine',
 'tag_Plant-Based',
 'tag_Property Sharing & Rentals',
 'tag_Reduce, Reuse, Recycle',
 'tag_Renewables',
 'tag_Restaurant & Bar Services',
 'tag_Robotics',
 'tag_SaaS',
 'tag_Services',
 'tag_Sleep',
 'tag_Smart Devices',
 'tag_Social Impact',
 'tag_Social Justice',
 'tag_Social Media + Networks',
 'tag_Software & SaaS',
 'tag_Sports',
 'tag_Stock Purchase Agreement (SPA)',
 'tag_Subscription',
 'tag_Supplements',
 'tag_Sustainability',
 'tag_Telecom',
 'tag_Token',
 'tag_Token Purchase Agreement (TPA)',
 'tag_Transportation',
 'tag_Veteran Founders',
 'tag_Video & Streaming',
 'tag_Waste Management & Sanitation',
 'tag_Wealth Management',
 'tag_Wearables',
 'tag_Wellbeing & Longevity',
 'tag_Women Founders'}


# In[437]:



funding_columns = [
    'project_url',
    'title_img', 'title_maintitle', 'title_subtitle',
    'sidebar_raised_type', 'sidebar_raised_amount', 'sidebar_raised_subtitle', 'sidebar_investors', 'sidebar_investors_subtitle', 'sidebar_left', 'sidebar_closed_date', 'sidebar_success',
    'valuation_cap_type', 'valuation_cap', 'discount', 'min_investment_type', 'min_investment', 'max_investment_type', 'max_investment', 'funding_goal_type', 'funding_goal_bottom', 'funding_goal_top', 'deadline', 'security', 'nominee',
    'document_descript',
    'perk_investor', 'perk_amount', 'perk_amount_type', 'perk_receive', 'perk_limit',
    'highlight_title', 'highlight_description', 'highlight_icon', 'highlight_content',
    'problem_h2', 'problem_h2_strong', 'problem_h2_a', 'problem_h2_em', 'problem_h2_img', 'problem_h2_yt','problem_h2_video', 'problem_h3', 'problem_h3_strong', 'problem_h3_a', 'problem_h3_em', 'problem_h3_img', 'problem_h3_yt', 'problem_h3_video', 'problem_p', 'problem_p_strong', 'problem_p_a', 'problem_p_em', 'problem_p_img', 'problem_p_yt', 'problem_p_video',
    'solution_h2', 'solution_h2_strong', 'solution_h2_a', 'solution_h2_em', 'solution_h2_img', 'solution_h2_yt','solution_h2_video', 'solution_h3', 'solution_h3_strong', 'solution_h3_a', 'solution_h3_em', 'solution_h3_img', 'solution_h3_yt', 'solution_h3_video', 'solution_p', 'solution_p_strong', 'solution_p_a', 'solution_p_em', 'solution_p_img', 'solution_p_yt', 'solution_p_video',
    'product_h2', 'product_h2_strong', 'product_h2_a', 'product_h2_em', 'product_h2_img', 'product_h2_yt','product_h2_video', 'product_h3', 'product_h3_strong', 'product_h3_a', 'product_h3_em', 'product_h3_img', 'product_h3_yt', 'product_h3_video', 'product_p', 'product_p_strong', 'product_p_a', 'product_p_em', 'product_p_img', 'product_p_yt', 'product_p_video',
    'traction_h2', 'traction_h2_strong', 'traction_h2_a', 'traction_h2_em', 'traction_h2_img', 'traction_h2_yt','traction_h2_video', 'traction_h3', 'traction_h3_strong', 'traction_h3_a', 'traction_h3_em', 'traction_h3_img', 'traction_h3_yt', 'traction_h3_video', 'traction_p', 'traction_p_strong', 'traction_p_a', 'traction_p_em', 'traction_p_img', 'traction_p_yt', 'traction_p_video',
    'customers_h2', 'customers_h2_strong', 'customers_h2_a', 'customers_h2_em', 'customers_h2_img', 'customers_h2_yt','customers_h2_video', 'customers_h3', 'customers_h3_strong', 'customers_h3_a', 'customers_h3_em', 'customers_h3_img', 'customers_h3_yt', 'customers_h3_video', 'customers_p', 'customers_p_strong', 'customers_p_a', 'customers_p_em', 'customers_p_img', 'customers_p_yt', 'customers_p_video',
    'biz_h2', 'biz_h2_strong', 'biz_h2_a', 'biz_h2_em', 'biz_h2_img', 'biz_h2_yt','biz_h2_video', 'biz_h3', 'biz_h3_strong', 'biz_h3_a', 'biz_h3_em', 'biz_h3_img', 'biz_h3_yt', 'biz_h3_video', 'biz_p', 'biz_p_strong', 'biz_p_a', 'biz_p_em', 'biz_p_img', 'biz_p_yt', 'biz_p_video',
    'market_h2', 'market_h2_strong', 'market_h2_a', 'market_h2_em', 'market_h2_img', 'h2_yt','market_h2_video', 'market_h3', 'market_h3_strong', 'market_h3_a', 'market_h3_em', 'market_h3_img', 'h3_yt', 'market_h3_video', 'market_p', 'market_p_strong', 'market_p_a', 'market_p_em', 'market_p_img', 'p_yt', 'market_p_video',
    'competition_h2', 'competition_h2_strong', 'competition_h2_a', 'competition_h2_em', 'competition_h2_img', 'competition_h2_yt','competition_h2_video', 'competition_h3', 'competition_h3_strong', 'competition_h3_a', 'competition_h3_em', 'competition_h3_img', 'competition_h3_yt', 'competition_h3_video', 'competition_p', 'competition_p_strong', 'competition_p_a', 'competition_p_em', 'competition_p_img', 'competition_p_yt', 'competition_p_video',
    'vision_h2', 'vision_h2_strong', 'vision_h2_a', 'vision_h2_em', 'vision_h2_img', 'vision_h2_yt','vision_h2_video', 'vision_h3', 'vision_h3_strong', 'vision_h3_a', 'vision_h3_em', 'vision_h3_img', 'vision_h3_yt', 'vision_h3_video', 'vision_p', 'vision_p_strong', 'vision_p_a', 'vision_p_em', 'vision_p_img', 'vision_p_yt', 'vision_p_video',
    'impact_h2', 'impact_h2_strong', 'impact_h2_a', 'impact_h2_em', 'impact_h2_img', 'impact_h2_yt','impact_h2_video', 'impact_h3', 'impact_h3_strong', 'impact_h3_a', 'impact_h3_em', 'impact_h3_img', 'impact_h3_yt', 'impact_h3_video', 'impact_p', 'impact_p_strong', 'impact_p_a', 'impact_p_em', 'impact_p_img', 'impact_p_yt', 'impact_p_video',
    'funding_h2', 'funding_h2_strong', 'funding_h2_a', 'funding_h2_em', 'funding_h2_img', 'funding_h2_yt','funding_h2_video', 'funding_h3', 'funding_h3_strong', 'funding_h3_a', 'funding_h3_em', 'funding_h3_img', 'funding_h3_yt', 'funding_h3_video', 'funding_p', 'funding_p_strong', 'funding_p_a', 'funding_p_em', 'funding_p_img', 'funding_p_yt', 'funding_p_video',
    'founders_h2', 'founders_h2_strong', 'founders_h2_a', 'founders_h2_em', 'founders_h2_img', 'founders_h2_yt','founders_h2_video', 'founders_h3', 'founders_h3_strong', 'founders_h3_a', 'founders_h3_em', 'founders_h3_img', 'founders_h3_yt', 'founders_h3_video', 'founders_p', 'founders_p_strong', 'founders_p_a', 'founders_p_em', 'founders_p_img', 'founders_p_yt', 'founders_p_video',
    'summary_h2', 'summary_h2_strong', 'summary_h2_a', 'summary_h2_em', 'summary_h2_img', 'summary_h2_yt','summary_h2_video', 'summary_h3', 'summary_h3_strong', 'summary_h3_a', 'summary_h3_em', 'summary_h3_img', 'summary_h3_yt', 'summary_h3_video', 'summary_p', 'summary_p_strong', 'summary_p_a', 'summary_p_em', 'summary_p_img', 'summary_p_yt', 'summary_p_video',
    'about_name', 'about_founded', 'about_form', 'about_employees', 'about_website', 'about_fb', 'about_twitter', 'about_ig', 'about_yt', 'about_linkedin', 'about_map', 'about_addr', 
    'main_img', 'main_yt', 'main_video',
    'followers', 'now',
    'discussion_num', 'updates_num', 'reviews_num'
]

funding_doc_columns = ['project_url', 'doc_link', 'doc_name']
funding_team_columns = ['project_url','team_img', 'team_name', 'team_position', 'team_descript', 'team_twitter', 'team_linkedin', 'team_angellist']
funding_press_columns = ['project_url', 'press_link', 'press_img', 'press_title', 'press_info_img', 'press_info', 'press_info_date', 'press_p']
funding_FAQ_columns = ['project_url', 'faq_h4', 'faq_p']
funding_risk_columns = ['project_url', 'risk_a', 'risk_text']
funding_co_columns = ['project_url','external_investors', 'external_subtitle', 'external_description', 'external_img', 'external_also']

a1 = pd.DataFrame(columns = funding_columns, data = csv)
b1 = pd.DataFrame(columns = list(ss), data = l)
a1.to_csv('Funding/Funding_projects.csv',index = False)
b2 = pd.concat([a1, b1],axis=1)
b2.to_csv('Funding/Funding_projects_with_tag.csv',index = False)

for i in csv_doc:
    if i != []:
        print(i[0][0][20:])
        a2 = pd.DataFrame(columns = funding_doc_columns, data = i)
        a2.to_csv('Funding/documents/' + str(i[0][0][20:]) + '.csv',index = False)
        print('')

for i in csv_team:
    if i != []:
        a3 = pd.DataFrame(columns = funding_team_columns, data = i)
        a3.to_csv('Funding/team/' + str(i[0][0][20:]) + '.csv',index = False)
        
for i in csv_FAQ:
    if i != []:
        a4 = pd.DataFrame(columns = funding_FAQ_columns, data = i)
        a4.to_csv('Funding/FAQ/' + str(i[0][0][20:]) + '.csv',index = False)
        
for i in csv_risk:
    if i != []:
        a5 = pd.DataFrame(columns = funding_risk_columns, data = i)
        a5.to_csv('Funding/risk/' + str(i[0][0][20:]) + '.csv',index = False)

for i in csv_co:
    if i != []:        
        a6 = pd.DataFrame(columns = funding_co_columns, data = i)
        a6.to_csv('Funding/co_invest/' + str(i[0][0][20:]) + '.csv',index = False)

for i in csv_press:
    if i != []:        
        a7 = pd.DataFrame(columns = funding_press_columns, data = i)
        a7.to_csv('Funding/press/' + str(i[0][0][20:]) + '.csv',index = False)


# In[448]:


fail


# In[449]:


fail2


# ### Funded

# In[450]:


def run_funded(url):
    
    csv = []
    csv_co = []
    csv_doc = []
    csv_team = []
    csv_press = []
    
    csv.append(url)
    
    x = title()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    x = sidebar()
    for y in range(8):
        csv.append(x[y])

    x = co_investors()
    if x != ([], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_co.append([])
            csv_co[y].append(url)
            for z in range(5):
                csv_co[y].append(x[z][y])

    x = deal_terms()
    for y in range(8):
        csv.append(x[y])
    if x[8] == None:
        csv.append(None)
        for y in range(8, 12):
            csv.append(x[y])
    else:
        temp = x[8].split(' – ')
        csv.append(temp[0])
        csv.append(temp[1][1:])
        csv.append(x[9])
        csv.append(x[10])
        csv.append(x[11])
        
    x = document()
    csv.append(x[0])
    if x[1] != []:
        for y in range(len(x[1])):
            csv_doc.append([])
            csv_doc[y].append(url)
            csv_doc[y].append(x[1][y])
            csv_doc[y].append(x[2][y])
            
    x = highlights()
    for y in range(4):
        csv.append(x[y])
    
    l = []  
    l.append(problem())
    l.append(solution())
    l.append(product())
    l.append(traction())
    l.append(customers())
    l.append(biz())
    l.append(market())
    l.append(competition())
    l.append(vision())
    l.append(impact())
    l.append(funding())
    l.append(founders())
    l.append(summary())
    
    for y in range(13):
        for z in range(21):
            csv.append(l[y][z])
    
    x = about()
    for y in range(12):
        csv.append(x[y])
        
    x = team()
    for y in range(len(x[0])):
        csv_team.append([])
        csv_team[y].append(url)
        for z in range(7):
            csv_team[y].append(x[z][y])
            
    x = press()
    if x != ([], [], [], [], [], [], []):
        for y in range(len(x[0])):
            csv_press.append([])
            csv_press[y].append(url)
            for z in range(7):
                csv_press[y].append(x[z][y])

    x = media()
    csv.append(x[0])
    csv.append(x[1])
    csv.append(x[2])
    
    # followers, now
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/footer"] span.follows-shared-follow_offering__bubble-counter').get_attribute('innerHTML')[1:-1])    
        csv.append(time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime()))
    except:
        csv.append([])
        csv.append([])
    try:    
        csv.append(driver.find_element(By.CSS_SELECTOR,'div[data-rc="offerings/show/footer"] .s-marginTop1_5.s-fontSize18.u-fontWeight500.u-colorGreen').get_attribute('innerHTML')[1:-1]) 
    except:
        csv.append([])
    
    # updates, reviews num
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#updates"] span').get_attribute('innerHTML')[1:-1])
    except:
        csv.append([])
    try:
        csv.append(driver.find_element(By.CSS_SELECTOR,'nav[data-rc="offerings/show/content_navigation"] a[href="#reviews"] span').get_attribute('innerHTML')[1:-1])    
    except:
        csv.append([])
    
    return csv, csv_co, csv_doc, csv_team, csv_press


# In[451]:


df = pd.read_csv('Funded.csv')

fail3 = []
csv = []
csv_co = []
csv_doc = []
csv_team = []
csv_press = []

s = set()
project_tags = []
fail4 = []

for i in df['project_url']:
    print()
    print()
    print()
    driver.get(i)
    
    try:
        temp = run_funded(i)
    except Exception as e:
        print(e)
        temp = ([], [], [], [], [])
        fail3.append(i)
    
    csv.append(temp[0])
    csv_co.append(temp[1])
    csv_doc.append(temp[2])
    csv_team.append(temp[3])
    csv_press.append(temp[4])
    
    l = []
    try:
        tags = driver.find_elements(By.CSS_SELECTOR,'div[data-rc="offerings/show/header/title"] div[data-rc="offerings/shared/tags"] a')
        for i in tags:
            l.append(i.get_attribute('innerHTML'))
            s.add(i.get_attribute('innerHTML'))
    except:
        fail4.append(i)
    project_tags.append(l)
    print(l)
    


# In[452]:


l = []
for i in project_tags:
    tags = dict.fromkeys(s, 0)
    for j in i:
        tags[j] = 1
    l.append(tuple(tags.values()))


# In[465]:


funded_columns = [
    'project_url',
    'title_img', 'title_maintitle', 'title_subtitle',
    'sidebar_raised_type', 'sidebar_raised_amount', 'sidebar_raised_subtitle', 'sidebar_investors', 'sidebar_investors_subtitle', 'sidebar_left', 'sidebar_closed_date', 'sidebar_success',
    'valuation_cap_type', 'valuation_cap', 'discount', 'min_investment_type', 'min_investment', 'max_investment_type', 'max_investment', 'funding_goal_type', 'funding_goal_bottom', 'funding_goal_top', 'deadline', 'security', 'nominee',
    'document_descript',
    'highlight_title', 'highlight_description', 'highlight_icon', 'highlight_content',
    'problem_h2', 'problem_h2_strong', 'problem_h2_a', 'problem_h2_em', 'problem_h2_img', 'problem_h2_yt','problem_h2_video', 'problem_h3', 'problem_h3_strong', 'problem_h3_a', 'problem_h3_em', 'problem_h3_img', 'problem_h3_yt', 'problem_h3_video', 'problem_p', 'problem_p_strong', 'problem_p_a', 'problem_p_em', 'problem_p_img', 'problem_p_yt', 'problem_p_video',
    'solution_h2', 'solution_h2_strong', 'solution_h2_a', 'solution_h2_em', 'solution_h2_img', 'solution_h2_yt','solution_h2_video', 'solution_h3', 'solution_h3_strong', 'solution_h3_a', 'solution_h3_em', 'solution_h3_img', 'solution_h3_yt', 'solution_h3_video', 'solution_p', 'solution_p_strong', 'solution_p_a', 'solution_p_em', 'solution_p_img', 'solution_p_yt', 'solution_p_video',
    'product_h2', 'product_h2_strong', 'product_h2_a', 'product_h2_em', 'product_h2_img', 'product_h2_yt','product_h2_video', 'product_h3', 'product_h3_strong', 'product_h3_a', 'product_h3_em', 'product_h3_img', 'product_h3_yt', 'product_h3_video', 'product_p', 'product_p_strong', 'product_p_a', 'product_p_em', 'product_p_img', 'product_p_yt', 'product_p_video',
    'traction_h2', 'traction_h2_strong', 'traction_h2_a', 'traction_h2_em', 'traction_h2_img', 'traction_h2_yt','traction_h2_video', 'traction_h3', 'traction_h3_strong', 'traction_h3_a', 'traction_h3_em', 'traction_h3_img', 'traction_h3_yt', 'traction_h3_video', 'traction_p', 'traction_p_strong', 'traction_p_a', 'traction_p_em', 'traction_p_img', 'traction_p_yt', 'traction_p_video',
    'customers_h2', 'customers_h2_strong', 'customers_h2_a', 'customers_h2_em', 'customers_h2_img', 'customers_h2_yt','customers_h2_video', 'customers_h3', 'customers_h3_strong', 'customers_h3_a', 'customers_h3_em', 'customers_h3_img', 'customers_h3_yt', 'customers_h3_video', 'customers_p', 'customers_p_strong', 'customers_p_a', 'customers_p_em', 'customers_p_img', 'customers_p_yt', 'customers_p_video',
    'biz_h2', 'biz_h2_strong', 'biz_h2_a', 'biz_h2_em', 'biz_h2_img', 'biz_h2_yt','biz_h2_video', 'biz_h3', 'biz_h3_strong', 'biz_h3_a', 'biz_h3_em', 'biz_h3_img', 'biz_h3_yt', 'biz_h3_video', 'biz_p', 'biz_p_strong', 'biz_p_a', 'biz_p_em', 'biz_p_img', 'biz_p_yt', 'biz_p_video',
    'market_h2', 'market_h2_strong', 'market_h2_a', 'market_h2_em', 'market_h2_img', 'h2_yt','market_h2_video', 'market_h3', 'market_h3_strong', 'market_h3_a', 'market_h3_em', 'market_h3_img', 'h3_yt', 'market_h3_video', 'market_p', 'market_p_strong', 'market_p_a', 'market_p_em', 'market_p_img', 'p_yt', 'market_p_video',
    'competition_h2', 'competition_h2_strong', 'competition_h2_a', 'competition_h2_em', 'competition_h2_img', 'competition_h2_yt','competition_h2_video', 'competition_h3', 'competition_h3_strong', 'competition_h3_a', 'competition_h3_em', 'competition_h3_img', 'competition_h3_yt', 'competition_h3_video', 'competition_p', 'competition_p_strong', 'competition_p_a', 'competition_p_em', 'competition_p_img', 'competition_p_yt', 'competition_p_video',
    'vision_h2', 'vision_h2_strong', 'vision_h2_a', 'vision_h2_em', 'vision_h2_img', 'vision_h2_yt','vision_h2_video', 'vision_h3', 'vision_h3_strong', 'vision_h3_a', 'vision_h3_em', 'vision_h3_img', 'vision_h3_yt', 'vision_h3_video', 'vision_p', 'vision_p_strong', 'vision_p_a', 'vision_p_em', 'vision_p_img', 'vision_p_yt', 'vision_p_video',
    'impact_h2', 'impact_h2_strong', 'impact_h2_a', 'impact_h2_em', 'impact_h2_img', 'impact_h2_yt','impact_h2_video', 'impact_h3', 'impact_h3_strong', 'impact_h3_a', 'impact_h3_em', 'impact_h3_img', 'impact_h3_yt', 'impact_h3_video', 'impact_p', 'impact_p_strong', 'impact_p_a', 'impact_p_em', 'impact_p_img', 'impact_p_yt', 'impact_p_video',
    'funding_h2', 'funding_h2_strong', 'funding_h2_a', 'funding_h2_em', 'funding_h2_img', 'funding_h2_yt','funding_h2_video', 'funding_h3', 'funding_h3_strong', 'funding_h3_a', 'funding_h3_em', 'funding_h3_img', 'funding_h3_yt', 'funding_h3_video', 'funding_p', 'funding_p_strong', 'funding_p_a', 'funding_p_em', 'funding_p_img', 'funding_p_yt', 'funding_p_video',
    'founders_h2', 'founders_h2_strong', 'founders_h2_a', 'founders_h2_em', 'founders_h2_img', 'founders_h2_yt','founders_h2_video', 'founders_h3', 'founders_h3_strong', 'founders_h3_a', 'founders_h3_em', 'founders_h3_img', 'founders_h3_yt', 'founders_h3_video', 'founders_p', 'founders_p_strong', 'founders_p_a', 'founders_p_em', 'founders_p_img', 'founders_p_yt', 'founders_p_video',
    'summary_h2', 'summary_h2_strong', 'summary_h2_a', 'summary_h2_em', 'summary_h2_img', 'summary_h2_yt','summary_h2_video', 'summary_h3', 'summary_h3_strong', 'summary_h3_a', 'summary_h3_em', 'summary_h3_img', 'summary_h3_yt', 'summary_h3_video', 'summary_p', 'summary_p_strong', 'summary_p_a', 'summary_p_em', 'summary_p_img', 'summary_p_yt', 'summary_p_video',
    'about_name', 'about_founded', 'about_form', 'about_employees', 'about_website', 'about_fb', 'about_twitter', 'about_ig', 'about_yt', 'about_linkedin', 'about_map', 'about_addr', 
    'main_img', 'main_yt', 'main_video',
    'followers', 'now', 'green_line',
    'updates_num', 'reviews_num'
]

funded_doc_columns = ['project_url', 'doc_link', 'doc_name']
funded_team_columns = ['project_url','team_img', 'team_name', 'team_position', 'team_descript', 'team_twitter', 'team_linkedin', 'team_angellist']
funded_press_columns = ['project_url', 'press_link', 'press_img', 'press_title', 'press_info_img', 'press_info', 'press_info_date', 'press_p']
funded_co_columns = ['project_url','external_investors', 'external_subtitle', 'external_description', 'external_img', 'external_also']

a1 = pd.DataFrame(columns = funded_columns, data = csv)
b1 = pd.DataFrame(columns = list(s), data = l)
a1.to_csv('Funded/Funded_projects.csv',index = False)
b2 = pd.concat([a1, b1],axis=1)
b2.to_csv('Funded/Funded_projects_with_tag.csv',index = False)

for i in csv_doc:
    if i != []:
        print(i[0][0][20:])
        a2 = pd.DataFrame(columns = funded_doc_columns, data = i)
        a2.to_csv('Funded/documents/' + str(i[0][0][20:]) + '.csv',index = False)
        print('')

for i in csv_team:
    if i != []:
        a3 = pd.DataFrame(columns = funded_team_columns, data = i)
        a3.to_csv('Funded/team/' + str(i[0][0][20:]) + '.csv',index = False)
        
for i in csv_co:
    if i != []:        
        a6 = pd.DataFrame(columns = funded_co_columns, data = i)
        a6.to_csv('Funded/co_invest/' + str(i[0][0][20:]) + '.csv',index = False)
        
for i in csv_press:
    if i != []:        
        a7 = pd.DataFrame(columns = funded_press_columns, data = i)
        a7.to_csv('Funded/press/' + str(i[0][0][20:]) + '.csv',index = False)


# In[468]:


len(fail3)


# In[469]:


fail3


# In[470]:


fail4

