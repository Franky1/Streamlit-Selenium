FROM python:3.7.10-slim

WORKDIR /app
COPY . ./

RUN apt-get update
RUN apt-get install --yes chromium chromium-common chromium-driver
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["streamlit", "run", "--server.port", "8080", "streamlit_app.py"]
