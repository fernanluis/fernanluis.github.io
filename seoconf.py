import os
import sys
sys.path.append(os.curdir)
from publishconf import *

PLUGINS = PLUGINS + ["pelican.plugins.seo"]

SEO_ARTICLES_LIMIT = 10
SEO_PAGES_LIMIT = 10
