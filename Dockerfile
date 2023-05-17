FROM python:3.10

WORKDIR /async-python-sprint-5

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .