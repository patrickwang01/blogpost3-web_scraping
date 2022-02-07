import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt10293938/']

    
    def parse(self, response):
        '''
        Function that parses the main site of the movie/tv-show and extracts the href of the 'Cast and Crews' tab. 
        Yields the url for the 'Cast and Crews' site and calls parse_full_credits afterwards
        '''

        # get href portion of 'cast and crew' item
        cast = response.css("li.ipc-inline-list__item a")[2].attrib["href"]

        # join href with main url 
        cast_crew = response.urljoin(cast)

        yield scrapy.Request(cast_crew, callback = self.parse_full_credits)

    
    def parse_full_credits(self, response):
        '''
        Function that parse the 'Cast and Crews' page and extracts the href suffix of each actor. 
        Adds href suffix of each actor onto main IMDB url 
        and yields full url for each individual actor and calls parse_actor_page afterwards
        '''

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
        '''
        Function that parses an individual actor's page. Extracts the name of the actor and 
        then all of the names of each movie/tv show that they worked on. 
        Yields a dictionary per movie/tv show with 2 key-value pairs of 
        {"actor": actor name, "movie_or_TV_name": movie_or_TV_name}
        '''

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

