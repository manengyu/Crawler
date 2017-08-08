# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from scrapy import cmdline

cmdline.execute("scrapy crawl ".split())
cmdline.execute("scrapy crawl ".split())
cmdline.execute("scrapy crawl  -o items.json".split())
