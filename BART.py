# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# [The Real BART API | bart.gov](http://www.bart.gov/schedules/developers/api)
# 
# [BART - API Documentation](http://api.bart.gov/docs/overview/index.aspx)
# 
# Two options for use of key
# 
# * use the public key: `MW9S-E7SL-26DU-VV8V`
# 
# * get your own key if you [sign up for one](http://api.bart.gov/api/register.aspx).  (read [Developer License Agreement | bart.gov](http://www.bart.gov/schedules/developers/developer-license-agreement))
# 
# Benefits of signing up:
# 
# > If you sign up for your own key you'll still be able to access the API if it turns into a tragedy of the commons. Plus you'll get a backstage pass to check out pre-release functionality that might just break everything you're working on -- or maybe give you a leg up in the marketplace.
# 

# <markdowncell>

# Larger context of transit APIs: [45 Transit APIs: Yahoo Traffic, SMSMyBus and BART | ProgrammableWeb](http://www.programmableweb.com/news/45-transit-apis-yahoo-traffic-smsmybus-and-bart/2012/02/14).  How about NYC?

# <markdowncell>

# [BART - API Documentation, Real-Time](http://api.bart.gov/docs/etd/etd.aspx)
# 
# cmd=etd	Requests current departure information. (Required)
# orig=<station>	Specifies the station. Stations are referenced by their abbreviations. You can also use 'ALL' to get all of the current ETD's. (Required)
# key=<key>	API registration key. (Required)
# plat=<platform>	This will limit results to a specific platform. Valid platforms depend on the station, but can range from 1-4. (Optional)
# dir=<dir>	This will limit results to a specific direction. Valid directions are 'n' for Northbound and 's' for Southbound. (Optional)

# <markdowncell>

# [BART - API Documentation, Station](http://api.bart.gov/docs/stn/)
# 
# get info about stations

# <markdowncell>

# Also a good idea to use the developer's group: https://groups.google.com/forum/#!forum/bart-developers

# <markdowncell>

# fun to look at [Ridership Reports | bart.gov](http://www.bart.gov/about/reports/ridership) too.

# <codecell>

#ETD
# [BART - API Documentation, Real-Time](http://api.bart.gov/docs/etd/etd.aspx)

import requests
import urllib
from lxml.etree import fromstring

import settings

try:
    # to allow import of a registered key if it exists
    from settings import BART_API_KEY
except:
    BART_API_KEY = "MW9S-E7SL-26DU-VV8V"
    

def etd(orig, key=BART_API_KEY):
    url = "http://api.bart.gov/api/etd.aspx?" +  \
            urllib.urlencode({'cmd':'etd',
                              'orig':orig,
                              'key':key})
    print url
                                                                  
    r = requests.get(url)
    return r.content

# <codecell>

# [BART - API Documentation, Station](http://api.bart.gov/docs/stn/stns.aspx)

def stations(key=BART_API_KEY):
    url = "http://api.bart.gov/api/stn.aspx?" +  \
            urllib.urlencode({'key':key,
                              'cmd':'stns'})
    r = requests.get(url)
    return r

r = stations().content

# <codecell>

from lxml import etree
stations = etree.fromstring(r).xpath("stations/station")
len(stations)

# <codecell>

from collections import OrderedDict
OrderedDict([(child.tag, child.text) for child in stations[0].iterchildren()])

# <codecell>

from pandas import DataFrame

def station_to_ordereddict(station):
    return OrderedDict([(child.tag, child.text) for child in station.iterchildren()])

stations_df = DataFrame([station_to_ordereddict(station) for station in stations])
stations_df.head()

# <codecell>

for s in stations_df.T.to_dict().values():
    print s['name'], float(s['gtfs_latitude']), float(s['gtfs_longitude'])

# <codecell>

# plot the maps using folium --- something to do...
# time perhaps to try out leaflet.js widget that Brian working on 
# https://github.com/ellisonbg/leaftletwidget

# http://nbviewer.ipython.org/gist/bburky/7763555/folium-ipython.ipynb

from IPython.display import HTML
import folium

def inline_map(map):
    """
    Embeds the HTML source of the map directly into the IPython notebook.
    
    This method will not work if the map depends on any files (json data). Also this uses
    the HTML5 srcdoc attribute, which may not be supported in all browsers.
    """
    map._build_map()
    return HTML('<iframe srcdoc="{srcdoc}" style="width: 100%; height: 510px; border: none"></iframe>'.format(srcdoc=map.HTML.replace('"', '&quot;')))

