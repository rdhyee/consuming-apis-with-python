# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Outline
# 
# Let's learn about consuming APIs with Python by looking at some of the simplest APIs around:  those for *geocoding*.  The process of geocoding is that of turning the names/labels of geographic entities (typically street addresses, but also things like cities, points of interest) into geographical coordinates -- typically latitude and longitude.
# 
# Let's start with [geocoder.us](#Geocoder.us)

# <headingcell level=1>

# geocoder.us

# <markdowncell>

# Go to http://geocoder.us/ and find out what the site is about:
# 
# > find the latitude & longitude of any US address - for free
# 
# <img src="https://www.evernote.com/shard/s1/sh/9a77110c-d3ec-48c8-b41a-074da933df64/3f1919509f1db26f87d7a1857c09fae6/res/d1a0177d-6644-4624-94d2-865e243c6e9f/geocoder.us__a_free_US_address_geocoder-20140611-154936.jpg.jpg?resizeSmall&width=832"/>
# 
# Reasons why it's a good service to learn from:
# 
# * free for non-commercial use
# * there is a user interface to the service you can use to get a feel for what the service is about -- and whose results with which you'll be able to compare data from the API.
# 
# To figure out how to use geocoder.us, click on the documentation: http://geocoder.us/help/.  There are various interfaces to the service including:
# 
# * XML-RPC
# * SOAP
# * REST-RDF
# * REST-CSV
# 
# We will focus here on using the REST-CSV and REST-RDF protocols.
# 
# Look at the following URL in a web browser for comparison:
# 
# http://rpc.geocoder.us/service/csv?address=1600+Pennsylvania+Ave,+Washington+DC
# 
# See my writeup in *Pro Web 2.0 Mashups* on  [Geocoding](http://mashupguide.net/1.0/html/ch13s06.xhtml#d0e21349) for more info.

# <markdowncell>

# The Geocoder.us API, which is documented here:
# 
# http://geocoder.us/help/
# 
# Let’s calculate the latitude and longitude for the White House (_1600 Pennsylvania Avenue, Washington, DC_) with different aspects of the Geocoder.us service:
# 
# The Geocoder.us user interface, invoked with this:
# 
# http://geocoder.us/demo.cgi?address=1600+Pennsylvania+Ave%2C+Washington+DC
# 
# shows that the latitude and longitude of the address is the following:
# 
# `(38.898748, -77.037684)`
# 
# <img src="https://www.evernote.com/shard/s1/sh/2c545912-dca3-46a0-8850-6dc0ac874088/d30820345e728018a04b16f99d7ccedf/res/f3ae7e3f-798c-4f0a-8f66-f25eee90faa0/geocoder.us__a_free_US_geocoder-20140611-161019.jpg.jpg" />

# <headingcell level=2>

# REST-CSV

# <markdowncell>

# The CSV interface, invoked with this:
# 
# http://rpc.geocoder.us/service/csv?address=2855+Telegraph+Ave.%2C+Berkeley%2C+CA
# 
# returns the following:
# 
# `37.858276,-122.260070,2855 Telegraph Ave,Berkeley,CA,94705`

# <markdowncell>

# url = "http://rpc.geocoder.us/service/csv?address=1600+Pennsylvania+Ave,+Washington+DC"

# <codecell>

# let's break out the address explicitly

import urllib

url = "http://rpc.geocoder.us/service/csv?" + \
        urllib.urlencode({
           'address':'1600 Pennsylvania Ave, Washington DC'
})
    
url

# <codecell>

import requests

url = "http://rpc.geocoder.us/service/csv?address=1600+Pennsylvania+Ave,+Washington+DC"
r = requests.get(url).content
r.split(",")

# <markdowncell>

# Sage cell version: http://bit.ly/SNZs0L
# 
# how to embed: https://sagecell.sagemath.org/static/about.html?v=15adefe8b7e89fcf49eda7af5303abd4

# <markdowncell>

# ##REST-RDF
# 
# The REST interface, through this:
# 
# http://geocoder.us/service/rest/?address=1600+Pennsylvania+Ave,+Washington+DC
# 
# returns the following:
# 
# 
#     <rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
#         <geo:Point rdf:nodeID="aid54380535">
#             <dc:description>1600 Pennsylvania Ave NW, Washington DC 20502</dc:description>
#             <geo:long>-77.037684</geo:long>
#             <geo:lat>38.898748</geo:lat>
#         </geo:Point>
#     </rdf:RDF>
#                

# <codecell>

import requests

# http://geocoder.us/service/rest/?address=1600+Pennsylvania+Ave,+Washington+DC
    
url = "http://geocoder.us/service/rest/?address=1600+Pennsylvania+Ave,+Washington+DC"
r = requests.get(url).text
print r

# <markdowncell>

# We can use the excellent [lxml](http://lxml.de/) library to parse the latitude and longitude.

# <codecell>

from lxml.etree import fromstring

NS = {'geo':'http://www.w3.org/2003/01/geo/wgs84_pos#'}
doc = fromstring(r)

(float(doc.find(".//{%s}lat" % (NS['geo'])).text), 
 float(doc.find(".//{%s}long" % (NS['geo'])).text))

# <markdowncell>

# Alternatively, let's look for a standard library approach -- for this example, we don't need to install `lxml` but rather just use the standard `xml.etree` library.
# 
# https://docs.python.org/2/library/xml.etree.elementtree.html

# <codecell>

import xml.etree.ElementTree as ET
tree = ET.fromstring(r)
tree

# <codecell>

(float(tree.find(".//{%s}lat" % (NS['geo'])).text), 
 float(tree.find(".//{%s}long" % (NS['geo'])).text))

