FROM python:3.10.7

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app ./


LABEL maintainer="felixroland12355@gmail.com"
LABEL build_date=$(date)
CMD ["streamlit", "run", "./app/index.py"]