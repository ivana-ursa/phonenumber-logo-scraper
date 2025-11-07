import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from phonenumber_logo_scraper.spiders.phonenumber_logo_spider import PhoneNumberLogoSpider
import logging

# Suppress logging from the asyncio library
# This keeps the console output cleaner
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

# Function to initialize and start the Scrapy crawl
def start_search(url):
    # Initialize Crawler Process with project settings
    process = CrawlerProcess(get_project_settings())

    # Queue the spider for crawling
    process.crawl(PhoneNumberLogoSpider, url = url)

    # Start the crawl
    process.start() 


# Standard Python entry point
if __name__ == '__main__':
    # Check if a command-line argument (url) was provided
    try:
        url = sys.argv[1]
    except IndexError:
        print("Error: Starting URL missing.")
        # Exit if no URL is provided
        sys.exit(1)

    # Start the scraping process
    start_search(url)