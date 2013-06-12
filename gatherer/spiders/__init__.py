# -*- coding: utf-8 -*-
from urlparse import urljoin

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector

from gatherer.items import CourseItem

class EduCommonsSpider(BaseSpider):
    external_id = None
    exclude_urls= []
    handle_httpstatus_list = [500]
    course_description_phrases = ['Course Description']

    xpath_parse_courses_selector = "//p[contains(concat(' ',normalize-space(@class),' '),' course-listing ')]"
    xpath_parse_course_url_list = "a/@href"
    xpath_parse_course_author = ".//*[@id='aboutInfo']/p[1]/strong/text()"
    xpath_parse_course_subpage_description = "//text()[contains(.,'%s')]/following::p[1]/text()"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        courses = hxs.select(self.xpath_parse_courses_selector)
        items = []

        for course in courses:
            # sometimes category is empty
            url_list = course.select(self.xpath_parse_course_url_list).extract()
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
        item['author'] = hxs.select(self.xpath_parse_course_author).extract()
        item['categories'] = hxs.select(".//*[@id='category']/.//*[@class='link-category']/text()").extract()
        image_src = hxs.select(".//*[@id='aboutPhoto']/.//img/@src").extract()
        if image_src:
            if not image_src[0].startswith('http'):
                image_src = urljoin(item['url'], image_src[0])
        item['image_src'] = image_src

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
                    item['description'] = ''.join(hxs.select(self.xpath_parse_course_subpage_description % course_description_phrase).extract())
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
            rss_url = "%s/rss_recent" % item['url']
            request = Request(url=rss_url,
                                callback=self.parse_rss)
            request.meta['item'] = item
            yield request

    def parse_rss(self, response):
        item = response.request.meta['item']

        if response.status != 500:
            xxs = XmlXPathSelector(response)
            xxs.remove_namespaces()

            item['date'] = xxs.select('.//channel/date/text()').extract()
            description = xxs.select('.//channel/description/text()').extract()
            if (len(item.get('description', '')) < 10) and description:
                item['description'] = ''.join(description).strip()

        del(item['subpage_urls'])

        return item


