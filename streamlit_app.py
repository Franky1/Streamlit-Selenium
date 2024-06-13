import json
import os
import shutil
import subprocess
import time
from typing import List, Tuple

import countryflag
import pandas as pd
import requests
import streamlit as st
from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@st.cache_data(show_spinner=False, ttl=180)
def get_proxyscrape_socks4(country: str = 'all', protocol: str = 'socks4') -> tuple:
    PROXYSCRAPE_URL = 'https://api.proxyscrape.com/v3/free-proxy-list/get'
    params = {
        'request': 'displayproxies',
        'proxy_format' : 'protocolipport',
        'format': 'json',
        'protocol': protocol,
        'timeout': 2000,
        'anonymity': 'all',
        'country': country,
    }
    try:
        response = requests.get(url=PROXYSCRAPE_URL, params=params, timeout=3)
        response.raise_for_status()
        response = response.json()
        response = pd.json_normalize(response.get('proxies')).astype(str)
    except Exception as e:
        return False, str(e)
    else:
        return True, response


@st.cache_data(show_spinner=False, ttl=180)
def get_mtproto_socks5() -> tuple:
    url = "https://mtpro.xyz/api/"
    params = {
        'type': 'socks'
    }
    try:
        response = requests.get(url, params=params)
        response = response.json()
        response = pd.DataFrame(response).astype(str)
    except Exception as e:
        return False, str(e)
    else:
        return True, response


@st.cache_resource(show_spinner=False)
def get_flag(country: str):
    return countryflag.getflag([country])


