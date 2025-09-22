import scrapy


class PlotExplainedSpider(scrapy.Spider):
    name = "plot_explained"

    async def start(self):
        start_year = 2015
        end_year = 2025
        pages = 20
        urls = [f'https://www.plotexplained.com/movie?sort=latest-release&fromYear={start_year}&toYear={end_year}&page={x}' for x in range(1, pages + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        

    def parse(self, response):
        urls = [f'https://www.plotexplained.com{x}' for x in response.css('a[href^="/movie/"]::attr(href)').getall()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.movie_parse)
    
    def movie_parse(self, responce):
        title = responce.css('h1::text').get()
        yield {
            'url': responce.url,
            'title': title
        }
    
