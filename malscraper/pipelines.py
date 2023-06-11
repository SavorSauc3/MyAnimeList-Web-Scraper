# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class MalscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        """
        #Strip whitespace
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()
        """
        """
        #switch category and product type to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
        """
            
        #string number convert to float
        float_keys = ['score']
        for float_key in float_keys:
            value = adapter.get(float_key)
            adapter[float_key] = float(value)
            
        #take items out of a tuple
        tuple_extract_keys = ['title_jap', 'url', 'watched_by', 'description', 'tags', 'studio', 'show_type', 'release_year', 'rank', 'popularity', 'num_episodes']
        for extract_key in tuple_extract_keys:
            value = adapter.get(extract_key)
            if value is not None:
                adapter[extract_key] = value[0]
            else:
                adapter[extract_key] = value
        
        #extract numbers between parenthesis from strings
        clean_num_keys = ['watched_by', 'num_episodes', 'popularity', 'rank']
        for num_key in clean_num_keys:
            value = adapter.get(num_key)
            value_string = re.findall("[0-9]",value)
            if value is not None:
                value_string = int(''.join(value_string))
                adapter[num_key] = value_string
            else:
                adapter[num_key] = value
        """
        ##Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)
        """
        #release_year, release_season --> convert text to number, split season from rest of item
        release_string = adapter.get('release_year')
        if release_string is not None:
            release_string_list = release_string.split(' ')
            adapter['release_season'] = release_string_list[0]
            adapter['release_year'] = int(release_string_list[1])
        else:
            adapter['release_season'] = None
            adapter['release_year'] = None
            
        return item