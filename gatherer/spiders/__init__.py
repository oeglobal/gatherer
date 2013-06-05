# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import Request

from scrapy.selector import HtmlXPathSelector
from gatherer.items import CourseItem

class EduCommonsSpider(BaseSpider):
    external_id = None
    exclude_urls= []
    course_description_phrases = ['Course Description']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        courses = hxs.select("//p[contains(concat(' ',normalize-space(@class),' '),' course-listing ')]")
        items = []

        print self.exclude_urls

        for course in courses:
            # sometimes category is empty
            url_list = course.select('a/@href').extract()
            if url_list:
                url = url_list[0]
                if url not in self.exclude_urls:
                    item = CourseItem()

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
        # remove "home" links that point to main page of the course that we just parsed
        if item['url'] in subpage_urls:
            subpage_urls.remove(item['url'])
        
        request = Request(url=item['subpage_urls'].pop(),
                            callback=self.parse_course_subpage)
        request.meta['item'] = item
        yield request

    def parse_course_subpage(self, response):
        item = response.request.meta['item']
        hxs = HtmlXPathSelector(response)

        if response.url.endswith('syllabus'):
            found_description = False
            for course_description_phrase in self.course_description_phrases:
                if not found_description and hxs.select("//text()[contains(.,'%s')]" % course_description_phrase):
                    item['description'] = ''.join(hxs.select("//text()[contains(.,'%s')]/following::p[1]/text()" % course_description_phrase).extract())
                    found_description = True

            if not found_description:
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