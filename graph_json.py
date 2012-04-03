#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vector_dict.VectorDict import VectorDict,convert_tree
from vector_dict.SparseMatrix import SparseMatrix

from os import path, environ
from json import load
from datetime import datetime as dt 
from matplotlib import dates
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
print options._package
if options._package:
    all_filter = lambda sequence : filter( lambda x : x["name"] in options._package, my_filter(sequence)) 


_key = options.key  or _key
print options._from
save=path.join(environ["HOME"], ".pipy.stat.json" )
result = load(open(save))
res = reduce( VectorDict.__add__,
    map(
        lambda x : convert_tree(
            { 
                x["name"] : dict(
                    date =[ dates.date2num(dt.strptime(x['date'],"%Y-%m-%d")) ] 
                )
            }) + convert_tree(   
                {  x['name'] : 
                    dict(
                dict( ( key, [  x[key] ] ) for key in _key) 
                )
            }),
            all_filter(
            result
        )
    )
)

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

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d') )
    ax.xaxis.set_minor_locator(days)
    ax.fmt_xdata = DateFormatter('%Y-%m-%d')
    ax.autoscale_view()

    ax.set_title( "%s for package %s" % ("total_dl", name) )
    fig.autofmt_xdate()
plt.show()

