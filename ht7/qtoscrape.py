import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    # Initialize a counter for the number of pages processed
    page_count = 0
    max_pages = 2

    def parse(self, response):
        # Extract quotes and authors from the current page
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').get(),
                'quote': quote.css('span.text::text').get(),
            }

        # Increment the page count
        self.page_count += 1

        # Follow the next page link if available and within the page limit
        if self.page_count < self.max_pages:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
