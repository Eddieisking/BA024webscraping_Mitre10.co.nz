"""
Project: Web scraping for customer reviews
Author: Hào Cui
Date: 06/20/2023
"""
import json
import math
import re

import scrapy
from scrapy import Request

from webscrapy.items import WebscrapyItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["www.mitre10.co.nz", "api.bazaarvoice.com"]

    def start_requests(self):
        # keywords = ['dewalt', 'Stanley', 'Black+Decker', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Facom', 'MAC Tools', 'Vidmar', 'Lista', 'Irwin Tools', 'Lenox', 'Proto', 'CribMaster', 'Powers Fasteners', 'cub-cadet', 'hustler', 'troy-bilt', 'rover', 'BigDog Mower', 'MTD']
        exist_keywords = ['dewalt', 'stanley', 'Black+Decker', 'Craftsman', 'Irwin Tools', 'Lenox']
        # company = 'Stanley Black and Decker'

        # from search words to generate product_urls
        for keyword in exist_keywords:
            push_key = {'keyword': keyword}

            search_url = f'https://www.mitre10.co.nz/shop/search?text={keyword}&q={keyword}'

            yield Request(
                url=search_url,
                callback=self.parse,
                cb_kwargs={**push_key},
            )

    def parse(self, response, **kwargs):

        # Extract the pages of product_urls
        page_string = response.xpath('//div[@class="result-count"]/text()')[0].get()
        numbers = re.findall(r'\d+', page_string)
        start, end, total = [int(num) for num in numbers]
        pages = math.ceil(total / (end + 1 - start))

        # Based on pages to build product_urls
        keyword = kwargs['keyword']
        product_urls = [f'https://www.mitre10.co.nz/shop/search?q={keyword}&cmsPage=0&page={page}&inStockSelectedStore=false&inStockNationwide=false' for page
                        in range(0, pages)]

        for product_url in product_urls:
            yield Request(url=product_url, callback=self.product_parse)

    def product_parse(self, response: Request, **kwargs):
        product_list = response.xpath('/html/body//div[@class="container"]/div[@class="row"]//div[@unbxdattr="product"]')

        for product in product_list:
            product_name = product.xpath('.//span[@class="product--name"]/text()')[0].extract()
            product_sku = product.xpath('./@data-sku')[0].extract()
            product_reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey' \
                                  f'=caWPwgJ2pghd4RhrgktdyVmJ4O5Znc6f8osLEjGCseuyY&apiversion=5.5&displaycode=14909' \
                                  f'-en_nz&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0' \
                                  f'=productid%3Aeq%3A' \
                                  f'{product_sku}&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_NZ&sort.q0=submissiontime' \
                                  f'%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts' \
                                  f'%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_NZ' \
                                  f'&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_NZ&filter_comments.q0' \
                                  f'=contentlocale%3Aeq%3Aen*%2Cen_NZ&limit.q0=8&offset.q0=0&limit_comments.q0=3 '

            yield Request(url=product_reviews_url, callback=self.review_single_parse, meta={'product_name': product_name})

    def review_single_parse(self, response: Request, **kwargs):
        product_name = response.meta['product_name']
        datas = json.loads(response.body)
        batch_results = datas.get('BatchedResults', {})

        offset_number = 0
        limit_number = 0
        total_number = 0

        if "q1" in batch_results:
            result_key = "q1"
        else:
            result_key = "q0"

        offset_number = batch_results.get(result_key, {}).get('Offset', 0)
        limit_number = batch_results.get(result_key, {}).get('Limit', 0)
        total_number = batch_results.get(result_key, {}).get('TotalResults', 0)

        for i in range(limit_number):
            item = WebscrapyItem()
            results = batch_results.get(result_key, {}).get('Results', [])

            try:
                item['review_id'] = results[i].get('Id', 'N/A')
                item['product_name'] = product_name
                item['customer_name'] = results[i].get('UserNickname', 'N/A') if results[i].get('UserNickname', 'N/A') else 'Ananymous'
                item['customer_rating'] = results[i].get('Rating', 'N/A')
                item['customer_date'] = results[i].get('SubmissionTime', 'N/A')
                item['customer_review'] = results[i].get('ReviewText', 'N/A')
                item['customer_support'] = results[i].get('TotalPositiveFeedbackCount', 'N/A')
                item['customer_disagree'] = results[i].get('TotalNegativeFeedbackCount', 'N/A')

                yield item
            except Exception as e:
                print('Exception:', e)
                break

        if (offset_number + limit_number) < total_number:
            offset_number += limit_number
            next_page = re.sub(r'limit.q0=\d+&offset.q0=\d+', f'limit.q0={30}&offset.q0={offset_number}', response.url)
            yield Request(url=next_page, callback=self.review_single_parse, meta={'product_name': product_name})

