def inicializa_driver(url):
    if "driver" not in st.session_state:
        chrome_options = Options()
        chrome_options.binary_location = "/opt/render/project/.render/chrome/chrome"

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(
            executable_path="/opt/render/project/.render/chromedriver/chromedriver",
            options=chrome_options
        )

        driver.get(url)
        st.session_state.driver = driver
    return st.session_state.driver
