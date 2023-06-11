import scrapy
from malscraper.items import AnimeItem
import random

class MalSpider(scrapy.Spider):
    name = "malspider"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/topanime.php"]

    def parse(self, response):
        animes = response.css('tr.ranking-list')
        
        for anime in animes:
            anime_url = anime.css('h3 a').attrib['href']
            yield response.follow(anime_url, callback= self.parse_anime_page)
            
        next_page = response.css('a.link-blue-box.next').attrib['href']
        
        if next_page is not None:
            next_page_url = 'https://myanimelist.net/topanime.php' + next_page
        yield response.follow(next_page_url, callback= self.parse)
        pass

    def parse_anime_page(self, response):
        anime_item = AnimeItem()
        anime_item['url'] = response.url,
        anime_item['title_jap'] = response.xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div/div[1]/div/h1/strong/text()').get(),
        anime_item['title_eng'] = response.xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div/div[1]/div/p/text()').get()
        anime_item['score'] = response.css('.score-label::text').get()
        anime_item['rank'] = response.css('span.numbers.ranked strong::text').get(),
        anime_item['popularity'] = response.css('.numbers.popularity strong::text').get(),
        anime_item['watched_by'] = response.css('.numbers.members strong::text').get(),
        anime_item['show_type'] = response.css('.information.type a::text').get(),
        anime_item['studio'] = response.css('.information.studio.author a::text').get(),
        anime_item['release_year'] = response.css('.information.season a::text').get(),
        anime_item['num_episodes'] = response.xpath('//*[@id="curEps"]/text()').get(),
        anime_item['description'] = response.xpath('//*[@itemprop="description"]/text()').get(),
        anime_item['tags'] = response.xpath('//*[@itemprop="genre"]/text()').getall(),
            
        yield anime_item
        