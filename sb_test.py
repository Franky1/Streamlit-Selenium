'''
SeleniumBase test script and playground to get it working in docker container
'''

from seleniumbase import Driver, page_actions

driver = Driver(headless=True, uc=True)
driver.get("https://nowsecure.nl")
page_actions.wait_for_text(driver, "OH YEAH, you passed!", "h1")
print(driver.find_element("css selector", "body").text)
screenshot_name = "sb-selenium-nowsecure.png"
driver.save_screenshot(screenshot_name)
print(f"Screenshot saved to: {screenshot_name}")
driver.quit()
