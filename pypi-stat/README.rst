Getting stats
*************
 
Utility for retrieveing stats 

 $ ./pypi_get_stat.py -h
 Usage: pypi_get_stat.py [options]
 
 Options:
   -h, --help            show this help message and exit
   -p _PACKAGE, --package=_PACKAGE
                         packages for wich to retrieve the stat

more than one package can be provided with the -p option
All results are stored in ~/.pypi.stat.json for later use. 
This script do not require numpy, matplotlib nor VectorDict
 
 $ ./pypi_get_stat.py -p VectorDict
 PyPI Package statistics for: VectorDict
 
     First Upload:            lun. 06 févr. 2012 17:57:51  (0.3.0)
     Last Upload:              jeu. 12 avril 2012 12:38:26  (1.0.0)
     Number of releases:                                  9
     Most downloads:                                    266
     Fewest downloads:                                    0
     Average downloads:                                 165
     Total downloads:                                 1 491
 
 
Graphing previously stored statistics about pipy
************************************************



Can be graphed : 
 
 * av_dl average download
 * max_dl maximum download
 * min_dl fewest download 

All these keys can be combined. 

Output is a file YYYY-MM-DD-pack1,pack2-stat.png in current dir  plus a matplotlib output (that does not work here:( )
 
output can be limited to only one of these by using --do save or --do plot. 

date are meant to be entered in isoformat "%Y-%m-%d"

BUG : ax.autoscale dont work on first graph :'( 
for accurate results I do recommand using doing stat one package per one package


 $ ./pypi_graph_stat.py -h
 Usage: pypi_graph_stat.py [options]
 
 Options:
   -h, --help            show this help message and exit
   -k KEY                keys to plot in stored stats
   -f _FROM, --from=_FROM
                         min date
   -t _TO, --to=_TO      to
   -a _ACTION, --do=_ACTION
                         action to do in save & show      *show* orders a
                         matplotlib show, *save* saves the graph in YYYYY-MM-
                         DD-pakkage1,package2-stat.png" in the      current dir
   -p _PACKAGE, --package=_PACKAGE
                         packages for wich to graph
 
