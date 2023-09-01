import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """A Spider for PEPs."""

    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Parse the initial page and follow links."""

        for url in response.xpath(
            '//*[@id="numerical-index"]').css('tbody').css('a[href]'
                                                           ):
            yield response.follow(url, callback=self.parse_pep)

    def parse_pep(self, response):
        """Parse a page and extract information."""

        title = response.css('h1.page-title::text').get().split(' – ')
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        yield PepParseItem(
            {
                'number': title[0][4:],
                'name': title[1],
                'status': status if status else 'None'
            }
        )
