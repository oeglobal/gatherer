# Scrapy settings for gatherer project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'OCWC gatherer'

SPIDER_MODULES = ['gatherer.spiders']
NEWSPIDER_MODULE = 'gatherer.spiders'

ITEM_PIPELINES = [
	'gatherer.pipelines.JsonExportExternalIdPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'OCWC gatherer (+https://github.com/ocwc/gatherer)'

HTTPCACHE_ENABLED = True