import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--disable-features=VizDisplayCompositor")


def run_selenium():
    name = str()
    with webdriver.Chrome(options=chrome_options) as driver:
        url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
        driver.get(url)
        xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
        results = driver.find_elements_by_xpath(xpath)
        name = results[0].get_property('attributes')[0]['name']
        print(name)
        # driver.close()
    return name


if __name__ == "__main__":
    st.set_page_config(page_title="Selenium Test", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('🔨 Selenium Test for Streamlit Sharing')
    st.markdown("""
        This app is only a very simple test for **Selenium** running on **Streamlit Sharing** runtime. <br>
        The suggestion for this demo app came from a post on the Streamlit Community Forum.
        <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>
        """, unsafe_allow_html=True)
    if st.button('Start Selenium run'):
        st.info(f'Selenium is running, please wait...')
        result = run_selenium()
        st.info(f'Result -> {result}')
        st.info(f'Finished')
