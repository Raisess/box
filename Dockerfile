FROM python:3.11.4-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY src/ src/

EXPOSE 8000

CMD ["python", "/usr/src/app/src/server.py", "8000", "0.0.0.0"]
