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
_action = ( 'show', 'save' )
parser.add_option("-k", dest="key", 
    help='keys to plot in stored stats', 
    action = 'append' ,
    
    )

parser.add_option("-f",'--from', dest="_from", 
    help='min date', default = ''
    )

parser.add_option("-t",'--to', dest="_to", 
    help='to',default = dt.now().date().isoformat()
    )

parser.add_option("-a",'--do', dest="_action", 
    help="""action to do in save & show 
    *show* orders a matplotlib show, *save* saves the graph in YYYYY-MM-DD-pakkage1,package2-stat.png" in the 
    current dir
    """,
    action='append'
    )
parser.add_option("-p",'--package', dest="_package", 
    help='packages for wich to graph',
    action='append'
    )

(options, args) = parser.parse_args()
my_filter = lambda sequence : filter(lambda r :  options._to >= r['date'] > options._from ,sequence )
all_filter = my_filter
if options._package:
    all_filter = lambda sequence : filter( lambda x : x["name"] in options._package, my_filter(sequence)) 

_action = options._action  or _action 
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

options._package = res.keys()
#http://blog.chilly.ca/?p=115
               
#trick = vd

#trick.__add__=trick.intersection
import matplotlib.pyplot as plt
fig = plt.figure()



### make an autoadpative marker for tick and min/max/interm formaters according
### to date range

total_plot = len(res)

for cursor, (name, data) in enumerate(res.iteritems()):
    ax = fig.add_subplot(  total_plot, 1, cursor+1)


    _plot = []
    for key in _key:
        _plot += [ ax.plot_date( data["date"], data[key],  'o-' , label = key) ]
    
    ax.legend(  loc=0,)
    
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
    ax.autoscale_view()


    ax.set_title( "Statistic for package %s" % (name) )
    # Sh*t ticker with formater only on one graph :(
    fig.autofmt_xdate()
    plt.draw()
if 'save'  in _action:
    plt.savefig("-".join( [  
        dt.now().date().isoformat(), 
        ",".join(options._package)  ,
        "stat.png" ]) 
    )
if 'show' in _action:
    plt.show()

