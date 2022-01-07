from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageFilter
import requests
from bs4 import BeautifulSoup as bs
import time
import cv2


chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")
# chrome_options.add_argument("--headless")

url = 'https://www.instagram.com/joscha0/'
driver = webdriver.Chrome(options=chrome_options)


def save_img(input_url: str,  output_path: str, denoise: bool = True):
    """Save image in 64x64 resolution

    Args:
        input_url (str): The image url
        output_path (str): The path of the output file
    """
    img = Image.open(requests.get(input_url, stream=True).raw)

    img.thumbnail((64, 64), resample=Image.LANCZOS)
    img.save(output_path, optimize=True)

    if (denoise):
        img = cv2.imread(output_path)
        dst = cv2.fastNlMeansDenoisingColored(img, None, 8, 0, 7, 21)
        cv2.imwrite(output_path, dst)


def get_post_urls() -> list:
    """Returns a list of post image urls from a profile

    Returns:
        list: List of post image urls
    """
    image_urls = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(1)
        # get all post image urls
        html = bs(driver.page_source, "html5lib")
        new_urls = [i.get('src')
                    for i in html.findAll("img", {"class": "FFVAD"})]

        # add unique image urls
        image_urls = image_urls + list(set(new_urls)-set(image_urls))

        # scroll down
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        new_height = driver.execute_script("return document.body.scrollHeight")
        # check if reached scroll limit
        if new_height == last_height:
            break

        last_height = new_height

    return image_urls


def save_posts():
    image_urls = get_post_urls()

    for idx, image_url in enumerate(image_urls):
        save_img(image_url, f'data/img{idx}.jpg')


def get_profile_img_url() -> str:
    return driver.find_element_by_xpath(
        '/html/body/div[1]/section/main/div/header/div/div/span/img').get_attribute('src')


driver.get(url)

save_posts()

save_img(get_profile_img_url(), 'data/profile.jpg')

driver.close()
