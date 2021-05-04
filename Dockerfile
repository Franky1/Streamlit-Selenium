FROM python:3.7.10-slim

WORKDIR /app
COPY . .

# CAVEAT: packages.txt must exist and have Linux LF only!!!
RUN apt-get update
RUN xargs -a packages.txt apt-get install --yes
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["streamlit", "run", "streamlit_app.py"]
