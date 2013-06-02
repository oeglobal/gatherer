# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class GathererItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class CourseItem(Item):
	url = Field()
	title = Field()
	author = Field()
	description = Field()
	raw_text = Field()
	subpage_urls = Field()
	
