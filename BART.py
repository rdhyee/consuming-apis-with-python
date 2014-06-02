# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Transit APIs in general
# 
# Larger context of transit APIs: [45 Transit APIs: Yahoo Traffic, SMSMyBus and BART | ProgrammableWeb](http://www.programmableweb.com/news/45-transit-apis-yahoo-traffic-smsmybus-and-bart/2012/02/14).  How about NYC?
# 
# [BART - API Documentation, Station](http://api.bart.gov/docs/stn/)
# 
# get info about stations

# <codecell>

%run talktools

# <markdowncell>

# # BART
# 
# Let's look at the documentation for the BART API:
# 
# * [The Real BART API | bart.gov](http://www.bart.gov/schedules/developers/api)
# 
# * [BART - API Documentation](http://api.bart.gov/docs/overview/index.aspx)
# 
# 
# Definitely good to familiarize yourself with the [BART website](bart.gov)

# <markdowncell>

# # BART developer's group and interesting data
# 
# Also a good idea to use the developer's group: https://groups.google.com/forum/#!forum/bart-developers
# 
# fun to look at [Ridership Reports | bart.gov](http://www.bart.gov/about/reports/ridership) too.

# <markdowncell>

# # BART Map
#     
# ![BART map](http://www.bart.gov/sites/all/themes/bart_desktop/img/global/system-map.gif)

# <markdowncell>

# # Optional API key signup
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

# <codecell>

# setting up the API Key

import requests
import urllib
from lxml.etree import fromstring


try:
    # to allow import of a registered key if it exists
    from settings import BART_API_KEY
except:
    BART_API_KEY = "MW9S-E7SL-26DU-VV8V"

# <markdowncell>

# # Stations
# 
# Let's look up data about the BART stations.
# 
# * [BART - API Documentation, Station](http://api.bart.gov/docs/stn/stns.aspx)
# 
# * See also [Geospatial Data | bart.gov](http://www.bart.gov/schedules/developers/geo) and [daguar/bart-geo](https://github.com/daguar/bart-geo)

# <codecell>

# [BART - API Documentation, Station](http://api.bart.gov/docs/stn/stns.aspx)

def stations(key=BART_API_KEY):
    url = "http://api.bart.gov/api/stn.aspx?" +  \
            urllib.urlencode({'key':key,
                              'cmd':'stns'})
    r = requests.get(url)
    return r

# grab the content of the XML document returned by the API
r = stations().content
print r

# <codecell>

# how many stations?
# parse the XML document to look for number of nodes with stations/station

from lxml import etree

stations = etree.fromstring(r).xpath("stations/station")
len(stations)

# <codecell>

# let's make a DataFrame (table) out of the stations data

from pandas import DataFrame
from collections import OrderedDict

def station_to_ordereddict(station):
    return OrderedDict([(child.tag, child.text) for child in station.iterchildren()])

stations_df = DataFrame([station_to_ordereddict(station) for station in stations])
stations_df

# <markdowncell>

# # Plotting stations on a Map
# 
# Let's use the latitude, longitude information to construct a map of the stations.

# <codecell>

for s in stations_df.T.to_dict().values():
    print s['name'], float(s['gtfs_latitude']), float(s['gtfs_longitude'])

# <codecell>

# plot the maps using folium 
# possible alternative: leaflet.js widget that Brian Granger working on 
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

# <markdowncell>

# # Simple real time info:  number of active trains
# 
# * [BART - API Documentation, Advisory](http://api.bart.gov/docs/bsa/count.aspx)
# 
# * http://api.bart.gov/api/bsa.aspx?cmd=count&key=MW9S-E7SL-26DU-VV8V

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

# <markdowncell>

# # Real time estimated departure times
# 
# One of the most useful parts of the BART API is real-time departure information:
# 
# * http://www.bart.gov/schedules/eta --> the interface on bart.gov
# * [BART - API Documentation, Real-Time](http://api.bart.gov/docs/etd/etd.aspx)
# * http://api.bart.gov/api/etd.aspx?cmd=etd&orig=PLZA&key=MW9S-E7SL-26DU-VV8V -> El Cerrito Plaza
# 
# 
# 
# 

# <codecell>

from dateutil.parser import parse
from dateutil.tz import tzlocal
from lxml.etree import fromstring

def etd(orig, key=BART_API_KEY):
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

# we can get ETA for all stations

from pandas import DataFrame
import pandas as pd
import numpy as np

df = DataFrame(etd('all'))
df

# <codecell>

# look up information for El Cerrito Plaza

df[df.station == 'PLZA']

# <markdowncell>

