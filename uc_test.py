'''
undetected_chromedriver test script and playground to get it working in docker container
'''
import logging
import shutil
import time
from pathlib import Path

import undetected_chromedriver as uc


browser_executable_path = shutil.which("chromium")
print(browser_executable_path)

# delete old log file
Path('selenium.log').unlink(missing_ok=True)
time.sleep(1)

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

with uc.Chrome(browser_executable_path=browser_executable_path,
                # debug=False,
                # headless=True,
                options=options,
                use_subprocess=False,
                log_level=logging.DEBUG,
                service_log_path='selenium.log') as driver:
    driver.get('https://nowsecure.nl' )  # test site with max anti-bot protection
    driver.implicitly_wait(1)
    driver.save_screenshot('selenium-nowsecure.png')
    driver.get("https://datadome.co/")
    driver.implicitly_wait(1)
    driver.save_screenshot('selenium-datadome.png')

time.sleep(1)
