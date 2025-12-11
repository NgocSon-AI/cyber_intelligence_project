FROM python:3.10-slim
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "src.main"]