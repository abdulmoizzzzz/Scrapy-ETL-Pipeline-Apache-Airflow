import scrapy
from FidelityUk.items import FidelityukItem
from FidelityUk.itemloaders import FidelityProductLoader
from urllib.parse import urljoin


class FidelitySpiderSpider(scrapy.Spider):
    name = "fidelity_spider"
    allowed_domains = ["www.fidelity.co.uk"]
    start_urls = ["https://www.fidelity.co.uk/shares/stock-market-news/market-reports/?p=0&c=10"]
    item_count = 0

    def parse(self, response):
        fidelity_news = response.css(".read-more-article-container")
        for news in fidelity_news:
            title = news.css(".read-more-article-title a::text").get()
            published_date = news.css("small::text").get()
            title_link = news.css("h5 a").attrib["href"]

            # Converting relative URL to absolute URL
            title_link = urljoin(response.url, title_link)

            
            loader = FidelityProductLoader(item=FidelityukItem(), response=response)
           
            loader.add_value('source_name', 'Fidelity.co.uk')
            loader.add_value('title', title)
            loader.add_value('published_date', published_date)
            loader.add_value('title_link', title_link)
             
            yield scrapy.Request(title_link, callback=self.parse_news_page, meta={'loader': loader})
            self.item_count += 1
            if self.item_count >= 100:  # Stop scraping after 100 items
                return

        next_page = response.css(".fil-icon-arrow-r-light")
        if next_page is not None:
            next_page_url = response.urljoin(next_page.attrib["href"])
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_news_page(self, response):
        loader = response.meta['loader']
        Description = response.css(".sharecast-article-detail").xpath("normalize-space()").get()
        loader.add_value('Description', Description)
        
        yield loader.load_item()
