FROM python:3.11-bookworm

# MinIO connection: enter your own values
ENV MINIO_ACCESS_KEY_ID=your_access_key
ENV MINIO_SECRET_ACCESS_KEY=your_secret_access_key
ENV MINIO_ENDPOINT=host:port
ENV MINIO_BUCKET_NAME=your_bucket

# SQL database connection: enter your own values
ENV DB_HOST=localhost
ENV DB_USER=root
ENV DB_PASS=root
ENV DB_PORT=5432
ENV DB_NAME=CryptoScraper

# Copy relevant project files 
WORKDIR /app
COPY cryptomodel cryptomodel/
# COPY config.json .
COPY main.py .
COPY requirements.txt .

# Install the packages based from requirements.txt
RUN pip install -r requirements.txt

# Define entrypoint
ENTRYPOINT [ "python", "main.py"]