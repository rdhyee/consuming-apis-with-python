# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# installation
# 
# conda
# 
# Conceptual overview
# 
# Requests library: [Requests: HTTP for Humans — Requests 2.3.0 documentation](http://docs.python-requests.org/en/latest/)

# <markdowncell>

# # What APIs to cover?
# 
# * geocoder.us -- simple to understand and use?

# <headingcell level=1>

# Geocoder.us

# <markdowncell>

# http://geocoder.us/
# 
# * free for non-commercial use
# 
# http://rpc.geocoder.us/service/csv?address=1600+Pennsylvania+Ave,+Washington+DC

# <codecell>

url = "http://rpc.geocoder.us/service/csv?address=1600+Pennsylvania+Ave,+Washington+DC"

# <codecell>

import requests
r = requests.get(url).content
r.split(",")

