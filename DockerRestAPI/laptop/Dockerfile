FROM python:3.11-slim

WORKDIR /brevets

COPY . /brevets

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "flask_brevets.py"]