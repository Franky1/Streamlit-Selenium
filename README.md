# Streamlit Selenium Test

Streamlit project to test Selenium running in Streamlit sharing runtime.

- [x] **Local Windows 10** machine works
- [x] **Local Docker** container works
- [x] **Streamlit Cloud** runtime works, see example app here: [![Docker](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud-red?logo=streamlit)](https://share.streamlit.io/franky1/streamlit-selenium/main)

## ToDo

- [x] cleanup repo
- [ ] improve example

## Problem

The suggestion for this repo came from a post on the Streamlit Community Forum.

<https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>

It is not that easy to install and use Selenium based webscraper in container based environments.
On the local computer, this usually works much more smoothly because a browser is already installed here and can be controlled by the associated webdriver.
In container-based environments, however, headless operation is mandatory because no UI can be used there.

Therefore, in this repository a small example is given to get Selenium working on:

- **Local Windows 10** machine
- **Local Docker** container that mimics the streamlit sharing runtime
- **Streamlit Sharing** runtime

---

## Pitfalls

- To use Selenium (even headless in a container) you need always **two** components to be installed on your machine:
  - A **webbrowser** and its associated **webdriver**.
- The _versions_ of the webbrowser and its associated webdriver must match.
- If your are using Selenium in a docker container or on streamlit sharing, the `--headless` option is mandatory, because there ist no graphical user interface available.
- There are three options of webbrowser/webdriver combinations for Selenium:
    1. `chrome & chromedriver`
    2. `chromium & chromedriver`
    3. `firefox & geckodriver`
- Unfortunately in the default Debian Buster apt package repositories, not all of these packages are available. If we want an installation from the default repositories, only `chromium & chromedriver` is left.
- To make this repository cross-platform, the Windows 10 chromedriver is stored here in the root folder as well. Be aware, that the version of this chromedriver `ChromeDriver 89.0.4389.23` must match the version of your installed Chrome browser. The chromedriver may be outdated. `PS: This information is outdated, always download the latest chromedriver version for Windows yourself`.
- The chromedriver has a lot of options, that can be set. It may be necessary to tweak these options on different platforms to make headless operation work smoothly.
- The deployment to streamlit sharing has unfortunately failed sometimes in the past. A concrete cause of the error or an informative error message could not be identified. Currently it seems to be stable during deplyoment.

---

## Development Setup

In the streamlit sharing runtime, neither chrome, chromedriver nor geckodriver are available in the default apt package sources.

The streamlit sharing runtime seems to be very similar to the official docker image `python:3.X-slim` on Docker Hub, which is based on Debian Buster.

In this repository a `Dockerfile` is provided that mimics the streamlit sharing runtime. It can be used for local testing.

A `packages.txt` is provided with the following minimal content:

```txt
chromium
chromium-driver
```

A `requirements.txt` is provided with the following minimal content:

```txt
selenium==4.2.0
streamlit
```

---

## Docker

### Docker Hub

Docker Images that come close to the actual streamlit sharing runtime:

- <https://github.com/amineHY/docker-streamlit-app>
- <https://github.com/russelljjarvis/docker-streamlit-app>

### Docker Container local

The provided `Dockerfile` tries to mimic the Streamlit Sharing runtime.

Pulling the base image from Docker Hub

```shell
docker pull python:3.9-slim
```

Run and shell into base Python container

```shell
docker run -it --name py39slim python:3.9-slim /bin/bash
docker run -ti --rm python:3.9-slim /bin/bash
```

Build local custom Docker Image from Dockerfile

```shell
docker build --progress=plain --tag selenium:latest .
docker run -ti --name selenium --rm selenium:latest /bin/bash
```

Run custom Docker Container

```shell
docker run -ti -p 8501:8501 --rm selenium:latest /bin/bash
docker run -ti -p 8501:8501 --rm selenium:latest
docker run -ti -p 8501:8501 -v $(pwd):/app --rm selenium:latest  # linux
docker run -ti -p 8501:8501 -v ${pwd}:/app --rm selenium:latest  # powershell
docker run -ti -p 8501:8501 -v %cd%:/app --rm selenium:latest  # cmd.exe
```

### Streamlit URL

Open the local Streamlit application:

<http://localhost:8501>

for local Windows or local Docker application.

---

## Selenium

<https://selenium-python.readthedocs.io/getting-started.html>

```sh
pip install selenium
```

## Chromium

Required packages to install

```shell
apt install chromium
apt install chromium-driver
```

### Chromium Options

<https://peter.sh/experiments/chromium-command-line-switches/>

---

### Webdriver Manager for Python

- <https://github.com/SergeyPirogov/webdriver_manager>
- <https://pypi.org/project/webdriver-manager/>

> Another option to try to install the right webdriver? But this may not work on Streamlit Cloud.

```shell
pip install webdriver-manager
```

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
```

### Geckodriver

<https://pypi.org/project/geckodriver-autoinstaller/>

### selenium_driver_updater

<https://github.com/Svinokur/selenium_driver_updater>

### chromedriver-binary-auto

<https://github.com/danielkaiser/python-chromedriver-binary>

---

## Status

> Last changes: 15.06.2022
