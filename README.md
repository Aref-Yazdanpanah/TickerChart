# Ticker Price Tracker

This project allows users to track and analyze the price movements of various tickers such as Bitcoin, Ethereum, or other cryptocurrencies. Users can input their purchased ticker data, specify a time range, and choose a desired time interval to view a chart of price changes and the average price of the selected tickers.

## Features

- **View Ticker List**: Users can retrieve a list of all 541 tickers currently in the system.
- **Price Chart**: A price chart displaying the price changes of selected tickers between a specified start date and end date, based on a user-defined time interval.
- **Average Price**: Calculates the average price of selected tickers during the specified time frame based on the selected interval.

### Data Source
- The list of 541 tickers and the market data is retrieved from the Binance API.
- Market data is fetched with a 15-minute time frame starting from January 1, 2023, to October 1, 2024.


## How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aref-Yazdanpanah/TickerChart.git
   cd TickerChart
   touch .env

2. **Copy the following text into the .env file**:
   ```bash
   SECRET_KEY='django-insecure-wtartsm--^c24k0mu@*7vxtfnk=qx(d(=ac=9#=d%z)b0xl$z#'
   DEBUG=True


   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```


## Running the Project with Docker

To execute the project using Docker, follow these steps:

1. **Ensure Docker is Installed**

   Make sure Docker is installed and running on your system. You can verify this by running the following command:

```bash
docker --version
```
   
2. **Ensure Docker Compose is Installed**

3. **Run the Project Using Make**:
```bash
make local-stack-up
```

4. **Verify the Project is Running**:
After running the command, the project should be up and running. You can verify by visiting http://localhost:8000 in your web browser. If you are using a different port or host configuration, adjust accordingly.

5. **Stopping the Project**:
```bash
make local-stack-down
```


## Retrieving Data from Binance

To retrieve market data from Binance, the project includes a management command that fetches data from the Binance API. However, since Binance may have regional restrictions or filtering mechanisms, the Docker container running the project must be configured to bypass these restrictions using a local proxy.

### Proxy Configuration for Binance API Access

In order to proxy the container to bypass the Binance filter and retrieve data successfully, you need to modify the Docker network configuration. This allows the container to use the local system's network, ensuring that it can communicate with Binance.

### Steps to Configure Docker for Binance API Access

1. **Modify the Docker Compose Network Mode**

   The Docker container running the project must be proxied to the local system. To achieve this, you need to configure the `network_mode` for the `web` service and `db` service in the `docker-compose.yml` file.

   Open your `docker-compose.yml` file and ensure the following configuration is applied:

```yaml
services:
  web:
    build: .
    network_mode: "host"
    # Add any other necessary configurations for the web service

  db:
    build: .
    network_mode: "host"
    # Add any other necessary configurations for the database service
```

2. **Modify the .env POSTGRES_HOST**
Then replace POSTGRES_HOST in the .env file with the following text.
When you set POSTGRES_HOST to 127.0.0.1, you're telling Django to connect to the PostgreSQL database that is expected to be running on the same host as the Django application. However, since you're using Docker with network_mode: 'host', both containers share the host's network stack, allowing them to communicate directly using localhost.

```bash
POSTGRES_HOST=127.0.0.1
```