FROM python:3.11-bookworm

# Enter your own values
ENV COINGECKO_API_KEY=CG-your-value
ENV DB_HOST=localhost
ENV DB_USER=root
ENV DB_PASS=root
ENV DB_PORT=5432
ENV DB_NAME=CryptoScraper

# Copy relevant project files 
WORKDIR /app
COPY cryptoscraper cryptoscraper/
COPY config.json .
COPY main.py .
COPY requirements.txt .

# Install the packages based from requirements.txt
RUN pip install -r requirements.txt

# Define entrypoint
ENTRYPOINT [ "python", "main.py", "market_chart"]