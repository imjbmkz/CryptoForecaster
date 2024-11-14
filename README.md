# Simple CryptoScraper
This project is built for demo and portfolio purposes. 

![Crypto Scraper ERD](/assets/architecture.svg)

**CryptoScraper** is designed to perform end-to-end Crypto analytics, including the following components:
- Data Architecture: Uses **Docker Compose** to locally host the required architecture for this project, which includes **PostgreSQL database**, **pgAdmin**, and **MinIO**
- ETL (Extract, Transform, Load): Scripts that extract data from [CoinGecko API](https://www.coingecko.com/en/api), transform it into the required format, and load it into the local PostgreSQL database.
- Machine Learning: Scripts that perform feature selection, train machine learning models for forecasting Crypto price, and evaluate their performance to get the best fitting model which will be uploaded to the local Minio cluster.
- API Hosting: A RESTful API that serves predictions based on the trained machine learning model.
- Dashboard: A Power BI dashboard that shows the trading price in the last 24 hours and the predicted prices predicted in the next 24 hour

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install) (WSL, for Windows users)
- [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

### Project Structure
```
project-root/
|
├── assets/
│   └── architecture.py     # Diagram of the project architecture
│
├── dags/
│   ├── .env                # Environment variables to be used. See .env-sample
│   └── run_dag.py          # Airflow DAG for ETL, model training, and API refresh
│
├── dashboard/              # Power BI project for visualizing forecasts
│
├── sql/                    # SQL script to be executed upon building the project
│
├── src/
│   ├── crypto_api/         # Scripts for hosting the API
│   ├── crypto_model/       # Scripts for training models
│   └── crypto_scraper/     # Scripts for ETL 
│
├── .gitignore
├── docker-compose.yaml     # Docker Compose file for running the project architecture
├── LICENSE
├── README.md               # Project documentation
└── requirements.txt        # Dependencies for Airflow orchestration
```

### Installation
#### WSL
The project has dependencies on Unix-based systems. For Windows users, WSL is required. 
```
wsl --install
```
Follow the [installation instructions](https://learn.microsoft.com/en-us/windows/wsl/install) from Microsoft. Afterwards, open either Command Prompt or PowerShell. Run the command below to access WSL.
```
wsl
```
Update all packages in WSL environment.
```
sudo apt update # get updates
sudo apt upgrade # install updates
```

#### Python
Install Python in WSL.
```
sudo apt install python3.11
```
`venv` is used to manage the virtual environment in this project. Run the following command to install `venv`.
```
sudo apt install python3.11-venv
```

#### Airflow
To install Airflow, setup a virtual environment first.
```
python3.11 -m venv env
```
Activate the virtual environment.
```
source env/bin/activate
```
Install the required packages from the `requirements.txt` file.
```
pip3 install -r requirements.txt
```


### Setting-up
#### CoinGecko API Key
Sign-up on [CoinGecko](https://www.coingecko.com/en/api) to get your API Key.

#### Minio
The forecasting API is a service included in the Docker Compose file. This API has dependencies to Minio. Minio needs to be setup first before running the Docker Compose altogether. 

Go to the project directory.
```
cd C:\Users\josh\Desktop\CryptoForecaster
```
Run Docker Compose command below to run Minio service first. The cluster needs to be setup first to acquire the access keys and secrets.
```
docker compose up minio
```
Go to http://localhost:9001 and login to Minio.

![Minio UI](/assets/minio.png)

Create an Access Key.

![Minio Access Key](/assets/minio_accesskey.png)

Make sure to copy the Secret Key.

![Minio Secret Key](/assets/minio_secretkey.png)

Create a bucket.

![Minio Bucket](/assets/minio_bucket.png)

Make sure to copy all values needed and store to the environment variables below.
- MINIO_ACCESS_KEY_ID
- MINIO_SECRET_ACCESS_KEY
- MINIO_ENDPOINT
- MINIO_BUCKET_NAME

Stop the Minio service afterwards.

#### Building Docker Compose and testing the services
To test the services, run the Docker Compose file.
```
docker compose up
# or 
docker compose up -d # runs in the background
```
Access the following portals and see if you can access the UI.

**pgAdmin and PostgreSQL**
- Login to http://localhost:8081 
- Register the `pgdatabase` server
- Check if the tables `public.market_chart` and `public.coins_list` are already created in the CryptoScraper database

**Minio**
- Login to http://localhost:9001
- See if you already have the Access Key and Bucket created

**Forecasting API**
- Access the http://localhost:4545 (or use `curl`) and see if there i a successful 

#### Building Docker Images
You need to build the Docker files for the components of this project: `crypto_scraper` and `crypto_model`. The Docker Compose file already manages the build of `crypto_api`, so there is no need to build it manually. 

Do the following steps to build the images.

Go to the project directory
```
cd C:\Users\josh\Desktop\CryptoForecaster\src\crypto_scraper
# or cd C:\Users\josh\Desktop\CryptoForecaster\src\crypto_model
```
Run the following command to build the images.
```
docker build -t cryptoscraper .
# or docker build -t cryptomodel .
```

### Running the project
Run the services required via Docker compose
```
cd your_project_directory
docker compose up -d 
```
Run Airflow using the following commands.
```
export AIRFLOW_HOME=$(pwd)
source env/bin/activate
airflow standalone
```