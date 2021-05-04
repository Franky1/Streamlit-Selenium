# only for python code snippets
# do not run this script

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

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
