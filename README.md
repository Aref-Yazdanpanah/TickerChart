# Ticker Price Tracker

This project allows users to track and analyze the price movements of various tickers such as Bitcoin, Ethereum, or other cryptocurrencies. Users can input their purchased ticker data, specify a time range, and choose a desired time interval to view a chart of price changes and the average price of the selected tickers.

## Features

- **View Ticker List**: Users can retrieve a list of all 541 tickers currently in the system.
- **Price Chart**: A price chart displaying the price changes of selected tickers between a specified start date and end date, based on a user-defined time interval.
- **Average Price**: Calculates the average price of selected tickers during the specified time frame based on the selected interval.

### Data Source
- The list of 541 tickers and the market data is retrieved from the Binance API.
- Market data is fetched with a 15-minute time frame starting from January 1, 2023, to October 1, 2024.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aref-Yazdanpanah/TickerChart.git
   cd TickerChart

2. **Create the Environment File**:
   ````bash
   touch .env


3. **Copy the following text into the .env file**:
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

## Handling Startup Errors:
If you encounter the following error:
   **ERROR: No container found for web_1**
This typically means that the web container started before the database container was ready. Since the web container depends on the database container, the project will not run correctly until both are ready.

## Solution:
To fix this issue, restart the web container by running the following command:
   ```bash
   make r
   ```


4. **Verify the Project is Running**:
After running the command, the project should be up and running. You can verify by visiting http://localhost:8000 in your web browser. If you are using a different port or host configuration, adjust accordingly.

5. **Stopping the Project**:
   ```bash
   make local-stack-down
   ```



## Performance Optimization

To optimize code and reduce the number of database queries, the following approach is recommended when fetching market data:

### Batch Fetching and Grouping Market Data

1. **Batch Fetch Market Data**:
   All market data for the specified ticker between `start_time` and `end_time` should be retrieved in a single query. This approach reduces the number of queries to just one for all market data within the specified date range.

2. **Group by Intervals**:
   After fetching the data, the results can be manually grouped in memory by the specified intervals. From this grouped data, the last close price for each interval can be extracted.

By implementing this strategy, significant improvements in the performance of the application can be achieved while minimizing the load on the database.



## Retrieving Data from Binance

To retrieve market data from Binance, the project includes a management command that fetches data from the Binance API. However, since Binance may have regional restrictions or filtering mechanisms, the Docker container must be configured to bypass these restrictions using a local proxy.

### Proxy Configuration for Binance API Access

In order to proxy the container to bypass the Binance filter and retrieve data successfully, you need to modify the Docker network configuration. This allows the container to use the local system's network, ensuring that it can communicate with Binance.

### Steps to Configure Docker for Binance API Access

1. **Modify the Docker Compose Network Mode**:

   The Docker container running the project must be proxied to the local system. To achieve this, you need to configure the `network_mode` for the `web` service and `db` service in the `docker-compose.yml` file.

   Open your `docker-compose.yml` file and ensure the following configuration is applied:

   ```yaml
   services:
      web:
         build: .
         network_mode: "host"


      db:
         build: .
         network_mode: "host"

   ```

2. **Modify the .env POSTGRES_HOST**:
Then replace POSTGRES_HOST in the .env file with the following text:
   ```bash
   POSTGRES_HOST=127.0.0.1
   ```

   When you set POSTGRES_HOST to 127.0.0.1, you're telling Django to connect to the PostgreSQL database that is expected to be running on the same host as the Django application. However, since you're using Docker with network_mode: 'host', both containers share the host's network stack, allowing them to communicate directly using localhost.


3. **Running Management Commands in the Web Container**:
   To interact with the project via the Django management commands within the Docker container, follow these steps:

   A. **Access the Web Container Shell**
   Run the following command to open an interactive shell (bash) inside the web container:
      ```bash
      make bash
      ```

   B. **Navigate to the Project Directory**
   After entering the web container, navigate to the TickerChart directory by running:
      ```bash
      cd TickerChart/
      ```

   C. **Fetch Tickers from Binance API**
   To access the Binance API through a local proxy (such as an HTTP or SOCKS proxy), ensure that the proxy server is running on your local machine. Then, use the HTTPS_PROXY environment variable to route the request through the proxy.

   Example using HTTP proxy (if your proxy server is running at 127.0.0.1:8889):
      ```bash
      HTTPS_PROXY=http://127.0.0.1:8889/ python manage.py fetch_all_symbols
      ```

   Example using SOCKS proxy (if your SOCKS proxy server is running at 127.0.0.1:1080):
      ```bash
      HTTPS_PROXY=socks5://127.0.0.1:1080/ python manage.py fetch_all_symbols
      ```

   These commands route the traffic through the specified proxy (HTTP or SOCKS) to fetch the ticker data from Binance.

   D. **Fetch Market Data from Binance API**
   Similarly, to fetch historical price data from the Binance API, run the following command:

   For HTTP proxy:
      ```bash
      HTTPS_PROXY=http://127.0.0.1:8889/ python manage.py fetch_historical_data
      ```

   For SOCKS proxy:
      ```bash
      HTTPS_PROXY=socks5://127.0.0.1:1080/ python manage.py fetch_historical_data
      ```

   These commands will retrieve market data from Binance while routing the traffic through the specified proxy.


   **Proxy Configuration Explanation**
   
   - **HTTP Proxy**:If using an HTTP proxy, set the HTTPS_PROXY environment variable to the HTTP proxy address in the format http://localhost:PORT/.

   - **SOCKS Proxy**:If using a SOCKS proxy, set the HTTPS_PROXY environment variable to the SOCKS proxy address in the format socks5://localhost:PORT/.



## Endpoints

To access detailed information about the endpoints in the project, you can utilize the Swagger or Redoc endpoints. Both of these endpoints are included in the project and offer interactive documentation for the API.


Swagger endpoint:
   ```bash
   schema/swagger-ui/
   ```

Redoc endpoint:
   ```bash
   schema/redoc/
   ```


## Libraries

[**django-debug-toolbar**](https://django-debug-toolbar.readthedocs.io/en/latest/)

"The Django Debug Toolbar is a configurable set of panels that display various debug information about the current request/response and when clicked, display more details about the panel's content."


## Testing
To ensure that the TickerChart project is functioning correctly, you can run the test suite provided.

### Running Tests

1. **Run Tests with Docker**:
   You can run the tests in the Docker environment using the following command:

   ```bash
   make test

### This command will execute the Django test suite inside the Docker container. The output will be similar to:
   ```bash
   Found 3 test(s).
   Creating test database for alias 'default'...
   System check identified no issues (0 silenced).
   /usr/local/lib/python3.11/site-packages/rest_framework/pagination.py:207: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'TickerChart.chartengine.models.Ticker'> QuerySet.
   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.031s

   OK
   Destroying test database for alias 'default'...
   ```