def embed_map(map, path="map.html"):
    """
    Embeds a linked iframe to the map into the IPython notebook.
    
    Note: this method will not capture the source of the map into the notebook.
    This method should work for all maps (as long as they use relative urls).
    """
    map.create_map(path=path)
    return HTML('<iframe src="files/{path}" style="width: 100%; height: 510px; border: none"></iframe>'.format(path=path))

# <codecell>

bart_map = folium.Map(location=[37.8717, -122.2728], zoom_start=9)


# for airport in islice(airports,None):
#    lat =  float(airport['Origin_lat'])
#    lon = float(airport['Origin_long'])
#    label = str(airport['Origin_airport'])  # don't know why str necessary here
#    airport_map.simple_marker([lat,lon],popup=label)


for s in stations_df.T.to_dict().values():
    bart_map.simple_marker([float(s['gtfs_latitude']), float(s['gtfs_longitude'])],
                           popup=s['name'])
inline_map(bart_map)

# <codecell>

# how to get list of stations

# <markdowncell>

# From http://stackoverflow.com/a/8525115, I get the idea to use `python-dateutil` instead to handle timezones
# 
#     pip search python-dateutil
#     
# http://labix.org/python-dateutil#head-c0e81a473b647dfa787dc11e8c69557ec2c3ecd2

# <markdowncell>

# # datetime.strptime couldn't yield timezone
# 
# 
# ````Python
# # http://emilics.com/blog/article/python_time.html
# 
# import datetime
# 
# s = '05/18/2014 10:58:18 PM PDT'
# dt = datetime.datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p %Z')
# ````

# <markdowncell>

# # how tzinfo() looks like PDT for me
# 
# ````Python
# tz = dt.tzinfo
# datetime.datetime.now(dt.tzinfo).tzname()
# ````
# 
#     PDT

# <markdowncell>

# Stations
# 
# http://api.bart.gov/docs/stn/stns.aspx

# <codecell>

from dateutil.parser import parse
from lxml.etree import fromstring

def etd2(orig, key=BART_API_KEY):
    url = "http://api.bart.gov/api/etd.aspx?" +  \
            urllib.urlencode({'cmd':'etd',
                              'orig':orig,
                              'key':key})
                                                                  
    r = requests.get(url)
    doc = fromstring(r.content)
    
    estimations_list = []

    # parse the datetime for the API call

    s = doc.find('date').text + " " +doc.find('time').text
    call_dt = parse(s)
    
    # turn the results into a rectangular format

    # parse the station

    for station in doc.findall('station'):
        etds = station.findall('etd')
        for etd in etds:
            estimates = etd.findall('estimate')
            for estimate in estimates:
                estimate_tuple = [(child.tag, child.text) for child in estimate.iterchildren()]
                
                estimate_tuple += [('call_dt', call_dt),
                                   ('station', station.find('abbr').text),
                                   ('destination', etd.find('abbreviation').text)]
               
                estimations_list.append(dict(estimate_tuple))

    return estimations_list

# <codecell>

from pandas import DataFrame
import pandas as pd
import numpy as np

df = DataFrame(etd2('all'))
df

# <codecell>

df[df.station == 'PLZA']

# <markdowncell>

# How to figure out the current number of trains in operation?
# 
#     http://api.bart.gov/docs/bsa/count.aspx

# <codecell>

def train_count(key=BART_API_KEY):
    url = "http://api.bart.gov/api/bsa.aspx?" +  \
        urllib.urlencode({'cmd':'count',
                          'key':key})
                                                                  
    r = requests.get(url)
    doc = fromstring(r.content)
    call_dt = doc.find('date').text + " " +doc.find('time').text
    count = doc.find('traincount').text
    return (call_dt, count)

d = train_count()
d

# <headingcell level=1>

# Use someone's BART API library

# <markdowncell>

# Easiest way to use the library is to use `pip` from PyPi.
# 
# https://pypi.python.org/pypi/bart_api/0.1  by Reuben Castelino
# 
# Should be able to do
# 
#     pip install bart_api
#     
# but as of 2014.05.25, the version doesn't work for Python 2.x.
# 
# Let's do installation from github (https://github.com/projectdelphai/bart_api):
# 
#     pip install git+git://github.com/projectdelphai/bart_api.git
# 
# 
# 
# 
# Problem is that it's written for Python 3.x

# <codecell>

