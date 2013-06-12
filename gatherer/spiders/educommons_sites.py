# -*- coding: utf-8 -*-
from gatherer.spiders import EduCommonsSpider

from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from gatherer.items import CourseItem

class KoreaUSpider(EduCommonsSpider):
    name = "korea_u"
    external_id = '113'
    allowed_domains = ["ocw.korea.edu"]
    start_urls = [
        "http://ocw.korea.edu/ocw/courselist",
    ]
    exclude_urls = [
        "http://ocw.korea.edu/ocw/center-for-teaching-and-learning",
        "http://ocw.korea.edu/ocw/center-for-teaching-and-learning/the-1st-asia-regional-ocw-conference-2009",
        "http://ocw.korea.edu/ocw/center-for-teaching-and-learning/teaching-and-learning-learning-portfolio",
        "http://ocw.korea.edu/ocw/center-for-teaching-and-learning/workshop",
        "http://ocw.korea.edu/ocw/center-for-teaching-and-learning/ae30cd08-d559bb38-bd84c57c-1"
    ]
    course_description_phrases = [
        'Course Description',
        'Description of course'
    ]

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

class UmbSpider(EduCommonsSpider):
    name = "umb"
    external_id = "693"
    allowed_domains = ["ocw.umb.edu"]
    start_urls = [
        "http://ocw.umb.edu/eduCommons/courselist",
    ]
    course_description_phrases = [
        "Course Description"
    ]
