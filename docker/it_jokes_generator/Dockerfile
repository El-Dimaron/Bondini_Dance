FROM python:3.12-slim

RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

RUN mkdir /my_folder
WORKDIR /my_folder

COPY ./jokes_generator.py .
COPY ./requirements.txt .

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

CMD ["python", "jokes_generator.py"]
