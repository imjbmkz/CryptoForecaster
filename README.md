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

#### Project Architecture
The architecture of this project needs to be setup first before running the Docker images.

Go to the project directory.
```
cd C:\Users\josh\Desktop\CryptoForecaster
```
Run Docker Compose command below to run the services required. Make sure that you add the needed environment variables
```
docker compose up -d # runs in the background
```
The API is also being called from the Docker Compose file, but may not be running yet. Do the following steps, then restart Docker Compose services.

**Setting-up database**
- Go to http://localhost:8081 and login to pgAdmin
- Register the PostgreSQL database server `pgdatabase`
- Run the query `sql/init-db.sql` in the `CryptoScraper` database

**Setting-up Minio**
- Go to http://localhost:9001 and login to Minio
- Create an Access Key 
- Make sure to copy the Secret Key
- Create a bucket

**Rerunning Docker Compose and testing the API**
- After doing these steps, stop the services `docker compose stop`
- Start the services again `docker compose up -d`
- Check if `cryptoforecaster-cryptoapi` image is running `docker ps`
- If the image is listed, you should get a successful response from http://localhost:4545 from your browser or via `curl`

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