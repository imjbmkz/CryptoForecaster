FROM python:3.11-bookworm

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