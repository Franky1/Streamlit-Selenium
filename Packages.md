# Packages

Just a scratchpad of useful commands regarding packages.

## search for apt packages

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

### apt packages found in Docker Container python:3.7.10-slim

```log
chromium - web browser
chromium-common - web browser - common resources used by the chromium packages
chromium-driver - web browser - WebDriver support
chromium-sandbox - web browser - setuid security sandbox for chromium
chromium-shell - web browser - minimal shell
firefox-esr - Mozilla Firefox web browser - Extended Support Release (ESR)
```

### apt package installation in Docker Container python:3.7.10-slim

```sh
apt install chromium chromium-common chromium-driver -y
```

### apt sources

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

### apt-cache policy

```shell
apt-cache policy chromium
```

Result:

```log
chromium:
  Installed: (none)
  Candidate: 89.0.4389.114-1~deb10u1
  Version table:
     89.0.4389.114-1~deb10u1 500
        500 http://security.debian.org/debian-security buster/updates/main amd64 Packages
     88.0.4324.182-1~deb10u1 500
        500 http://deb.debian.org/debian buster/main amd64 Packages
```

```shell
apt-cache policy chromium-common
```

Result:

```log
chromium-common:
  Installed: (none)
  Candidate: 89.0.4389.114-1~deb10u1
  Version table:
     89.0.4389.114-1~deb10u1 500
        500 http://security.debian.org/debian-security buster/updates/main amd64 Packages
     88.0.4324.182-1~deb10u1 500
        500 http://deb.debian.org/debian buster/main amd64 Packages
```

```shell
apt-cache policy chromium-driver
```

Result:

```log
chromium-driver:
  Installed: (none)
  Candidate: 89.0.4389.114-1~deb10u1
  Version table:
     89.0.4389.114-1~deb10u1 500
        500 http://security.debian.org/debian-security buster/updates/main amd64 Packages
     88.0.4324.182-1~deb10u1 500
        500 http://deb.debian.org/debian buster/main amd64 Packages
```
