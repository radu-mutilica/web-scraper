# Simple web scraper

## About
This is a docker containerized application running in three separate docker containers.
A webscraper, a database and an API exposing one endpoint to query the scraped data.

When starting the app the following will happen:
1. All three containers will be built and started at once.
2. The scraper will proceed to query the "https://urparts.com" website for all
of their product inventory. All products scraped are then stored in a MongoDB instance.
3. The FastAPI endpoint will already be up and running and query-able. It will serve
incomplete data though, until the scraper finishes and exits.

## Project structure
The code is structured in two separate projects:

```
dnl/
    dnl_api/ # code for the fastapi
        Dockerfile
        requirements.txt
        ...
    dnl_scraper/ # code for the scraper
        Dockerfile
        requirements.txt
        ...
    FOREWORD.md # some details about the homework
    README.md # read this to start containers
    compose.yaml
    ...
```

- dnl_api: python project containing the API code.
- dnl_scraper: python project containing the scraper code.
- compose.yaml: at top-level to deploy the two different projects.

## Running the app
When you're ready, start your application by running:

`docker compose up --build`

The API will be available to call at http://127.0.0.1:8000.
