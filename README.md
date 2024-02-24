<!-- markdownlint-disable MD026 -->
# Streamlit Selenium Test

Streamlit project to test Selenium running in Streamlit Cloud runtime.

- [x] **Local Windows 10** machine works
- [x] **Local Docker** container works
- [x] **Streamlit Cloud** runtime works, see example app here: [![Docker](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud-red?logo=streamlit)](https://selenium-example.streamlit.app/)

## Issues :bug:

- `2024-02-24` Example fails on Streamlit Cloud with a TimeoutException, but works locally. Probably geoip or ip blocking on the target website. :thinking:

## ToDo :ballot_box_with_check:

- [ ] improve example
- [ ] try also `undetected_chromedriver` package
- [ ] try also `seleniumbase` package

## Problem :thinking:

The suggestion for this repo came from a post on the Streamlit Community Forum.

<https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>

It is not that easy to install and use Selenium based webscraper in container based environments.
On the local computer, this usually works much more smoothly because a browser is already installed here and can be controlled by the associated webdriver.
In container-based environments, however, headless operation is mandatory because no UI can be used there.

Therefore, in this repository a small example is given to get Selenium working on:

- **Local Windows 10** machine
- **Local Docker** container that mimics the Streamlit Cloud runtime
- **Streamlit Community Cloud** runtime

## Pitfalls :triangular_flag_on_post:

- To use Selenium (even headless in a container) you need always **two** components to be installed on your machine:
  - A **webbrowser** and its associated **webdriver**.
- The **version** of the headless webbrowser and its associated webdriver must always **match**.
- If your are using Selenium in a docker container or on Streamlit Cloud, the `--headless` option is mandatory, because there is no graphical user interface available.
- There are three options of webbrowser/webdriver combinations for Selenium:
    1. `chrome & chromedriver`
    2. `chromium & chromedriver`
    3. `firefox & geckodriver`
- Unfortunately in the default Debian Bullseye apt package repositories, not all of these packages are available. If we want an installation from the default repositories, only `chromium & chromedriver` is left.
- To make this repository cross-platform, the Windows 10 chromedriver must be stored here in the root folder or add to the PATH. Be aware, that the version of this chromedriver must match the version of your installed Chrome browser.
- The chromedriver has a lot of options, that can be set. It may be necessary to tweak these options on different platforms to make headless operation work smoothly.
- The deployment to Streamlit Cloud has unfortunately failed sometimes in the past. A concrete cause of the error or an informative error message could not be identified. Currently it seems to be stable during deployment.

## Development Setup :hammer_and_wrench:

In the Streamlit Cloud runtime, neither chrome, chromedriver nor geckodriver are available in the default apt package sources.

The Streamlit Cloud runtime seems to be very similar to the official docker image `python:3.XX-slim` on Docker Hub, which is based on Debian Bookworm.

In this repository a [Dockerfile](Dockerfile) is provided that mimics the Streamlit Cloud runtime. It can be used for local testing.

A `packages.txt` is provided with the following minimal content:

```txt
chromium
chromium-driver
```

A `requirements.txt` is provided with the following minimal content:

```txt
streamlit
selenium
```

## Docker :whale2:

### Docker Hub

Docker Images that come close to the actual Streamlit Cloud runtime:

- <https://github.com/amineHY/docker-streamlit-app>
- <https://github.com/russelljjarvis/docker-streamlit-app>

### Docker Container local

The provided [Dockerfile](Dockerfile) tries to mimic the Streamlit Cloud runtime.

Build local custom Docker Image from Dockerfile

```shell
docker build --progress=plain --tag selenium:latest .
```

Run custom Docker Container

```shell
docker run -ti -p 8501:8501 --rm selenium:latest
docker run -ti -p 8501:8501 --rm selenium:latest /bin/bash
docker run -ti -p 8501:8501 -v $(pwd):/app --rm selenium:latest  # linux
docker run -ti -p 8501:8501 -v ${pwd}:/app --rm selenium:latest  # powershell
docker run -ti -p 8501:8501 -v %cd%:/app --rm selenium:latest    # cmd.exe
```

## Selenium :eye:

<https://selenium-python.readthedocs.io/getting-started.html>

```sh
pip install selenium
```

### Chromium :spider_web:

Required packages to install

```shell
apt install chromium
apt install chromium-driver
```

### Chromium Options

<https://peter.sh/experiments/chromium-command-line-switches/>

## undetected_chromedriver :man_shrugging:

> Another option to try, not yet done...

- <https://github.com/ultrafunkamsterdam/undetected-chromedriver>
- *Resources*
  - <https://datawookie.dev/blog/2022/10/undetected-chromedriver/>
  - <https://stackoverflow.com/questions/74469556/undetected-chromedriver-with-proxy>
  - <https://stackoverflow.com/questions/72919814/undetected-chromedriver-is-not-bypassing-in-headless-mode>
  - <https://stackoverflow.com/questions/73838436/why-cant-i-connect-to-chrome-when-using-the-undetected-chromedriver>
  - <https://stackoverflow.com/questions/74793705/how-to-load-chrome-options-using-undetected-chrome>
  - <https://www.youtube.com/watch?v=6SDzRN1aHiI>

## Status :heavy_check_mark:

> Last changed: 2023-10-24
