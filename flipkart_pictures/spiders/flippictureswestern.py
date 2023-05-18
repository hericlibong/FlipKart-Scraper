import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class FlippictureswesternSpider(CrawlSpider):
    name = "flippictureswestern"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/clothing-and-accessories/dresses-and-gown/dress/women-dress/pr?sid=clo,odx,maj,jhy&otracker=categorytree&otracker=nmenu_sub_Women_0_Dresses"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//div[@class='_2B099V']//a[@class='IRpwTa _2-ICcC']"), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths = "//a[@class='_1LKTO3']")))

    def parse_item(self, response):
        url = response.url
        title = response.xpath("//h1/span[2]/text()").get()
        brand = response.xpath("//h1/span[@class='G6XhRU']/text()").get()
        main_picture = response.xpath("//div[@class='_312yBx SFzpgZ']/img/@src").get()
        current_price = response.xpath("//div[@class='_25b18c']/div[1]/text()").get()
        original_price = response.xpath("//div[@class='_25b18c']/div[2]/text()[2]").get()

        try:
            discount_rate = response.xpath("//div[@class='_3Ay6Sb _31Dcoz pZkvcx']/span/text()").get().replace('off', '')
        except:
            discount_rate = None
        
        try:
            stars = response.xpath("//div[@class='_3LWZlK _138NNC']/text()").get().strip()
        except:
            stars = None 

       
        try:
            ratings_reviews = response.xpath("//span[@class='_2_R_DZ _2IRzS8']/span/text()").get().strip()
        except:
            ratings_reviews = None

    
        ratings = None
        reviews = None
        if ratings_reviews:
            match = re.search(r'(\d+) ratings and (\d+) reviews', ratings_reviews)
            if match:
                ratings = int(match.group(1))
                reviews = int(match.group(2))
        try :
            sellername = response.xpath("//div[@id='sellerName']//span/text()").get().strip() 
        except :
            sellername = None
        
        try:
            sellerstar = response.xpath("//div[@id='sellerName']//div/text()").get().strip()
        except :
            sellerstar = None 
        try:
            left_pictures = response.xpath("//div[@class='_2mLllQ']/ul/li//img/@src")
            left_pictures = [pic.get().replace('image/128/128/', 'image/832/832/') for pic in left_pictures]
        except:
            left_pictures = None

        try : 
            right_pictures = response.xpath("//div[@class='ffYZ17 _3DM78Z col col-12-12'][1]//ul/li//img/@src")
            right_pictures = [pic.get().replace('image/180/180/', 'image/832/832/') for pic in right_pictures]
        except :
            right_pictures = None

        product_id = None
        match = response.xpath("//meta[@property='og:url']/@content")
        if match:
            url_content = match.get()
            product_id = url_content.rsplit('/', 1)[-1]
        yield {
            'product_id':product_id,
            'url': url,
            'title':title, 
            'brand':brand,
            'discount_rate':discount_rate,
            'current_price': current_price,
            'original_price': original_price,
            'stars':stars,
            'ratings':ratings,
            'reviews':reviews,
            'sellername': sellername,
            'sellerstars': sellerstar, 
            'main_picture':main_picture,
            'left_pictures':left_pictures, 
            'right_pictures': right_pictures
        }
