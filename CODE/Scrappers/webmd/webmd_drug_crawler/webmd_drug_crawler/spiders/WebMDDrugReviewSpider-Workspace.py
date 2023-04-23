
import scrapy
import re

#  scrapy crawl webmd_drug_review_crawler -O patient_info_forums.json:json
class WebMDDrugReviewSpider(scrapy.Spider):
    name = 'webmd_drug_review_crawler'
    allowed_domains = ['webmd.com']

    startUrls = [
        'https://www.webmd.com/drugs/drugreview-1082-aspirin+oral.aspx'
    ]

    def parse(self, response):
        print("Processing: " + response.url)

        count = 1
        for review in response.css('#ratings_fmt > div.userPost'):
            print('\n')
            print(review.css('div.postHeading.clearfix > div.conditionInfo::text').extract_first().strip())
            print(review.css('div.postHeading.clearfix > div.date::text').extract_first().strip())
            print(review.css('p.reviewerInfo::text').extract_first().strip())
            print(review.xpath('// *[ @ id = "comFull' + str(count) +'"] / text()').extract_first())
            print(re.sub(r'\s+', ' ', review.css('div > p.helpful::text').extract_first().strip()))
            print(review.css('#ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())
            print(review.css('#ctnStars > div:nth-child(2) > p.inlineRating.starRating > span::text').extract_first().strip())
            print(review.css('#ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip())

            count += 1