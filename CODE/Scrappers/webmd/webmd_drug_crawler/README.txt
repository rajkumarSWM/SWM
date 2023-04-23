Crawling status: completed

Here are the steps to run a Scrapy-based Python crawler that extracts drug review data from WebMD:

1. Install Scrapy by running "pip3 install Scrapy" command.
2. From this current directory run the following command to grab all drugs and details page link:
3. Run "scrapy crawl webmd_drug_detail_page_crawler -O webmd_drug_detail_urls.json:json" command to get all the drug detail page links and store them in a JSON file.
4. Run "scrapy crawl webmd_drug_review_page_crawler -O webmd_drug_review_urls.json:json" command to get all the drug review page links and store them in a JSON file.
5. Run "scrapy crawl webmd_drug_review_crawler -O webmd_drugs_reviews.json:json" command to crawl all drug reviews and store them in a JSON file.

Alternatively, you can run "rundrugcrawler.sh" script to run the crawler. Make sure to install Scrapy and beautifulsoup4 libraries before running the script.

Library used(should be installed before running):
1. Scrapy
2. beautifulsoup4


