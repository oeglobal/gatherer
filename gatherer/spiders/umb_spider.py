# -*- coding: utf-8 -*-
from gatherer.spiders import EduCommonsSpider

class UmbSpider(EduCommonsSpider):
    name = "umb"
    external_id = '693'
    allowed_domains = ["ocw.umb.edu"]
    start_urls = [
        "http://ocw.umb.edu/eduCommons/courselist",
    ]
    course_description_phrases = [
        'Course Description'
    ]