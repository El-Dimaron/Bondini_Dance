FROM python:3.12-slim

RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*
RUN python --version

COPY hello_world_from_docker.py ./hello_world.py

CMD ["python", "hello_world.py"]
