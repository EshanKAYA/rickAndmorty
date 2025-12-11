
# Python'un hafif sürümünü kullan
FROM python:3.9-slim

# Çalışma klasörünü ayarla
WORKDIR /app

# Gereksinimleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm kodları kopyala
COPY . .

# 5000 portunu aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]
