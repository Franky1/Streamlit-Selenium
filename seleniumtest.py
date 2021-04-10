import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_argument('--headless')

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

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.python.org")
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
# print(driver.page_source)
driver.close()
