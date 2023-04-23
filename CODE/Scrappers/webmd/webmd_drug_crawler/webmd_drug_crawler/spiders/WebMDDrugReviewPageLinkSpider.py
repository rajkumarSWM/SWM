import scrapy
import os
import json

from webmd_drug_crawler.webmd_drug_crawler.items import DrugReviewPageLinkItem

HOME_URL = 'https://www.webmd.com'



class WebMDDrugReviewPageLinkSpider(scrapy.Spider):
    name = 'webmd_drug_review_page_crawler'
    allowed_domains = ['webmd.com']

    startUrls = []
    drugUrlToDrugNameMap = {}
    with open(os.path.dirname(__file__) + '/../../webmd_drug_detail_urls.json') as f:
        drugs = json.load(f)
        for drug in drugs:
            startUrls.append(drug['detail_page_url'])
            drugUrlToDrugNameMap[drug['detail_page_url']] = drug['name']

    def parse(self, response):

        print("Processing: " + response.request.url)
        redirectedUrl = response.request.url
        
        if response.request.meta.get('redirect_urls'):
            requestedUrl = response.request.meta['redirect_urls'][0]
        else:
            requestedUrl = response.request.url

        Css = '#ContentPane29 > div.drug-monograph-container > div.drug-information > div.drug-names > div > ' \
              'a.drug-review::attr(href) '
        
        reviewPageUrl = response.css(Css).extract_first()
        if reviewPageUrl is not None and reviewPageUrl != '':
            reviewPageUrl = HOME_URL + reviewPageUrl
            drugReviewLinkItem = DrugReviewPageLinkItem()
            drugReviewLinkItem['name'] = self.drugUrlToDrugNameMap[requestedUrl]
            drugReviewLinkItem['detail_page_url'] = requestedUrl
            drugReviewLinkItem['detail_page_redirectedUrl'] = redirectedUrl
            drugReviewLinkItem['reviewPageUrl'] = reviewPageUrl + '&pageIndex=0&sortby=3&conditionFilter=-1'

            return drugReviewLinkItem