# # Use someone else's BART API library
# 
# * Now that we have some feel for the BART API, we now decide between:
# 
#   * implementing more of the API ourselves in Python
#   * use someone else's library (if such libraries exist.)
# 
# In the case of the BART API, there is: https://pypi.python.org/pypi/bart_api/0.1 ([github](https://github.com/projectdelphai/bart_api)) by Reuben Castelino
# 
# Easiest way to use the library is to use `pip` from PyPi.  Should be able to do:
# 
#     pip install bart_api
#     
# but as of 2014.05.25, the version doesn't work for Python 2.x.  The github version is more up-to-date. You can do installation from github (https://github.com/projectdelphai/bart_api):
# 
#     pip install git+git://github.com/projectdelphai/bart_api.git
# 
# I've made some changes so it might be helpful to use [my fork](https://github.com/rdhyee/bart_api) until my changes get folded back into the main project:
# 
#      pip install git+git://github.com/rdhyee/bart_api.git

# <markdowncell>

# # Source code for bart_api
# 
# https://github.com/projectdelphai/bart_api/blob/master/bart_api/__init__.py
#    
#    or
#     
# https://github.com/rdhyee/bart_api/blob/master/bart_api/__init__.py

# <codecell>

# example:  use the bart_api to calculate the number of active trains

import bart_api 
reload(bart_api)

bart = bart_api.BartApi()
bart.number_of_trains()

# <codecell>

# stations

station_list = bart.get_stations()
station_list

# <codecell>

#routes = bart.routes(sched, date)
# http://api.bart.gov/docs/route/routes.aspx
# http://api.bart.gov/api/route.aspx?cmd=routes&key=MW9S-E7SL-26DU-VV8V

routes = bart.routes(34, '05/27/2014')
routes

# <codecell>

# let's display the routes with the BART color coding
# sorted by BART numbering
# nice feature of the IPython notebook to able to use HTML

from IPython.display import HTML
import jinja2


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

# # Pros and Cons of Writing your own library vs using someone else's
# 
# * a chance to collaborate and improve on what's already there vs doing something different
# * sometime it takes a fair amount of work to understand other people's code.  (of course, sometimes hard to read one's own code!)

# <codecell>

# bart.get_route_schedule seems to be outdated
# https://github.com/projectdelphai/bart_api/blob/5101e0deec452ddca2f76d0d6d97d6725080ae31/bart_api/__init__.py#L147


bart.get_route_schedule('4')

# <codecell>

# http://api.bart.gov/docs/sched/routesched.aspx
# The optional "date" and "sched" parameters should not be used together. 
# If they are, the date will be ignored, and the sched parameter will be used.

# to get route 4 (Richmond->Fremont)
# http://api.bart.gov/api/sched.aspx?cmd=routesched&route=4&key=MW9S-E7SL-26DU-VV8V

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

print doc.find("date").text, "\n"

for train in doc.findall('route/train'):
    print train.attrib['index']
    for stop in train.iterchildren():
        print stop.attrib['station'], stop.attrib['origTime']
    print

# <markdowncell>

# # Comparing schedule and real-time for a specific station
# 
# Where I'd like to go...but will ultimately leave as an exercise to you all...comparing the scheduled arrival times with the
# real time BART info to see how individual trains (and the system as a whole) are doing.
# 
# What we do here:
# 
# * calculate the schedule for PLZA station
# * calculate the current real time info for PLZA station
# * figure out the difference between the real time info for the next train 
# 
# Compare http://www.bart.gov/schedules/eta?stn=PLZA with http://www.bart.gov/schedules/bystationresults?station=PLZA

# <codecell>

%%html
<iframe src="http://www.bart.gov/schedules/eta?stn=PLZA"/ width=800 height=600>

# <codecell>

# Get schedule for PLZA

# using El Cerrito Plaza station as an example (closest station to me)
# http://www.bart.gov/stations/plza
# http://api.bart.gov/api/sched.aspx?cmd=stnsched&orig=plza&key=MW9S-E7SL-26DU-VV8V

schedule_plza_df = DataFrame(bart.get_station_schedule('PLZA'))
schedule_plza_df.head()

# <codecell>

# Get real time info for PLZA, accounting for 'Leaving', 'Arriving' in Minutes fields

# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=PLZA&key=MW9S-E7SL-26DU-VV8V
# compare to http://www.bart.gov/schedules/eta?stn=PLZA

# need to handle the case of 'Leaving' and 'Arriving' given for minutes in the real time estimates

def etd_minutes_to_int(m):
    if m in ['Leaving', 'Arriving']:
        return 0
    else:
        try:
            return int(m)
        except:
            return np.nan
        

etd_plza_df = DataFrame(etd('PLZA'))
etd_plza_df['minutes'] = etd_plza_df.minutes.apply(etd_minutes_to_int)
etd_plza_df

# <codecell>

# compute the absolute time associated with real time estimate

from datetime import timedelta

etd_plza_df['estimate'] = etd_plza_df.apply(lambda s: s['call_dt'] + \
                                            timedelta(minutes=s['minutes']), axis=1)
etd_plza_df[['destination','direction','station','estimate','minutes']]

# <codecell>

# convert scheduled time into an absolute time

from pytz import timezone
pacific_tz = timezone("US/Pacific")

