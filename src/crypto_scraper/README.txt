docker build -t cryptoscraper .
docker run -e COINGECKO_API_KEY="CG-u6w9sguZFc3mRAwDmoFuQWh9" \
    -e DB_HOST="192.168.1.11" \
    -e DB_USER="root" \
    -e DB_PASS="root" \
    -e DB_PORT="5432" \
    -e DB_NAME="CryptoScraper" \
    cryptoscraper