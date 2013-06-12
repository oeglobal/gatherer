# -*- coding: utf-8 -*-
from gatherer.spiders import EduCommonsSpider

from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from gatherer.items import CourseItem

class NotreDameSpider(EduCommonsSpider):
    name = "nd"
    external_id = "155"
    allowed_domains = ["ocw.nd.edu"]
    start_urls = [
        "http://ocw.nd.edu/courselist"
    ]
    course_description_phrases = [
        "Course Description"
    ]    

    xpath_parse_courses_selector = "//*[contains(concat(' ',normalize-space(@class),' '),' course-listing ')]"
    xpath_parse_course_url_list = "td[1]/a/@href"
    xpath_parse_course_author = ".//*[@id='aboutInfo']/p[1]/*/text()"
    xpath_parse_course_subpage_description = "//text()[contains(.,'%s')]/following::p[1]/span/text()"