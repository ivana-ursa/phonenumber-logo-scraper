import scrapy
import re

class PhoneNumberLogoSpider(scrapy.Spider):

    name = 'phonenumber_logo_spider'

    # The constructor for the spider
    def __init__(self, url, **kwargs):
        # Call the parent class constructor
        super().__init__(**kwargs)
        # Store the starting URL
        self.url = url
        # Flag to enable/disable dynamic content rendering with Playwright
        self.dynamic = True     # change to False to turn off the the search with Playwright

    # Defines the initial request the spider will make
    async def start(self):
        yield scrapy.Request(url = self.url, 
                             callback = self.parse,
                             headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",},
                             meta={'playwright': self.dynamic, "playwright_include_page": self.dynamic}   
        )
      
    # The callback method that processes the HTTP response
    def parse(self, response):
        # Extract phone numbers from the response content
        self.parse_numbers(response)
        # Extract the company logo URL from the response content
        self.parse_logo(response)

    # Method to find and extract a potential company logo URL
    def parse_logo(self, response):
        # XPath query to find an <img> tag that likely represents a logo
        logo = response.xpath(
                '//div//img['
                '(contains(translate(@src, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "logo") '
                'or contains(translate(@alt, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "logo")) '
                'and (contains(@src, ".svg") or contains(@src, ".png") or contains(@src, ".jpg") or contains(@src, ".jpeg"))'
                ']/@src'
            ).get()
        
        # Check if an image source was found 
        if logo != None:
            # Turn relative URL into absolute URL
            print(response.urljoin(logo))
        else:
            print('None')

    # Method to extract potential phone numbers 
    def parse_numbers(self, response):
        # Regular expression for a broad range of phone number formats
        phone_number_regex = re.compile(r"(^|(?<=[:\s]))(?<![\d,])(\+?\d{1,3}[-\s\/]?)?\(?\d{1,6}\)?[-\s\/]?\d{1,4}[-\s\/]?\d{2,4}[-\s\/]?\d{1,6}")

        # Get all visible text from the <body> of the HTML
        texts = response.xpath('//body//*[not(self::script) and not(self::style)]/text()').getall()
        # Join all extracted text into one string for regex search
        full_text = ' '.join(t for t in texts)
        # Find all matches of the phone number regex in the text
        full_matches = [m.group(0) for m in phone_number_regex.finditer(full_text)]
        # Clean and filter the potential phone numbers
        phone_numbers = self.clean_phone_numbers(full_matches)

        # Output the results
        if len(phone_numbers) == 0:
            print('None')
        else:
            print(', '.join(phone_numbers))

    # Method to clean and filter the extracted phone numbers
    def clean_phone_numbers(self, numbers):
        # Regular expression to detect common postal codes which might be identified as phone numbers
        potential_postal_code_regex = re.compile(r"\b\d{6}\b")
        # Regular expression to remove non-digit characters, except for +, (, and )
        cleaning_regex = re.compile(r"[^\d\+\(\)]")
        cleaned_numbers = set() # Use set to remove duplicates

        for n in numbers:
            # Count the number of digits in the potential phone number
            num_of_digits = sum(i.isdigit() for i in n)
            # Filter criteria: not a postal code and has between 6 and 15 digits
            if not potential_postal_code_regex.match(n) and 6 <= num_of_digits <= 15:
                # Replace unwanted characters with a space
                clean_n = cleaning_regex.sub(' ', n)
                # Add the cleaned number to the set
                cleaned_numbers.add(clean_n)

        return cleaned_numbers
    
    


