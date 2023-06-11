# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class MalItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def serialize_price(value):
    return f'£ {str(value)}'

class AnimeItem(scrapy.Item):
    url = scrapy.Field()
    title_jap = scrapy.Field()
    title_eng = scrapy.Field()
    score = scrapy.Field()
    rank = scrapy.Field()
    popularity = scrapy.Field()
    watched_by = scrapy.Field()
    show_type = scrapy.Field()
    studio = scrapy.Field()
    release_year = scrapy.Field()
    release_season = scrapy.Field()
    num_episodes = scrapy.Field()
    description = scrapy.Field()
    tags = scrapy.Field()