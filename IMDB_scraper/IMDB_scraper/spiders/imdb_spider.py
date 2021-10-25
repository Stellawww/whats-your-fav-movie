# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt3281548/']

    def parse(self, response):

        """
        This parser method assumes that you are on your favorite movie page.
        It then navigates you to the Cast & Crew page. Once you are there,
        parse_full_credits() method is called. 
        Note that this method returns no data.
        """

        # specify the Caste&Crew's url and request to go to that page

        caste_crew_url = 'https://www.imdb.com/title/tt3281548/fullcredits/'
        yield scrapy.Request(caste_crew_url, callback = self.parse_full_credits)


    def parse_full_credits(self, response):

        """
        This parser method assumes that you are on the Cast & Crew page. 
        It then parse links data of each actor listed on the page and yield a
        request to go to each actor's page. When the actor's page is reached,
        parse_actor_page() method is called.
        Note that this method returns no data.
        """

        # create a list of relative paths corresponding to each actor
        suffix_links = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # iterate through the suffix_links and request to go to each actor's page
        # and call the next parser method
        for suffix in suffix_links:
            actor_links = "https://www.imdb.com" + suffix
            yield scrapy.Request(actor_links, callback = self.parse_actor_page)


    def parse_actor_page(self, response):

        """
        This parser method assumes that you are on an actor's page. 
        It then parse the actor's name and movies or TV shows that the actor participated in.
        It yields a dictionary that contains actors' names and corresponding movies.
        """

        # get the actor's name once we are on the actor's page
        actor_name = response.css("span.itemprop::text").get()

        # iterate through the boxes that contains movie or TV titles
        # and get the list of their titles 
        for movie_or_TV_boxes in response.css("div.filmo-row"):

            movie_or_TV_name = [movie_or_TV_boxes.css("a:first-child::text").get()]

            # return the dictionary pairing actor names and movies they worked 
            yield{
            "actor" : actor_name, 
            "movie_or_TV_name" : movie_or_TV_name
            }
    


