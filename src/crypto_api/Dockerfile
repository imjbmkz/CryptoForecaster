FROM python:3.11-bookworm

# Copy relevant project files 
WORKDIR /app
COPY cryptoapi cryptoapi/
COPY regression_model.pkl .
COPY main.py .
COPY requirements.txt .

# Install the packages based from requirements.txt
RUN pip install -r requirements.txt

# Define entrypoint
ENTRYPOINT [ "fastapi", "run", "main.py", "--port", "4545"]