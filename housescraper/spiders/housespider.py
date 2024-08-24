import scrapy
from json import loads
from housescraper.items import HousescraperItem


class HousespiderSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains = ["www.rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/southwark-85215.html?page=1"]

    def parse(self, response):
        house_item = HousescraperItem()
        content = response.xpath("//script[contains(text(), 'window.__PRELOADED_STATE__')]/text()").get()
        content = content[len("window.__PRELOADED_STATE__ = "):]
        content = loads(content)
        properties  = content["results"]["properties"]
        for house_property in properties:
            house_item["address"] = house_property["address"]
            house_item["type"] = house_property["propertyType"]
            house_item["images"] = house_property["images"]
            house_item["transactions"] = house_property["transactions"]
            house_item["location"] = house_property["location"]
            house_item["url"] = house_property["detailUrl"]
            yield house_item
                
            current_page = int(content["pagination"]["current"])
            last_page = int(content["pagination"]["last"])
            if current_page < last_page:
                next_page = f"https://www.rightmove.co.uk/house-prices/southwark-85215.html?page={current_page + 1}"
                yield scrapy.Request(next_page, callback=self.parse)
            
            

        
