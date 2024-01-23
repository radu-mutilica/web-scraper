# Deep Neuron Lab Backend Challenge

## About
This is a docker containerized application running in three separate docker containers.
A webscraper, a database and an API exposing one endpoint to query the scraped data.

When starting the app the following will happen:
1. All three containers will be built and started at once.
2. The scraper will proceed to query the "https://urparts.com" website for all
of their product inventory. All products scraped are then stored in a MongoDB instance.
3. The FastAPI endpoint will already be up and running and query-able. It will serve
incomplete data though, until the scraper finishes and exits.

## Running the app
When you're ready, start your application by running:

`docker compose up --build`

The API will be available to call at http://127.0.0.1:8000.
