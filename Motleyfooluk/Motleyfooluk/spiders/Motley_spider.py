import scrapy
from scrapy_selenium import SeleniumRequest

class MotleyfoolSpiderSpider(scrapy.Spider):
    name = "Motley_spider"
    allowed_domains = ["fool.co.uk"]
    start_urls = ["https://www.fool.co.uk/recent-headlines/"]
    max_items = 100

    def start_requests(self):
        
        from scrapy_selenium import SeleniumRequest

        
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=20)  

    def parse(self, response):
        self.logger.debug("Parsing URL: %s", response.url)

       
        links = response.selector.xpath('//main//a/@href').getall()

        news_articles = response.css("article")
      
        for index, article in enumerate(news_articles):
            title = article.css("h3::text").get()
            published_date = article.css(".article-meta time::text").get()
            article_meta_text = " ".join(article.css(".article-meta ::text").getall()).strip()
            publisher_name = article_meta_text.split("|")[-1].strip()

           
            title_link = links[index] if index < len(links) else None

            yield scrapy.Request(
                title_link,
                callback=self.parse_description,
                meta={
                    'title': title,
                    'published_date': published_date,
                    'publisher_name': publisher_name,
                    'source_name': 'The Motley Fool',
                }
            )

            self.max_items -= 1
            if self.max_items <= 0:
                self.logger.info("Maximum items limit reached. Stopping scraping.")
                return

       
        next_page_url = response.css("a.next.page-numbers::attr(href)").get()
        if next_page_url and self.max_items > 0:
            yield SeleniumRequest(url=next_page_url, callback=self.parse, wait_time=20)  # Adjust wait_time as needed

    def parse_description(self, response):
        Description_text = " ".join(response.css(".entry-content *:not(script):not(style)::text").getall()).strip()

        yield {
            'source_name': response.meta['source_name'],
            'title': response.meta['title'],
            'title_link': response.url,
            'published_date': response.meta['published_date'],
            'publisher_name': response.meta['publisher_name'],
            'Description': Description_text,
            
        }
