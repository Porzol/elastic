# Use slim Python image
FROM python:3.13.3-slim

RUN apt-get update

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8001"]
