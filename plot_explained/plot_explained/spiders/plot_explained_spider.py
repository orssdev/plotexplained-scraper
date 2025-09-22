import scrapy


class PlotExplainedSpider(scrapy.Spider):
    name = "plot_explained"

    async def start(self):
        start_year = 2015
        end_year = 2025
        pages = 5
        urls = [f'https://www.plotexplained.com/movie?sort=latest-release&fromYear={start_year}&toYear={end_year}&page={x}' for x in range(1, pages + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        

    def parse(self, response):
        urls = [f'https://www.plotexplained.com{x}' for x in response.css('a[href^="/movie/"]::attr(href)').getall()]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.movie_parse)
    
    def movie_parse(self, response):
        title = response.css('h1::text').get()
        info = response.css('div.flex.pt-4.flex-row.font-semibold.text-base.sm\\:text-lg.xl\\:text-xl.font-source-pro.gap-x-8.md\\:gap-x-14.gap-y-2.sm\\:gap-y-3.md\\:gap-y-4.flex-wrap p::text').getall()
        yield {
            'url': response.url,
            'title': title,
            'info': info
        }
    
