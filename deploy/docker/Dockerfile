FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY deploy/api/package/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deploy/api/package/main.py .
COPY deploy/api/package/templates/ templates/
COPY deploy/api/package/static/     static/
COPY deploy/api/package/tools/      tools/
COPY deploy/api/package/scripts/    scripts/
COPY deploy/api/package/data/users.json.example data/users.json.example

RUN mkdir -p data reports .ssh

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
