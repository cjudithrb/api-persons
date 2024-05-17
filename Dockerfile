FROM python:3-slim
WORKDIR /programas/api-persons
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["fastapi", "run", "./main.py", "--port", "9010"]