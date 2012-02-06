#!/usr/bin/env python
# -*- coding: utf-8 -*-
#WTFPL
"""maybe giving a sense to
dict( { a : 1 } ) + dict(  { a : 2 } ) + dict( { b : 2 } )
would be a practical for map reduce operations in nosql/large dataset
(HDF5 iterators) like context. Je dis ça, je dis rien"""
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


from vector_dict.VectorDict import iter_object,  VectorDict
from csv import reader, writer
import os
from io import StringIO
from numpy import array

### CSV of langage users in a nosql DB (or any cloudish crap)
### having individual votes of cooolness per langage
### should be a very large dataset to be funnier

mocking_nosql = u"""george,FR,fun,perl,2
roger,FR,serious,python,3
christine,DE,fun,python,3
bob,US,serious,php,1
isabelle,FR,fun,perl,10
Kallista,FR,unfun,c#,-10
Nellev,FR,typorigid,python,1
haypo,FR,javabien,python,1
potrou,FR,globally locked,python,1
petra,DE,sexy,VHDL,69"""

nosql_iterator = reader

### interesting columns/key we want to emit
COUNTRY = 1
LANGAGE = 3
COOLNESS = 4

w = writer(os.sys.stdout)

## basic example for counting langage users nothing more interesting than
## what collections.counter does
print ""
w.writerow(["langage", "how many users"])
map(w.writerow,
    iter_object(
        reduce(
            ## well that is a complex reduce operation :)
            VectorDict.__iadd__,
            map(
                lambda document: VectorDict(int, {document[LANGAGE]: 1}),
                nosql_iterator(StringIO(mocking_nosql))
            )
        ),
        flatten = True
    )
)
"""expected result :
langage,how many users
python,3
c#,1
php,1
VHDL,1
perl,2
"""
print "\n" * 2 + "next test\n"
### example with group by + aggregation of a counter
### counting all langage per country with their coolness and number of users
### Hum .... I miss a sort and a  limit by to be completely SQL like compatible
w.writerow(["country", "langage", "coolness", "howmany"])
map(w.writerow,
    iter_object(
        ##nosql like reduce
        reduce(
            ## well that is the same very complex reduce operation :)
            VectorDict.__iadd__,
            ##nosql like map where we emit interesting subset of the record
            map(
                lambda document: VectorDict(
                    VectorDict, {
                        #KEY
                        document[COUNTRY]:
                        VectorDict(
                            array,
                            {
                                #GROUPBY
                                document[LANGAGE]:
                                #AGGREGATOR
                                array([
                                    #Counter
                                    int(document[COOLNESS]),
                                    #presence
                                    1
                                ])
                            }
                        ),
                        ## making a (sub) total on the fly
                        'total_coolness_and_voters': array([
                            int(document[COOLNESS]), 1
                        ])
                    }
                ),

                ## nosql like filter that should be in the map if it was nosql
                ## maybe we also need a map that accepts None as a result and
                ## skip the result in the resulting iterator,
                ## or a skip() callable in lambda ?
                ## or sub()  like in perl with curly braces
                ## joke : combining map / filter is easy enough
                filter(
                    lambda document: "php" != document[LANGAGE],
                    nosql_iterator(StringIO(mocking_nosql))
                )
            )
        ),
            flatten = True
    )
)
"""expected result :
country,langage,coolness,howmany
FR,python,4,2
FR,c#,-10,1
FR,perl,12,2
total_votes_and_coolness,7,78
DE,python,3,1
DE,VHDL,69,1
"""
