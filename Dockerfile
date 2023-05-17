FROM python:3.10.3

WORKDIR /async-python-sprint-5

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .