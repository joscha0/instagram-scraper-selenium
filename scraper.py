from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")

url = 'https://www.instagram.com/joscha0/?__a=1'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

content = driver.find_element_by_tag_name('pre').text
parsed_json = json.loads(content)
print(parsed_json)
