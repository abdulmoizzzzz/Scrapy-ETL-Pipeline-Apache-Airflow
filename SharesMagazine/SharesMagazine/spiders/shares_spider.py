import scrapy
from SharesMagazine.items import SharesmagazineItem


class SharesSpiderSpider(scrapy.Spider):
    name = "shares_spider"
    allowed_domains = ["www.sharesmagazine.co.uk"]
    start_urls = ["https://www.sharesmagazine.co.uk/news/shares"]
    max_items = 100
    item_count = 0

    def parse(self, response):
        main_news = response.css(".brdr-under-sh5")
        for news in main_news:
            title = news.css(".txt-sh8::text").get()
            published_date = news.css(".dateIcon::text").get()
            title_link = news.css('.sb-content.padd-under.gutter-under-large.brdr-under-sh5 > a::attr(href)').get()
            
            if title and published_date and title_link:
                yield response.follow(title_link, callback=self.parse_detail, meta={'title': title, 'published_date': published_date, 'title_link': title_link})
                if self.item_count >= self.max_items:
                    return

        next_page = response.css(".next::attr(href)").get()
        if next_page is not None and self.item_count < self.max_items:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        title = response.meta['title']
        published_date = response.meta['published_date']
        title_link = response.meta['title_link']
        description_elements = response.css('p::text, p strong::text, p em::text, p span::text').getall()
        Description = " ".join(description_elements).strip()
        
        item = SharesmagazineItem()
        item["source_name"] = "SharesMagazine"
        print("source_name:", item["source_name"])
        item["title"] = title
        item["published_date"] = published_date
        item["title_link"] = title_link
        item["Description"] = Description

        self.item_count += 1
        
        yield item
