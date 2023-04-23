
import scrapy
import os
import json
import re
import urllib.parse as url_parser

from webmd_drug_crawler.webmd_drug_crawler.items import DrugReviewItem

HOME_URL = 'https://www.webmd.com'


#  scrapy crawl webmd_drug_review_crawler -O webmd_drugs_reviews.json:json
class WebMDDrugReviewSpider(scrapy.Spider):
    name = 'webmd_drug_review_crawler'
    allowed_domains = ['webmd.com']

    startUrls = []
    drugReviewUrlToDrugDetailsMap = {}
    with open(os.path.dirname(__file__) + '/../../webmd_drug_review_urls.json') as f:
        drugs = json.load(f)
        for drug in drugs:
            startUrls.append(drug['reviewPageUrl'])
            drugDetails = [drug['name'],drug['detail_page_redirected_url'],]
            reviewPageUrl = drug['reviewPageUrl']
            drugDetails.append(reviewPageUrl)
            if '?drugid=' in reviewPageUrl:
                reviewPageUrl = reviewPageUrl[0: reviewPageUrl.find('?drugid=')]
            drugReviewUrlToDrugDetailsMap[reviewPageUrl] = drugDetails

    def parse(self, response):
        print("Processing: " + response.url)

        count = 1
        for review in response.css('#ratings_fmt > div.userPost'):
            reviewPageUrl = response.url
            if '?drugid=' in reviewPageUrl:
                reviewPageUrl = reviewPageUrl[0: reviewPageUrl.find('?drugid=')]
            drugDetails = self.drugReviewUrlToDrugDetailsMap[reviewPageUrl]

            drugReviewItem = DrugReviewItem()
            drugReviewItem['drug_name'] = drugDetails[0]
            drugReviewItem['drug_detail_page'] = drugDetails[1]
            drugReviewItem['drug_review_page'] = drugDetails[2]
            drugReviewItem['health_conditionName'] = re.sub(r'\s+', ' ', review.css('div.postHeading.clearfix > div.conditionInfo::text').extract_first().strip())[len('Condition: '):]
            drugReviewItem['timestamp'] = review.css('div.postHeading.clearfix > div.date::text').extract_first().strip()
            reviewerDetails = re.sub(r'\s+', ' ', review.css('p.reviewerInfo::text').extract_first().strip())
            drugReviewItem['reviewer_full_det'] = reviewerDetails

            if reviewerDetails.find('Reviewer: ') != -1:
                reviewerDetails = reviewerDetails[len('Reviewer: '):]

                reviewerName = 'unknown'
                if reviewerDetails.find(', ') != -1:
                    reviewerName = reviewerDetails[0: reviewerDetails.find(',')]
                    reviewerDetails = reviewerDetails[reviewerDetails.find(', ') + 2:]
                    reviewerDetails = reviewerDetails.strip()
                drugReviewItem['reviewerName'] = reviewerName

                ageRange = 'unknown'
                # if the reviewer details also contains the age details
                if reviewerDetails[0].isdigit() and '-' in reviewerDetails:
                    start = reviewerDetails[0: reviewerDetails.find('-')].strip()
                    reviewerDetails = reviewerDetails[reviewerDetails.find('-')+1:].strip()
                    end = reviewerDetails[0: reviewerDetails.find(' ')]
                    ageRange = str(start) + '-' + str(end)
                drugReviewItem['patient_ageRange'] = ageRange

                gender = 'unknown'
                if reviewerDetails.find('Female') != -1:
                    gender = 'Female'
                elif reviewerDetails.find('Male') != -1:
                    gender = 'Male'
                drugReviewItem['patient_gender'] = gender

                duration = 'unknown'
                if reviewerDetails.find('on Treatment for ') != -1:
                    start_idx = reviewerDetails.find('on Treatment for ')
                    end_idx = reviewerDetails.find(' (')
                    duration = reviewerDetails[start_idx + len('on Treatment for '): end_idx]
                drugReviewItem['treatment_duration'] = duration

                category = 'unknown'
                if reviewerDetails.find('(Patient)') != -1:
                    category = 'Patient'
                if reviewerDetails.find('(Caregiver)') != -1:
                    category = 'Caregiver'
                drugReviewItem['reviewer_category'] = category
            else:
                drugReviewItem['reviewerName'] = 'unknown'
                drugReviewItem['patient_ageRange'] = 'unknown'
                drugReviewItem['patient_gender'] = 'unknown'
                drugReviewItem['treatment_duration'] = 'unknown'
                drugReviewItem['reviewer_category'] = 'unknown'

            comment = review.xpath('// *[ @ id = "comFull' + str(count) + '"] / text()').extract_first()
            if comment:
                comment = re.sub(r'\s+', ' ', comment)
            else:
                comment = ''
            drugReviewItem['review_comment'] = comment

            numPeopleFoundUseful = 0
            found_helpful = re.sub(r'\s+', ' ', review.css('div > p.helpful::text').extract_first().strip())
            if found_helpful[0].isdigit():
                numPeopleFoundUseful = int(found_helpful[0: found_helpful.find(' ')])
            drugReviewItem['num_of_people_found_useful'] = numPeopleFoundUseful

            drugReviewItem['effectiveness_rating'] = review.css(
                '#ctnStars > div.catRatings.firstEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip()[len('Current Rating: '):]

            drugReviewItem['ease_of_use_rating'] =  review.css(
                '#ctnStars > div:nth-child(2) > p.inlineRating.starRating > span::text').extract_first().strip()[len('Current Rating: '):]

            drugReviewItem['satisfaction_rating'] = review.css(
                '#ctnStars > div.catRatings.lastEl.clearfix > p.inlineRating.starRating > span::text').extract_first().strip()[len('Current Rating: '):]

            count += 1
            yield drugReviewItem

        if response.xpath('//*[@id="ratings_fmt"]/div/div/a[contains(text(), "Next")]'):
            current_page_url = response.url
            print('Current Page: '+current_page_url)

            urlParts = url_parser.urlsplit(current_page_url)
            params = url_parser.parse_qs(urlParts.query)
            lastPageIdx = int(params['pageIndex'][0])
            lastPageIdx = lastPageIdx + 1
            params['pageIndex'] = [str(lastPageIdx)]
            newQuery = ''
            count = 0
            for param_key in params:
                if count != 0:
                    newQuery = newQuery + '&'
                newQuery = newQuery + param_key + '=' + params[param_key][0]
                count += 1

            next_page_url = url_parser.urlunsplit((urlParts[0], urlParts[1], urlParts[2], newQuery, urlParts.fragment))
            print('Next Page: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
