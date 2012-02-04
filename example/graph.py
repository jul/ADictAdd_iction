# t!/usr/bin/python
# -*- coding: utf-8 -*-
#WTFPL
"""Trying lame cosinus on text
to create the mysoginie and troll input text file
you need *nix 
fortunes / fortunes-fr
and then 
fortune mysoginie -m '' | egrep -v -r "^%" | egrep -v  '\-\+\-' > myso-fr.txt 
fortune tribune-linuxfr  -m '' | egrep -v -r "^%" | egrep -v  '\-\+\-' >  troll.txt

chienne is the text of a feminist site http://www.chiennesdegarde.com/

blague miso is  a random mysoginistic joke on internet. 

The higher a cos is the more two things are similar. 

I used pydot to make a svg map of the path / frequency, just for fun

"""


import os, sys, inspect
cmd_folder = os.path.abspath(
    os.path.join(
        os.path.split(
            inspect.getfile( inspect.currentframe() )
        )[0] ,
        ".."
    )
)
if cmd_folder not in sys.path:
   sys.path.insert(0, cmd_folder)




import re
from vector_dict.VectorDict import VectorDict, tree_from_path, flattening
import pydot as pd
from codecs import open as open

def dot_graph( dict_graph, out_name, gopts = dict( fontsize = 20.0, size = "100.0,100.0", dpi= 1000.0 )):
    graph = pd.Dot(graph_type='digraph', **gopts )
    node = set()
    edge = []
    label = [] 
    for pair in dict_graph.as_row_iter(flatten=False):
        path = [ "ROOT" ] +  list(pair[0]) + list( [ pair[1] ] )  
        ## on vire weigth
        path.pop(-2) 
        node = node | set( x for x in flattening(path)  )
        
        label += [ u"->".join(unicode(x) for x in path[1::] ) ]

        while len(path) >= 2:
            if isinstance( path[1], int) or ( path[0:2]) not in edge :
                edge += [ ( path[0:2] ) ]
            path.pop(0)
    for n in node:
        graph.add_node( pd.Node( n) )
    for e in edge:
        arg = dict()
        if isinstance(e[1],int):
            arg = dict( label = label.pop(0) )
        graph.add_edge( pd.Edge( e[0], e[1], arrowhead="normal", **arg ))
    graph.write_jpeg(out_name)

t1 = u"""Je vais à la pêche aux moules moules moules, qui viendras avec moi?"""
t2 = u"""je vais à la pêche électorale aux voies"""
t3 = u"""tous les chemins mènent à Rome"""
t4 = u"""Le je du jeu, Jeune je vois, est il une jeunesse ?"""
t5 = u"""je jeune à jeun, jeu à jouer"""

def path_collider(vector, path):
    """adding a path to a vector"""
    path_copy = list(path)
    if not isinstance( vector, VectorDict):
        if len(vector):
            vector = tree_from_path( vector + [ "weight" , 1 ])
        else:
            vector = VectorDict( VectorDict, dict() )
    current = vector
    while len(path) :
        current_key = path.pop(0)
        if current_key in current.keys():
            
            current = current[current_key]
            if current.get("weight", False):
                current["weight"]+=1
        else:
            path = [ current_key ] + path
            break
    if len(path):
        vector.add_path( path_copy + [ "weight" , 1 ] )
    return vector 

def text_grapher(unicode_text):
    sp_pattern = re.compile( "[\s\-\,\']+", re.M)
    return reduce( 
        path_collider,  
        map( 
                lambda string : filter(unicode.isalpha,list(string)) ,
                map( unicode.lower,sp_pattern.split(unicode_text ) ) 
       )
    )
print "sample of a text to word counter"
text_grapher(t1).pprint()

print "some cos"
print "cos t1, t2"
print text_grapher(t1).cos(text_grapher(t2))
print "cos t1, t3"
print text_grapher(t1).cos(text_grapher(t3))

print "cos t4, t5"
print text_grapher(t4).cos(text_grapher(t5))


mysogine = text_grapher( open("myso-fr.txt","rt",encoding= "utf-8" ).read() )
mysogine.pprint()
dot_graph( mysogine, "mysogine.svg")


troll = text_grapher(  open("troll.txt","rt", encoding='utf-8').read() )

chienne = text_grapher(  open("chienne.txt","rt", encoding='utf-8').read() )

print "la page de garde de chienne de garde est elle troll ou missogyne? %r ou %r " % (troll.cos( chienne) , mysogine.cos( chienne))
blague = text_grapher(  open("blague-myso.txt","rt", encoding='utf-8').read() )
print "blague mysogyne est elle un troll ou misogyne? %r ou %r " % (troll.cos( blague) , mysogine.cos( blague))

print "troll cos mys = %r" % troll.cos( mysogine )
