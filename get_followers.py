from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup as bs
from lxml import etree
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
# chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")


url = 'https://www.instagram.com/joscha0/'
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
sleep(3)


###
# Get followers
# not working 100% reliable only gets 95%
###


followers_button = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
following_button = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')

followers_button.click()
sleep(2)

usernames = []

attempts = 0

while True:

    html = bs(driver.page_source, "html5lib")

    followerlist = dom = etree.HTML(str(html)).xpath(
        '/html/body/div[6]/div/div/div[2]/ul/div//li')
    new_usernames = [i.xpath('.//a/text()')[0]
                     for i in followerlist if i.xpath('.//a/text()')]

    updated_usernames = usernames + list(set(new_usernames)-set(usernames))

    if updated_usernames == usernames:
        attempts += 1
        # 5 failed attempts
        if attempts > 5:
            break
    else:
        usernames = updated_usernames
        attempts = 0

    # scroll down
    last_element = driver.find_element(By.XPATH,
                                       '/html/body/div[6]/div/div/div[2]//a[last()]')
    last_element.send_keys(Keys.END)

    # try:
    #     finished = driver.find_element(By.LINK_TEXT, 'See All Suggestions')
    #     print('end of followers reached')
    #     break
    # except:
    #     pass

    sleep(1)

print(usernames)

print(len(usernames))

sleep(100)
driver.close()
