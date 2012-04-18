Gather and Give
===============

This package is composed of 2 scripts that have two distincts missions : one to
fetch stats and store the data in json format, the other to use the previous 
stats to graph the result. 

pypi_get_stat to gather
***********************

Stats are fetched on pypi. It is based on http://www.codekoala.com/blog/2010/pypi-download-stats/

The added value consists in 
 * using an optparse to have an usage;
 * storing data in the form of a json in ~/.pypi.stat.json. 

Each stats are daily based so it is useless to call it more than once a day. 

pypi_graph_stat to give a graph
*******************************

Based on the stored stats, use matplotlib : 
 * either to make a graph in matplotlib (it should pop a TK window with the graph) ;
 * or print a the graph in a mentioned file

It has limited query feature : 
 * date interval can be specified ;
 * package to plot ;
 * keys in the stat to plot


