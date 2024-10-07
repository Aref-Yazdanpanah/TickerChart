# Ticker Price Tracker

This project allows users to track and analyze the price movements of various tickers such as Bitcoin, Ethereum, or other cryptocurrencies. Users can input their purchased ticker data, specify a time range, and choose a desired time interval to view a chart of price changes and the average price of the selected tickers.

## Features

- **View Ticker List**: Users can retrieve a list of all 541 tickers currently in the system.
- **Price Chart**: A price chart displaying the price changes of selected tickers between a specified start date and end date, based on a user-defined time interval.
- **Average Price**: Calculates the average price of selected tickers during the specified time frame based on the selected interval.

### Data Source
- The list of 541 tickers and the market data is retrieved from the Binance API.
- Market data is fetched with a 15-minute time frame starting from January 1, 2023, to October 1, 2024.

### Docker Setup
To run the application, we use Docker. Ensure that the network mode is properly configured to proxy the web container to the host system to fetch data from the Binance API.

### Prerequisites

- Docker and Docker Compose installed on your machine.
- The network configuration should allow local proxying, so make sure the following is set in your `docker-compose.yml`:

```yaml
services:
  web:
    build: .
    network_mode: "host"
