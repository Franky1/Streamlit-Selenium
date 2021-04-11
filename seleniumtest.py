import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")

if sys.platform.startswith("linux"):
    print("Linux OS detected")
    # executable_path = "./binaries/chromedriver"
    # chrome_options.BinaryLocation = "/usr/bin/chromium"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
elif sys.platform.startswith("win"):
    print("Windows OS detected")
    # executable_path = "./binaries/chromedriver.exe"
else:
    raise ValueError("Unknown OS")

with webdriver.Chrome(options=chrome_options) as driver:
    url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
    driver.get(url)
    balise = '//*[@class="ui-mainview-block eventpath-wrapper"]'
    results = driver.find_elements_by_xpath(balise)
    print(results[0].get_property('attributes')[0]['name'])
    # driver.close()
