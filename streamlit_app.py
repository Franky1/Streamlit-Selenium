import os
import json
import shutil
import subprocess
import time

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree, html


@st.cache_resource(show_spinner=False)
def get_python_version():
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_chromium_version():
    try:
        result = subprocess.run(['chromium', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_chromedriver_version():
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_logpath():
    return os.path.join(os.getcwd(), 'selenium.log')


@st.cache_resource(show_spinner=False)
def get_chromedriver_path():
    return shutil.which('chromedriver')


@st.cache_resource(show_spinner=False)
def get_webdriver_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    return options


def get_messages_from_log(logs):
    messages = list()
    for entry in logs:
        logmsg = json.loads(entry["message"])["message"]
        if logmsg["method"] == "Network.responseReceived": # Filter out HTTP responses
            # check for 200 and 204 status codes
            if logmsg["params"]["response"]["status"] not in [200, 204]:
                messages.append(logmsg)
        elif logmsg["method"] == "Network.responseReceivedExtraInfo":
            if logmsg["params"]["statusCode"] not in [200, 204]:
                messages.append(logmsg)
    if len(messages) == 0:
        messages.append('No non 200/204 status codes found!')
    return messages


def prettify_html(html_content):
    return etree.tostring(html.fromstring(html_content), pretty_print=True).decode('utf-8')


def get_webdriver_service(logpath):
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service


def delete_selenium_log(logpath):
    if os.path.exists(logpath):
        os.remove(logpath)


def show_selenium_log(logpath):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.warning('No log file found!')


def run_selenium(logpath):
    name = None
    with webdriver.Chrome(options=get_webdriver_options(),
                        service=get_webdriver_service(logpath=logpath)) as driver:
        url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
        xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
        try:
            driver.get(url)
            time.sleep(2)
            html_content = driver.page_source
            # Wait for the element to be rendered:
            element = WebDriverWait(driver, 10).until(lambda x: x.find_elements(by=By.XPATH, value=xpath))
            name = element[0].get_property('attributes')[0]['name']
        except Exception as e:
            st.error(body='Selenium Exception occured!', icon='🔥')
            st.text(f'{str(e)}\n' f'{repr(e)}')
        finally:
            performance_log = driver.get_log('performance')
            browser_log = driver.get_log('browser')
            # selenium_log = driver.get_log('selenium')
    return name, performance_log, browser_log, html_content


if __name__ == "__main__":
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    st.set_page_config(page_title="Selenium Test", page_icon='🕸️', layout="wide",
                        initial_sidebar_state='collapsed')
    left, middle, right = st.columns([3, 8, 2])
    with middle:
        st.title('Selenium on Streamlit Cloud 🕸️')
        st.markdown('''This app is only a very simple test for **Selenium** running on **Streamlit Cloud** runtime.<br>
            The suggestion for this demo app came from a post on the Streamlit Community Forum.<br>
            <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563><br><br>
            This is just a very very simple example and more a proof of concept.<br>
            A link is called and waited for the existence of a specific class to read a specific property.
            If there is no error message, the action was successful.
            Afterwards the log file of chromium is read and displayed.
            ''', unsafe_allow_html=True)
        # show the version of the used packages
        st.markdown('---')
        st.header('Versions')
        st.text(f'Checking versions that are installed in this environment:\n'
                f'- Python:       {get_python_version()}\n'
                f'- Streamlit:    {st.__version__}\n'
                f'- Selenium:     {webdriver.__version__}\n'
                f'- Chromedriver: {get_chromedriver_version()}\n'
                f'- Chromium:     {get_chromium_version()}')
        st.markdown('---')
        st.balloons()

        show_html = st.checkbox('Show also HTML content after the log files', value=False)
        if st.button('Start Selenium run'):
            st.warning('Selenium is running, please wait...', icon='⏳')
            result, performance_log, browser_log, html_content = run_selenium(logpath=logpath)
            if result is None:
                st.error('There was an error, no result found!', icon='🔥')
            else:
                st.info(f'Result -> {result}')
            st.info('Selenium log files are shown below...', icon='⬇️')
            st.subheader('Performance Log (filtered) - only non 200/204 status codes')
            st.code(body=json.dumps(get_messages_from_log(performance_log), indent=4), language='json', line_numbers=True)
            st.subheader('Selenium Log')
            show_selenium_log(logpath=logpath)
            if show_html:
                st.header('HTML Content')
                st.code(body=prettify_html(html_content), language='html', line_numbers=True)
