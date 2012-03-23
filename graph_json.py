#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vector_dict.VectorDict import VectorDict,convert_tree

from os import path, environ
from json import load
from datetime import datetime as dt 
from matplotlib import dates

save=path.join(environ["HOME"], ".pipy.stat.json" )
result = load(open(save))
res = reduce( VectorDict.__add__,
    map(
        lambda x : convert_tree( dict(
            dl = [ x['total_dl']],
            date =[ dates.date2num(dt.strptime(x['date'],"%Y-%m-%d")) ] )
        ),
        result
    )
)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

from matplotlib.dates import YearLocator, MonthLocator, DateFormatter,DayLocator
years    = YearLocator()   # every year
months   = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')
days = DayLocator()

ax.plot_date( res["date"], res["dl"],  '-' )

ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d') )
ax.xaxis.set_minor_locator(days)
ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.autoscale_view()
fig.autofmt_xdate()
plt.show()