import bart_api 
reload(bart_api)

bart = bart_api.BartApi()
bart.number_of_trains()

# <codecell>

station_list = bart.get_stations()
station_list

# <codecell>

#routes = bart.routes(sched, date)
routes = bart.routes(34, '05/27/2014')
routes

# <codecell>

%%html
<div style="color:#0000FF">
  <h3>This is a heading</h3>
  <p>This is a paragraph.</p>
</div>

# <codecell>

sorted(routes, key=lambda r: int(r.get('number')))

# <codecell>

from IPython.display import HTML
import jinja2

CSS = ""

ROUTE_TEMPLATE = """
<div class="wrap">
<table>
 {% for item in items %}<tr>
 <td style="background-color:{{item.color}}">{{item.name}}</td>
 <td>{{item.number}}</td>
 </tr>
 {% endfor %}
</table>
</div>
"""

template = jinja2.Template(ROUTE_TEMPLATE)

HTML(template.render(items=sorted(routes, key=lambda r: int(r.get('number')))))

# <markdowncell>

# 
#     
# ![BART map](http://www.bart.gov/sites/all/themes/bart_desktop/img/global/system-map.gif)

# <markdowncell>

# I don't think the bart_api is a complete implementation....

# <codecell>

# http://api.bart.gov/docs/sched/routesched.aspx
# The optional "date" and "sched" parameters should not be used together. 
# If they are, the date will be ignored, and the sched parameter will be used.

url = "http://api.bart.gov/api/sched.aspx?cmd=routesched&route=4&key=MW9S-E7SL-26DU-VV8V"

def filter_none(d):
    return dict([(k,v) for (k,v) in d.items() if v is not None])

def route_schedule(route, sched=None, date=None, l=0, key=BART_API_KEY):
    url = "http://api.bart.gov/api/sched.aspx?" +  \
        urllib.urlencode(filter_none({'cmd':'routesched',
                          'route':route,
                          'sched':sched,
                          'date':date,
                          'l':l,
                          'key':key}))
                                                                  
    r = requests.get(url)
    doc = fromstring(r.content)
    return doc

doc = route_schedule(4)
doc

# <codecell>

doc.find("date").text

# <headingcell level=1>

# Fixing Bug in bart_api

# <markdowncell>

# If you do
# 
#     routes = bart.routes()
#     
# you get an error.
# 
# ````bash
# git clone git@github.com:rdhyee/bart_api.git
# cd bart_api
# git remote add upstream https://github.com/projectdelphai/bart_api.git
# ````
# 
# I issued a PR: https://github.com/projectdelphai/bart_api/pull/2

# <headingcell level=1>

# Questions

# <markdowncell>

# * As of 2014.05.26, http://api.bart.gov/api/sched.aspx?cmd=scheds&key=MW9S-E7SL-26DU-VV8V shows two schedules in effect: 33 and 34 -- when does schedule 33 get used?  Is number 33 archival?  How about older schedules -- are they still available from the API?
# 
# * come back to [Assessing accuracy of real-time arrival estimate systems](https://groups.google.com/forum/#!topic/transit-developers/JJ1REEpknv4)

# <headingcell level=1>

# Comparing schedule and real-time for a specific station

# <markdowncell>

# I like http://api.bart.gov/docs/overview/examples.aspx --> helps me to wrap my head around the API

# <codecell>

station = "PLZA"

# station schedule
# http://api.bart.gov/api/sched.aspx?cmd=stnsched&orig=embr&key=MW9S-E7SL-26DU-VV8V

schedule_plza_df = DataFrame(bart.get_station_schedule(station)).tail()
schedule_plza_df

# <codecell>

# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=PLZA&key=MW9S-E7SL-26DU-VV8V
# compare to http://www.bart.gov/schedules/eta?stn=PLZA

etd_plza_df = DataFrame(etd2('PLZA'))
etd_plza_df

# <codecell>

%%html
<iframe src="http://www.bart.gov/schedules/eta?stn=PLZA"/ width=800 height=600>

# <markdowncell>

# How to match the real time estimate with the schedule?
# 
# Let's focus just on the next arrival.
# 
# Might need 
# Possible that a train is late
# 
# In order to compare to schedule for a given station, need to know what route we're considering.

# <codecell>

from IPython.core.debugger import Pdb
pdb = Pdb()
pdb.runcall(bart.get_station_schedule, 'PLZA')

# <codecell>

stations_df.abbr

