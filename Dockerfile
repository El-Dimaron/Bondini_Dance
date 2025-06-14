FROM python:3.12-slim

RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

RUN mkdir /bd_server
WORKDIR /bd_server

COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "src/manage.py", "runserver"]
