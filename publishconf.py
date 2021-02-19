#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://fernanluis.github.io'
RELATIVE_URLS = False

GOOGLE_ANALYTICS = "G-VXYBJFPECC"
DISQUS_SITENAME = "https-fernanluis-github-io"

FEED_DOMAIN = 'http://feeds.feedburner.com' # servicio utilizado para enviar los correos
FEED_ALL_ATOM = 'luisdev' # alias
FEED_ATOM = 'feeds/all.atom.xml' # esto es sencillamente dónde estará alojado el XML

RECORD_SESSION = True

# FEED_ALL_ATOM = 'feeds/all.atom.xml'
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
