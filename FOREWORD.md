# Deep Neuron Lab Backend Challenge

This has been quite a fun project. I particularly found the scraping part interesting. Having
developed and interfaced with webscrapers in the past, I felt right at home. In my experience, the
scrapers I have worked with were designed using `requests` and `BeautifulSoup` or `PyQuery`. I
decided to keep it simple and try out `scrapy` for the first time. While the concepts
were the same, the under the hood automatic handling of http requests, following urls and logging
eliminated most of the boilerplate associated with a task like this.

The structure of the "urparts" website informed the traversal algorithm to naturally mimic DFS.

## Project structure

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
    ...
```

## Assumptions made

I started this task by assuming that the functionality of the crawler is fully defined by the provided
set of requirements. These were sparse, so in places where functionality was not clear I took the
following liberties:

- performance: by default, fires off multiple requests, up to a max of CONCURRENT_REQUESTS. In this 
website's particular case I noticed that the default was a bit too high (experienced throttles).
I played around with multiple values and landed on 6 as a good balance.
- design: as the task was to scrape this particular website I wrote the parsing functions to be
specific. In a real life environment that might not be the case.
- multiple scrapes: as it is now, repeated scrapes will keep updating the same collection with
duplicate items. I left it as such because I was torn between two designs:
  - have each subsequent scrape use a new collection (that way we keep historical data)
  - use just one collection but index all items uniquely, and change the scraper to do an upsert to
the database instead of an insert.
- testing: out of the three separate services (database, scraper, api), for this scenario, only the
scraper has a resemblance of actual business logic in it, the API is purely boilerplate which
returns mostly raw data. In my experience, testing web scrapers is a can of worms. What we used
to do was mock the requests library to return cached versions of the HTML documents in question.
This mostly served to increase code coverage in my opinion, as the constant changes in website 
HTML bodies made the tests useless in the long run.
