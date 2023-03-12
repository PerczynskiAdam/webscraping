## General info
Goal of this project was to web scrap the Motorhome for Sale from (https://rv.campingworld.com/rvclass/motorhome-rvs) that are running on Diesel.

## Setup
To run this project, install dependencies from requirements.txt and run:
```python -m main```

To run tests:
```python -m pytest```


## Problems
The biggest problem for me was to bypass Cloudflare and Captcha. I tried requests, cloudscraper library and was reading about proxies.
I found solution with optimized Selenium Chromedriver called undetected_chromedriver. It's working but it's quite slow.
It can be seep up with set executable path.

I think there is a problem with provided Web becuase I cannot reach pages 21 and higher.

I also wasn't sure how often I can hit the website so I decided to set sleep to 5 seconds after every request.

The next problem I encountered was static typing of BeautifulSoup library so I decided to skip mypy types validation.