import scrapy
from scrapy.http import Request

from pep_parse.items import PepParseItem
from pep_parse.settings import PEP_SPIDER_URL


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = (PEP_SPIDER_URL,)
    start_urls = [f'https://{PEP_SPIDER_URL}/']

    def parse(self, response, **kwargs):
        links = response.css('tbody tr a[href^="pep-"]::attr(href)').getall()
        for link in links:
            yield Request(response.urljoin(link), callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        status = response.css('dt:contains("Status")+dd abbr::text').get()
        if title:
            title_parts = title.split()
            if len(title_parts) >= 4:
                _, number, _, *name = title_parts
                data = {
                    'number': number,
                    'name': ' '.join(name).strip(),
                    'status': status,
                }
                yield PepParseItem(data)
