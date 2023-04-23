
cd /Users/devaduttsanka/PycharmProjects/webmd/webmd_drug_crawler

scrapy crawl webmd_drug_detail_page_crawler -O webmd_drug_detail_urls.json:json

scrapy crawl webmd_drug_review_page_crawler -O webmd_drug_review_urls.json:json

scrapy crawl webmd_drug_review_crawler -O webmd_drugs_reviews.json:json