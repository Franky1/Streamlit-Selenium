# this base image seems to be quite similar to the streamlit cloud environment
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# we need some build tools for installing additional python pip packages
RUN apt-get update \
    && apt-get install --yes \
    software-properties-common \
    build-essential \
    gcc \
    g++ \
    cmake \
    git \
    curl \
    python3-dev

WORKDIR /app

# if we have a packages.txt, install it
COPY packages.txt packages.txt
RUN xargs -a packages.txt apt-get install --yes

RUN pip install --no-cache-dir --upgrade pip setuptools wheel uv
COPY requirements.txt requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

EXPOSE 8501

HEALTHCHECK --interval=1m --timeout=20s \
    CMD curl --fail http://localhost:8501/_stcore/health

COPY . .

CMD ["streamlit", "run", "streamlit_app.py"]

# docker build --progress=plain --tag streamlit-selenium:latest .
# docker run -ti -p 8501:8501 --rm streamlit-selenium:latest /bin/bash
# docker run -ti -p 8501:8501 --rm streamlit-selenium:latest
# docker run -ti -p 8501:8501 -v ${pwd}:/app --rm streamlit-selenium:latest
# docker run -ti -p 8501:8501 -v ${pwd}:/app --rm streamlit-selenium:latest /bin/bash
