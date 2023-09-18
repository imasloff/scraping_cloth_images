import scrapy
import itertools
from scrapy import Request
from scrapy.selector import Selector
from scrapy_playwright.page import PageMethod
from fashion_images.items import ClothItem


class FashionSpider(scrapy.Spider):
    name = "fashion_spider"
    id_obj = itertools.count()
    # allowed_domains = ["www.shopcider.com"]
    # start_urls = ["https://www.shopcider.com/"]

    def start_requests(self):
        base_url = "https://www.shopcider.com/collection/"
        categories = ['top', 'bottom', 'dress']
        for cat in categories:
            url = base_url + cat
            yield Request(url, meta={ 
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', '.product-item a[title]'),
                    PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                ],
                'errback': self.errback,
            })


    async def parse(self, response):
        start_url = "https://www.shopcider.com"
        page = response.meta['playwright_page']

        selectors = set()
        while len(selectors) < 350:
            prev_selectors_set = selectors
            selectors_list = await page.query_selector_all('.product-item a[title]')
            selectors = set([await s.get_attribute('href') for s in selectors_list])

            if not selectors - prev_selectors_set:
                self.logger.info("No more new selectors added. Stopping.")
                break

            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')

            await page.wait_for_timeout(2000)
        
        await page.close()

        for selector in selectors:
            item_url = selector
            url = start_url + item_url
            yield Request(url, callback=self.parse_item)


    def parse_item(self, response):
        cloth_item = ClothItem()
        cloth_item['id'] = next(FashionSpider.id_obj)
        cloth_item['category'] = response.url
        cloth_item['title'] = response.css('.product-detail-title::text').get()
        cloth_item['image_urls'] = response.css(
            '.cider-image[data-img*="product"]:not([data-img*="?"])::attr(data-img)'
        ).getall()
        yield cloth_item


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()