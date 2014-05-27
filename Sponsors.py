# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from lxml.html import fromstring
import requests

url = "http://www.apiconsf.com/apiconsponsors"
doc = fromstring(requests.get(url).content)

# <codecell>

doc.cssselect(".sponsor_bio")

# <codecell>

# if we just want name
print "\n".join([e.text for e in doc.cssselect(".bio_name")])