@st.cache_resource(show_spinner=False)
def get_python_version() -> str:
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_chromium_version() -> str:
    try:
        result = subprocess.run(['chromium', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_chromedriver_version() -> str:
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        version = result.stdout.split()[1]
        return version
    except Exception as e:
        return str(e)


@st.cache_resource(show_spinner=False)
def get_logpath() -> str:
    return os.path.join(os.getcwd(), 'selenium.log')


@st.cache_resource(show_spinner=False)
def get_chromedriver_path() -> str:
    return shutil.which('chromedriver')


@st.cache_resource(show_spinner=False)
def get_webdriver_options(proxy: str = None, socksStr: str = None) -> Options:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument('--ignore-certificate-errors')
    if proxy is not None and socksStr is not None:
        options.add_argument(f"--proxy-server={socksStr}://{proxy}")
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    return options


def get_messages_from_log(logs) -> List:
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
        return None
    return messages


def prettify_html(html_content) -> str:
    return etree.tostring(html.fromstring(html_content), pretty_print=True).decode('utf-8')


def get_webdriver_service(logpath) -> Service:
    service = Service(
        executable_path=get_chromedriver_path(),
        log_output=logpath,
    )
    return service


def delete_selenium_log(logpath: str):
    if os.path.exists(logpath):
        os.remove(logpath)


def show_selenium_log(logpath: str):
    if os.path.exists(logpath):
        with open(logpath) as f:
            content = f.read()
            st.code(body=content, language='log', line_numbers=True)
    else:
        st.error('No log file found!', icon='🔥')


def run_selenium(logpath: str, proxy: str, socksStr: str) -> Tuple[str, List, List, str]:
    name = None
    html_content = None
    options = get_webdriver_options(proxy=proxy, socksStr=socksStr)
    service = get_webdriver_service(logpath=logpath)
    with webdriver.Chrome(options=options, service=service) as driver:
        url = "https://www.unibet.fr/sport/hub/euro-2024"
        try:
            driver.get(url)
            time.sleep(2)
            # Wait for the element to be rendered:
            element = WebDriverWait(driver=driver, timeout=10).until(lambda x: x.find_elements(by=By.CSS_SELECTOR, value="h2.eventcard-content-name"))
            name = element[0].get_property('attributes')[0]['name']
            html_content = driver.page_source
        except Exception as e:
            st.error(body='Selenium Exception occured!', icon='🔥')
            st.error(body=str(e), icon='🔥')
        finally:
            performance_log = driver.get_log('performance')
            browser_log = driver.get_log('browser')
    return name, performance_log, browser_log, html_content


if __name__ == "__main__":
    if "proxy" not in st.session_state:
        st.session_state.proxy = None
    if "proxies" not in st.session_state:
        st.session_state.proxies = None
    if "socks5" not in st.session_state:
        st.session_state.socks5 = False
    if "df" not in st.session_state:
        st.session_state.df = None
    if "countries" not in st.session_state:
        st.session_state.countries = None
    logpath=get_logpath()
    delete_selenium_log(logpath=logpath)
    st.set_page_config(page_title="Selenium Test", page_icon='🕸️', layout="wide",
                        initial_sidebar_state='collapsed')
    left, middle, right = st.columns([2, 11, 1], gap="small")
    with middle:
        st.title('Selenium on Streamlit Cloud 🕸️')
        st.markdown('''This app is only a very simple test for **Selenium** running on **Streamlit Cloud** runtime.
            The suggestion for this demo app came from a post on the Streamlit Community Forum.<br>
            <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563><br><br>
            This is just a very very simple example and more a proof of concept.
            A link is called and waited for the existence of a specific class to read a specific property.
            If there is no error message, the action was successful. Afterwards the log files are displayed.
            Since the target website has geoip blocking enabled, a proxy is required to bypass this and can be selected optionally.
            However, the use of proxies is not guaranteed to work, as they may not working properly.
            If you disable the proxy, the app will usually fail on streamlit cloud to load the page.
            ''', unsafe_allow_html=True)
        st.markdown('---')
        middle_left, middle_right = st.columns([9, 10], gap="medium")
        with middle_left:
            st.header('Proxy')
            st.session_state.useproxy = st.toggle(label='Enable proxy to bypass geoip blocking', value=True, disabled=False)
            if st.session_state.useproxy:
                socks5 = st.toggle(label='Use Socks5 proxy', value=True, disabled=False)
                if socks5 != st.session_state.socks5:
                    st.session_state.socks5 = socks5
                    st.session_state.proxy = None
                    st.session_state.proxies = None
                    st.session_state.df = None
                if st.session_state.socks5:
                    # try to gather and use socks5 proxies
                    if st.button(label='Refresh proxies from free Socks5 list'):
                        success, proxies = get_mtproto_socks5()
                        if not success:
                            st.error(f"No socks5 proxies found", icon='🔥')
                            st.error(proxies, icon='🔥')
                            st.session_state.df = None
                        else:
                            if not proxies.empty:
                                countries = sorted(proxies['country'].unique().tolist())
                                st.session_state.df = proxies.copy()
                                st.session_state.countries = countries
                            else:
                                st.session_state.df = None
                                st.session_state.countries = None
                else:
                    # try to gather and use socks4 proxies
                    if st.button(label='Refresh proxies from free Socks4 list'):
                        success, proxies = get_proxyscrape_socks4(country='all', protocol='socks4')
                        if not success:
                            st.error(f"No socks4 proxies found", icon='🔥')
                            st.error(proxies, icon='🔥')
                            st.session_state.df = None
                        else:
                            if not proxies.empty:
                                countries = sorted(proxies['ip_data.countryCode'].unique().tolist())
                                st.session_state.df = proxies.copy()
                                st.session_state.countries = countries
                            else:
                                st.session_state.df = None
                                st.session_state.countries = None
                if st.session_state.countries is not None:
                    # limit countries to a set of countries
                    allowed_countries = ['FR', 'GB', 'DE', 'ES', 'CH', 'US']
                    st.session_state.countries = [country for country in st.session_state.countries if country in allowed_countries]
                if st.session_state.df is not None and st.session_state.countries is not None:
                    selected_country = st.selectbox(label='Select a country', options=st.session_state.countries)
                    selected_country_flag = get_flag(selected_country)
                    st.info(f'Selected Country: {selected_country} {selected_country_flag}', icon='🌍')
                    if st.session_state.socks5:
                        selected_country_proxies = st.session_state.df[st.session_state.df['country'] == selected_country]
                    else:
                        selected_country_proxies = st.session_state.df[st.session_state.df['ip_data.countryCode'] == selected_country]
                    st.session_state.proxies = set(selected_country_proxies[['ip', 'port']].apply(lambda x: f"{x.iloc[0]}:{x.iloc[1]}", axis=1).tolist())
                    if st.session_state.proxies:
                        st.session_state.proxy = st.selectbox(label='Select a proxy from the list', options=st.session_state.proxies, index=0)
                        st.info(body=f'{st.session_state.proxy} {get_flag(selected_country)}', icon='😎')
            else:
                st.session_state.proxy = None
                st.session_state.proxies = None
                st.session_state.df = None
                st.info('Proxy is disabled', icon='🔒')
        with middle_right:
            st.header('Versions')
            st.text('This is only for debugging purposes.\n'
                    'Checking versions installed in environment:\n\n'
                    f'- Python:        {get_python_version()}\n'
                    f'- Streamlit:     {st.__version__}\n'
                    f'- Selenium:      {webdriver.__version__}\n'
                    f'- Chromedriver:  {get_chromedriver_version()}\n'
                    f'- Chromium:      {get_chromium_version()}')
        st.markdown('---')

        if st.button('Start Selenium run'):
            st.info(f'Selected Proxy: {st.session_state.proxy}', icon='☢️')
            if st.session_state.useproxy:
                socksStr = 'socks5' if st.session_state.socks5 else 'socks4'
                st.info(f'Selected Socks: {socksStr}', icon='🧦')
            else:
                socksStr = None
            with st.spinner('Selenium is running, please wait...'):
                result, performance_log, browser_log, html_content = run_selenium(logpath=logpath, proxy=st.session_state.proxy, socksStr=socksStr)
                if result is None:
                    st.error('There was an error, no result found!', icon='🔥')
                else:
                    st.success(body=f'Result: {result}', icon='🎉')
                st.info('Selenium log files are shown below...', icon='⬇️')
                performance_log_msg = get_messages_from_log(performance_log)
                if performance_log_msg is not None:
                    st.header('Performance Log (filtered) - only non 200/204 status codes')
                    st.code(body=json.dumps(performance_log_msg, indent=4), language='json', line_numbers=True)
                st.header('Selenium Log')
                show_selenium_log(logpath=logpath)
                if result is None and html_content is not None:
                    st.header('HTML Content')
                    st.code(body=prettify_html(html_content), language='html', line_numbers=True)
                st.balloons()
