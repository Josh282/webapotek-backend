# Gunakan image Python ringan
FROM python:3.10-slim

# Set workdir di dalam container
WORKDIR /app

# Salin semua isi project ke dalam container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Jalankan FastAPI pakai Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
