# Streamlit Selenium Test

Streamlit project to test Selenium running in Streamlit sharing runtime.

> WORK IN PROGRESS - NOT FINISHED YET

## Problem

It is not that easy to install and use Selenium based webscraper in container based environments.
On the local computer, this usually works much more smoothly because a browser is already installed here and can be controlled remotely.
In container-based environments, however, headless operation is mandatory because no UI can be started there.

Therefore, in this repository a small example is tried to get Selenium working in a Docker container and in Streamlit Sharing.

## ToDo

- [ ] improve the selenium example
- [ ] make a streamlit app
- [ ] test streamlit app locally
- [ ] deploy to streamlit sharing runtime
- [ ] test streamlit app on streamlit sharing runtime

## Development Setup

In the streamlit sharing runtime, neither chrome, chromedriver nor geckodriver are available in the apt package sources.

The streamlit sharing runtime seems to be very similar to the official docker image `python:3.7.10-slim` on Docker Hub, which is based on Debian Buster.

### Docker Hub

Docker Images that come close to the actual streamlit sharing runtime

- <https://github.com/amineHY/docker-streamlit-app>
- <https://github.com/russelljjarvis/docker-streamlit-app>

### Docker Container local

```shell
docker pull python:3.7.10
docker pull python:3.7.10-slim
```

```shell
docker run -it --name py3710 python:3.7.10 /bin/bash
docker run -it --name py3710slim python:3.7.10-slim /bin/bash
docker run -ti --rm python:3.7.10-slim /bin/bash # testing python container

docker build -t franky1/docker-streamlit-selenium:latest .
docker run -ti -p 8080:8080 --rm franky1/docker-streamlit-selenium:latest
docker run -ti -p 8080:8080 -v $(pwd):/app --rm franky1/docker-streamlit-selenium:latest  # linux
docker run -ti -p 8080:8080 -v ${pwd}:/app --rm franky1/docker-streamlit-selenium:latest  # powershell
docker run -ti -p 8080:8080 -v %cd%:/app --rm franky1/docker-streamlit-selenium:latest  # cmd.exe
```

### Selenium Installation

```sh
pip install selenium
```

#### search for apt packages

```sh
apt update
apt-cache search chrome
apt-cache search chromium
apt-cache search firefox
apt-cache search firefox-geckodriver
apt-cache search geckodriver
apt-cache search chromedriver
cat /etc/apt/sources.list
```

#### apt packages Docker Container python:3.7.10

```log
chromium - web browser
chromium-common - web browser - common resources used by the chromium packages
chromium-driver - web browser - WebDriver support
chromium-sandbox - web browser - setuid security sandbox for chromium
chromium-shell - web browser - minimal shell
firefox-esr - Mozilla Firefox web browser - Extended Support Release (ESR)
```

#### apt package installation Docker Container python:3.7.10

```sh
apt install chromium chromium-common chromium-driver -y
```

#### apt sources

```sh
cat /etc/apt/sources.list
```

```log
# deb http://snapshot.debian.org/archive/debian/20210329T000000Z buster main
deb http://deb.debian.org/debian buster main
# deb http://snapshot.debian.org/archive/debian-security/20210329T000000Z buster/updates main
deb http://security.debian.org/debian-security buster/updates main
# deb http://snapshot.debian.org/archive/debian/20210329T000000Z buster-updates main
deb http://deb.debian.org/debian buster-updates main
```

## Selenium

<https://selenium-python.readthedocs.io/getting-started.html>

### Chrome


### Chromium

```
apt install chromium
apt install chromium-common
apt install chromium-driver
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.BinaryLocation = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",options=options)
driver.get("https://www.google.com")
```

#### Chromium Options

<https://peter.sh/experiments/chromium-command-line-switches/>

#### Chromium Headless

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/opt/chromedriver85', options=chrome_options)
#driver.set_window_size(1366, 728)
driver.implicitly_wait(5)
print("get url...")
driver.get("https://www.google.com")
```

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 11.04.2021