def orig_time_dt(ot):
    """ """
    dt = parse(ot)
    # with rare exception, we should not find any times earlier than 4am -- if so this is the
    # next day
    # exception:  Bay Bridge repair weekend http://www.bart.gov/news/articles/2013/news20130815

    if dt.hour < 4:
        dt = dt + timedelta(days=1)

    # put dt into local timezone
    dt = pacific_tz.localize(dt)
   
    return dt

schedule_plza_df['orig_time'].apply(orig_time_dt)

# <codecell>

# as a first pass, compare only the the next trains for each route

next_plza_trains = etd_plza_df.groupby('destination').apply(lambda s: min(s['estimate']))
next_plza_trains

# <codecell>

# do the comparison

comparisons = []

for (destination, estimate) in next_plza_trains.iterkv():
    scheduled_for_dest = schedule_plza_df[schedule_plza_df.train_head_station==destination]
    time_diff = scheduled_for_dest['orig_time'].apply(orig_time_dt) - estimate
    comparisons.append({'destination':destination,
                        'estimate':estimate,
                        'schedule':schedule_plza_df.iloc[np.argmin(abs(time_diff))]['orig_time'],
                        'diff': np.min(abs(time_diff))})
    
comparisons_df = DataFrame(comparisons)
comparisons_df

# <codecell>

# put it all together

# first pass at an algorithm
# for all ETD, find the minimum difference with a sechedule arrival

import requests
import urllib
from datetime import timedelta

from lxml.etree import fromstring

from dateutil.parser import parse
from dateutil.tz import tzlocal

from pandas import DataFrame
import numpy as np

import bart_api 


try:
    # to allow import of a registered key if it exists
    from settings import BART_API_KEY
except:
    BART_API_KEY = "MW9S-E7SL-26DU-VV8V"

from pytz import timezone
pacific_tz = timezone("US/Pacific")


def etd(orig, key=BART_API_KEY):
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


def etd_minutes_to_int(m):
    if m in ['Leaving', 'Arriving']:
        return 0
    else:
        try:
            return int(m)
        except:
            return np.nan
        

def orig_time_dt(ot):
    """ """
    dt = parse(ot)
    # with rare exception, we should not find any times earlier than 4am -- if so this is the
    # next day
    # exception:  Bay Bridge repair weekend http://www.bart.gov/news/articles/2013/news20130815

    if dt.hour < 4:
        dt = dt + timedelta(days=1)

    # put dt into local timezone
    dt = pacific_tz.localize(dt)
   
    return dt


bart = bart_api.BartApi(BART_API_KEY)

# using El Cerrito Plaza station as an example (closest station to me)
# http://www.bart.gov/stations/plza

# station schedule
# http://api.bart.gov/api/sched.aspx?cmd=stnsched&orig=plza&key=MW9S-E7SL-26DU-VV8V

schedule_plza_df = DataFrame(bart.get_station_schedule('PLZA'))

# http://api.bart.gov/api/etd.aspx?cmd=etd&orig=PLZA&key=MW9S-E7SL-26DU-VV8V
# compare to http://www.bart.gov/schedules/eta?stn=PLZA

etd_plza_df = DataFrame(etd('PLZA'))

# make sure minutes are integer
etd_plza_df['minutes'] = etd_plza_df.minutes.apply(etd_minutes_to_int)

# compute the absolute time of the real time estimates
etd_plza_df['estimate'] = etd_plza_df.apply(lambda s: s['call_dt'] + \
                                            timedelta(minutes=s['minutes']), axis=1)

# for each route, compute the next train coming into PLZA
next_plza_trains = etd_plza_df.groupby('destination').apply(lambda s: min(s['estimate']))

comparisons = []

for (destination, estimate) in next_plza_trains.iterkv():
    scheduled_for_dest = schedule_plza_df[schedule_plza_df.train_head_station==destination]
    time_diff = scheduled_for_dest['orig_time'].apply(orig_time_dt) - estimate
    comparisons.append({'destination':destination,
                        'estimate':estimate,
                        'schedule':schedule_plza_df.iloc[np.argmin(abs(time_diff))]['orig_time'],
                        'diff': np.min(abs(time_diff))})
    #print destination, estimate, schedule_plza_df.iloc[np.argmin(abs(time_diff))]['orig_time'], np.min(abs(time_diff))
    
comparisons_df = DataFrame(comparisons)
comparisons_df

# <markdowncell>

# # Some Next Steps
# 
# * Generalize to all stations
# * Accumulate data over a period of time to study BART performance.
# * Compare delays we see with the alerts that come from BART itself.

# <markdowncell>

# # Questions (I'm keeping tabs on)
# 
# * As of 2014.05.26, http://api.bart.gov/api/sched.aspx?cmd=scheds&key=MW9S-E7SL-26DU-VV8V shows two schedules in effect: 33 and 34 -- when does schedule 33 get used?  Is number 33 archival?  How about older schedules -- are they still available from the API?
# 
# * come back to [Assessing accuracy of real-time arrival estimate systems](https://groups.google.com/forum/#!topic/transit-developers/JJ1REEpknv4)

# <codecell>


