import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")


def delete_selenium_log():
    if os.path.exists('selenium.log'):
        os.remove('selenium.log')


def show_selenium_log():
    if os.path.exists('selenium.log'):
        with open('selenium.log') as f:
            content = f.read()
            st.code(content)


def run_selenium():
    name = str()
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
        driver.get(url)
        time.sleep(3) # waits for page load
        xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
        results = driver.find_elements_by_xpath(xpath)
        name = results[0].get_property('attributes')[0]['name']
        print(name)
        # driver.close()
    return name


if __name__ == "__main__":
    delete_selenium_log()
    st.set_page_config(page_title="Selenium Test", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('🔨 Selenium Test for Streamlit Sharing')
    st.markdown("""
        This app is only a very simple test for **Selenium** running on **Streamlit Sharing** runtime. <br>
        The suggestion for this demo app came from a post on the Streamlit Community Forum.  <br>
        <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>  <br>
        Unfortunately this app does not work on Streamlit Sharing yet... 😞  <br>
        """, unsafe_allow_html=True)
    if st.button('Start Selenium run'):
        st.info(f'Selenium is running, please wait...')
        result = run_selenium()
        st.info(f'Result -> {result}')
        st.info(f'Finished')
        show_selenium_log()
