# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt3281548/']

    def parse(self, response):

        caste_crew_url = 'https://www.imdb.com/title/tt3281548/fullcredits/'
        yield scrapy.Request(caste_crew_url, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        for suffix in [a.attrib["href"] for a in response.css("td.primary_photo a")]:
            actor_links = "https://www.imdb.com" + suffix
            yield scrapy.Request(actor_links, callback = self.parse_actor_page)

#    actor_links = [a.attrib["href"] for a in response.css("td.primary_photo a")]

#    for link in actor_links:
#        yield scrapy.Request(link, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        actor_name = response.css("span.itemprop::text").get()

        for movie_or_TV_boxes in response.css("div.filmo-row"):
            movie_or_TV_name = [movie_or_TV_boxes.css("a:first-child::text").get()]

            yield{
            "actor" : actor_name, 
            "movie_or_TV_name" : movie_or_TV_name
            }
    
#    #movie_ids = response.css("::attr(id)")
#    movie_boxes = response.css("div.filmo-row")
#    movie_or_TV_name = movie_boxes.css("a:first-child::text")

#    acotr_boxes = response.css("td.name-overview-widget__section")
#    actor_header = acotr_boxes.css("h1.header")
#    actor_name = actor_header.css("span.itemprop")

    # create a empty list for storing actor name and movie title
#    list = []

#    data = {"actor" : actor_name, 
#            "movie_or_TV_name" : movie_or_TV_name}

#    list.append(data)

#    yield list
    



# titles of movies and TV shows
#element.css("::attr(id)")
#element.css("div.filmo-row")
#element.css("a::text")







