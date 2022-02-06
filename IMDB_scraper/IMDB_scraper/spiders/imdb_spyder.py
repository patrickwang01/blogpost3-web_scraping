import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

# C:/Users/wangp/anaconda3/Scripts/activate

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt10293938/']

    
    def parse(self, response):
        
        # get href portion of 'cast and crew' item
        cast = response.css("li.ipc-inline-list__item a")[2].attrib["href"]

        # join href with main url 
        cast_crew = response.urljoin(cast)

        yield scrapy.Request(cast_crew, callback = self.parse_full_credits)

    
    def parse_full_credits(self, response):
        
        # get href portion for each actor thumbnail
        actor_names = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # set main website link
        main = "https://imdb.com"

        # combine main website url with actor href 
        actor_links = [main + actor for actor in actor_names]

        # loop through entire list of actor urls
        for link in actor_links:
            yield scrapy.Request(link, callback = self.parse_actor_page)
        
    
    def parse_actor_page(self, response):
        
        # extract actor name 
        actor_name = response.css("span.itemprop::text").get() 
 
        rows = response.css("div.filmo-row")

        # loop through all the movies/tv shows
        for row in rows:
            
            # obtain movie/tv show name
            movie_or_TV_name = row.css("b a::text").get()

            # create dictionary with actor name and movie/tv show name
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }