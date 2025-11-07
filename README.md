# phonenumber-logo-scraper
Scrapy web scraper for phone number and company logo extraction

## Description
The goal of this project is to find, extract, and output all phone numbers and a logo URL that are present on the website.

## Dependencies
- Python 3.12.
- Scrapy 2.13.3
- Playwright 1.55.0

## Getting started
Clone the repository:
```bash
git clone https://github.com/ivana-ursa/phonenumber-logo-scraper.git
```

In terminal navigate to the project directory:
```bash
cd phonenumber-logo-scraper
```

### Install and Run via Docker

Build a Docker image:
```bash
docker build . -t scraper_app
```
Run:
```bash
docker run scraper_app {website-url}
```

### Install and Run via Python

Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
playwright install --with-deps
```

Run:
```bash
python extract.py {website-url}
```

To deactivate virtual environment:
```bash
deactivate
```