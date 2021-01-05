# -*- coding: utf-8 -*-
# @Date    : 2020-12-09 08:55:28
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

import os
from scrapy import cmdline

#cmdline.execute("scrapy crawl jing_dong  -s JOBDIR=job_info/001".split())
#cmdline.execute("scrapy crawl jing_dong ".split())
cmdline.execute("scrapy crawl computer ".split())
