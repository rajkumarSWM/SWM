import scrapy
from string import ascii_lowercase

from webmd_drug_crawler.webmd_drug_crawler.items import DrugDetailPageLinkItem

BASE_URL = 'https://www.webmd.com/drugs/2/alpha/'
HOME_URL = 'https://www.webmd.com'


class WebMDDrugDetailSpider(scrapy.Spider):
    name = 'webmd_drug_detail_page_crawler'
    allowed_domains = ['webmd.com']

    startUrl = [BASE_URL + '0']
    for ch1 in ascii_lowercase:
        for ch2 in ascii_lowercase:
            startUrl.append(BASE_URL + ch1 + '/' + ch1 + ch2)
    print(startUrl)

    def parse(self, response):
        print("Processing: " + response.url)

        # ContentPane30 > div.drug-list-container > ul > li
        drugItems = []
        # if the page has this container listing drugs then only iterate and collect drug detail page url
        for drug in response.css('#ContentPane30 > div.drug-list-container > ul > li'):
            drugLinkItem = DrugDetailPageLinkItem()
            drugLinkItem['name'] = drug.xpath('a/text()').extract_first().strip()
            drugLinkItem['detail_page_url'] = HOME_URL + drug.xpath('a/@href').extract_first().strip()
            drugItems.append(drugLinkItem)

        return drugItems
