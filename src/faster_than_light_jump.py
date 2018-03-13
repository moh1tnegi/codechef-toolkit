""" Yeah, FTLJ. The script gathers usernames from dynamic js api"""
from collections import defaultdict
from selenium import webdriver
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import json

if __name__ == '__main__':
    url = "https://www.codechef.com/ratings/all"
    xpath = '//*[@class="dataTable"]/tbody'  # /div/div/[1]/div[3]/div[1]/div[1]/div[2]/tbody/tr[0]/td[1]/a'
    
    # with open('dynamic_logs.txt', 'w'):
    #     pass

    f = open('from_all_ratings.json', 'a')
    page_from = 1
    page_to = 1517

    chrome_path = "/home/mohit/Downloads/chromedriver"
    browser = webdriver.Chrome(chrome_path)

    for page in range(page_from, page_to):  # 1517
        try:
            purl = '?itemsPerPage=40&order=asc&page='\
                    +str(page)\
                    +'&sortBy=global_rank'
            browser.get(url+purl)  # 924   1242

            WebDriverWait(browser, 60).until(
                ec.presence_of_element_located(
                    (By.CLASS_NAME, "user-name")))

            html_source = browser.page_source
            tree = html.fromstring(html_source)
            text = tree.xpath(xpath)[0]
            print(page)
            for i in range(len(text)):
                di = defaultdict()
                usr_rat = text[i][2].text_content().strip()
                usr_chng = text[i][3].text_content().strip()
                usr_li = text[i][0].text_content().strip().split('(')
                user = text[i][1].text_content().strip().split()[0]
                usr_inst = ' '.join(text[i][1].text_content().strip().split()[1:])
                di[user[2:]] = [user[:2], usr_inst, usr_li[0], usr_li[1][:-1], usr_rat, usr_chng]
                json.dump(di, f, ensure_ascii=False)
                f.write('\n')
        except:
            with open('log.txt', 'a') as l:
                l.write(page)
    browser.quit()
    f.close()
