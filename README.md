# (GTAS) GreekTrain Announcements Scraper 

This is a small simple scrapper I made in an afternoon to get the latest news of the greek trains. I made it because I wanted to get the latest news of the company and I didn't want to manually check the website every day. It scrapes the news from their [website](https://www.hellenictrain.gr/en/announcements) and returns the latest news articles in json format using a simple API.

## REQUIREMENTS
* Python 3.8
* Venv
* Pip

## Installation
* Create a virtual environment
    * ``python3 -m venv venv``
* Activate the virtual environment
    * ``source venv/bin/activate``
* Install the requirements
    * ``pip install -r requirements.txt``
* Run the scrapper
    * ``python scrape_api.py``

## Usage
The program will respond to the following endpoints:
* default: Returns the latest news articles in json format of the first page of site
    * ``?page=2``: Returns the latest news articles in json format of the **3rd** page of site
    * ``en=true``: All the news will be returned in english
* ``/latest``: Returns the latest news article in json format
    * ``en=true``: The news will be returned in english

## Response
The response will be in json format and will contain the following fields:
* ``title``: The title of the news article
* ``url``: The url of the news article
* ``content``: The content of the news article
* ``id``: The id of the news article scraped from the website (can be used as a unique identifier)
* ``date``: The date of the news article in unix timestamp format , null if the date is not available
