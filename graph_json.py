#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vector_dict.VectorDict import VectorDict as vd,convert_tree
from vector_dict.SparseMatrix import SparseMatrix

from os import path, environ
from json import load
from datetime import datetime as dt 
from matplotlib import dates
#from matplotlib.ticker import AutoDateFormater
from optparse import OptionParser
parser = OptionParser()
_key = ['total_dl' ]
parser.add_option("-k", dest="key", 
    help='keys to plot in stored stats', 
    action = 'append' ,
    
    )

parser.add_option("-f",'--from', dest="_from", 
    help='min date', default = ''
    )

parser.add_option("-t",'--to', dest="_to", 
    help='to',default = dt.now().strftime("%Y-%m-%d") 
    )

parser.add_option("-p",'--package', dest="_package", 
    help='packages for wich to grpah',
    action='append'
    )

(options, args) = parser.parse_args()
my_filter = lambda sequence : filter(lambda r :  options._to >= r['date'] > options._from ,sequence )
all_filter = my_filter
if options._package:
    all_filter = lambda sequence : filter( lambda x : x["name"] in options._package, my_filter(sequence)) 


_key = options.key  or _key
save=path.join(environ["HOME"], ".pipy.stat.json" )
result = load(open(save))
#import types
#set.__add__ = types.MethodType(set.union, set, set)
res = reduce( vd.__add__,
    map(
        lambda x : convert_tree(
            { 
                x["name"] : dict(
                    date =[ dates.date2num(dt.strptime(x['date'],"%Y-%m-%d")) ],
                )
            }) + convert_tree(
                {  x['name'] : 
                    dict( ( key, [  x[key] ] ) for key in _key) 
                
            }) + convert_tree( {
                x["name"] : { 
                    'release' :  { x["last_release"] : 
                    [ x['last_upload'] ] } 
                    }} 
            ),
            all_filter(
                result
            )
    )
)

#http://blog.chilly.ca/?p=115
               
#trick = vd

#trick.__add__=trick.intersection
import matplotlib.pyplot as plt
fig = plt.figure()



from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,DayLocator
### make an autoadpative marker for tick and min/max/interm formaters according
### to date range

years    = YearLocator()   # every year
months   = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')
days = DayLocator()
total_plot = len(res)

for cursor, (name, data) in enumerate(res.iteritems()):
    ax = fig.add_subplot(  total_plot, 1, cursor+1)


    _plot = []
    for key in _key:
        _plot += [ ax.plot_date( data["date"], data[key],  'o-' , label = key) ]
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    for label, date in data["release"].iteritems():
        ax.annotate( "release\n" + label,xy = (
        dates.date2num(dt.strptime(date[0][0:10],"%Y-%m-%d"  )),
        ax.get_ybound()[0] + 10
        
        ),
        horizontalalignment='center', verticalalignment='center',
        xytext = (
             dates.date2num(dt.strptime(date[0][0:10],"%Y-%m-%d"  )),
             sum(ax.get_ybound()) /2
    ),
            arrowprops=dict(facecolor='black')
        ) 

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.autoscale_view()


    ax.set_title( "%s for package %s" % ("total_dl", name) )
    # Sh*t ticker with formater only on one graph :(
    fig.autofmt_xdate()
    plt.draw()
plt.show()

