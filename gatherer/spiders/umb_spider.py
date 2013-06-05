from scrapy.spider import BaseSpider
from scrapy.http import Request

from scrapy.selector import HtmlXPathSelector
from gatherer.items import CourseItem

class UmbSpider(BaseSpider):
    name = "umb"
    external_id = '693'
    allowed_domains = ["ocw.umb.edu"]
    start_urls = [
        "http://ocw.umb.edu/eduCommons/courselist",
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        courses = hxs.select("//p[contains(concat(' ',normalize-space(@class),' '),' course-listing ')]")
        items = []

        for course in courses:
            item = CourseItem()

            # sometimes category is empty
            url = course.select('a/@href').extract()
            if url:
                url = url[0]
                item['title'] = course.select('a/text()').extract()
                item['url'] = url

                request = Request(url=item['url'],
                                callback=self.parse_course)
                request.meta['item'] = item
                yield request

    def parse_course(self, response):
        item = response.request.meta['item']
        item['raw_text'] = ''
        hxs = HtmlXPathSelector(response)
        item['author'] = hxs.select(".//*[@id='aboutInfo']/p[1]/strong/text()").extract()
        item['categories'] = hxs.select(".//*[@id='category']/.//*[@class='link-category']/text()").extract()

        subpage_urls = hxs.select(".//*[@class='portletItem']/a/@href").extract()
        item['subpage_urls'] = subpage_urls
        subpage_urls.remove(item['url'])
        
        request = Request(url=item['subpage_urls'].pop(),
                            callback=self.parse_course_subpage)
        request.meta['item'] = item
        yield request

    def parse_course_subpage(self, response):
        item = response.request.meta['item']
        hxs = HtmlXPathSelector(response)

        if response.url.endswith('syllabus'):
            item['description'] = ''.join(hxs.select(".//*[@id='parent-fieldname-text']/p[1]/text()").extract())
        item['raw_text'] += ''.join(hxs.select(".//*[@id='parent-fieldname-text']//text()").extract())

        if len(item['subpage_urls']):
            new_url = item['subpage_urls'].pop()
            request = Request(url=new_url,
                                callback=self.parse_course_subpage)
            request.meta['item'] = item
            yield request
        else:
            yield item
        