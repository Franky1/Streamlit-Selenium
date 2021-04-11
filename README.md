# Streamlit Selenium Test

Streamlit project to test Selenium running in Streamlit sharing runtime.

> WORK IN PROGRESSs  
> Local Windows and Docker deployment works  
> Deployment to Streamlit Sharing does NOT work

## ToDo

- [ ] Test streamlit app on streamlit sharing runtime [FAILED]

## Problem

The suggestion for this repo came from a post on the Streamlit Community Forum.

<https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>

It is not that easy to install and use Selenium based webscraper in container based environments.
On the local computer, this usually works much more smoothly because a browser is already installed here and can be controlled by the associated webdriver.
In container-based environments, however, headless operation is mandatory because no UI can be used there.

Therefore, in this repository a small example is given to get Selenium working on:

- Local Windows 10 machine
- Local docker container that mimics the streamlit sharing runtime
- Streamlit Sharing runtime

---

## Pitfalls

- To use Selenium (even headless in a container) you need always *two* components to be installed on your machine: A webbrowser and its associated webdriver.
- The versions of the webbrowser and its associated webdriver must match.
- If your are using Selenium in a docker container or on streamlit sharing, the `--headless` option is mandatory, because there ist no UI available.
- There are three options of webbrowser/webdriver combinations for Selenium:
  1. chrome/chromedriver
  2. chromium/chromedriver
  3. firefox/geckodriver
- Unfortunately in the default Debian Buster apt package repositories, not all of these packages are available. If we want an installation from the default repositories, only `chromium/chromedriver` is left.
- To make this repository cross-platform, the Windows 10 chromedriver is stored here in the root folder as well. Be aware, that the version of this chromedriver must match the version of your installed Chrome browser. The chromedriver may be outdated.
- The chromedriver has a lot of options, that can be set. It may be necessary to tweak these options on different platforms to make headless operation work smoothly.

---

## Development Setup

In the streamlit sharing runtime, neither chrome, chromedriver nor geckodriver are available in the default apt package sources.

The streamlit sharing runtime seems to be very similar to the official docker image `python:3.7.10-slim` on Docker Hub, which is based on Debian Buster.

In this repository a `Dockerfile` is provided that mimics the streamlit sharing runtime. It can be used for local testing.

A `packages.txt` is provided with the following minimal content:

```txt
chromium
chromium-common
chromium-driver
```

A `requirements.txt` is provided with the following minimal content:

```txt
selenium
streamlit
```

---

## Docker

### Docker Hub

Docker Images that come close to the actual streamlit sharing runtime:

- <https://github.com/amineHY/docker-streamlit-app>
- <https://github.com/russelljjarvis/docker-streamlit-app>

### Docker Container local

Pulling the image from Docker Hub

```shell
docker pull python:3.7.10-slim
```

Run and shell into default python container

```shell
docker run -it --name py3710slim python:3.7.10-slim /bin/bash
docker run -ti --rm python:3.7.10-slim /bin/bash
```

Build local custom Docker Image from Dockerfile

```shell
docker build -t franky1/docker-streamlit-selenium:latest .
docker run -ti --name selenium --rm franky1/docker-streamlit-selenium:latest /bin/bash
```

Run custom Docker Container

```shell
docker run -ti -p 8080:8080 --rm franky1/docker-streamlit-selenium:latest
docker run -ti -p 8080:8080 -v $(pwd):/app --rm franky1/docker-streamlit-selenium:latest  # linux
docker run -ti -p 8080:8080 -v ${pwd}:/app --rm franky1/docker-streamlit-selenium:latest  # powershell
docker run -ti -p 8080:8080 -v %cd%:/app --rm franky1/docker-streamlit-selenium:latest  # cmd.exe
```

---

## Selenium

<https://selenium-python.readthedocs.io/getting-started.html>

```sh
pip install selenium
```

## Chromium

Required packages to install

```
apt install chromium
apt install chromium-common
apt install chromium-driver
```

### Chromium Options

<https://peter.sh/experiments/chromium-command-line-switches/>

---

## Status

- WORK IN PROGRESS - not finished yet
- Last changes: 11.04.2021
