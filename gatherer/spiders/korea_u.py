# -*- coding: utf-8 -*-
from gatherer.spiders import EduCommonsSpider

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