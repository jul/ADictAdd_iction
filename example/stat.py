#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculates the total number of downloads that a particular PyPI package has
received across all versions tracked by PyPI
author : codekoala (not me)
License : ask codekoala
source : http://www.codekoala.com/blog/2010/pypi-download-stats/
Added a save method
"""

from datetime import datetime
import locale
import sys
import xmlrpclib

locale.setlocale(locale.LC_ALL, '')

class PyPIDownloadAggregator(object):

    def __init__(self, package_name, include_hidden=True):
        self.package_name = package_name
        self.include_hidden = include_hidden
        self.proxy = xmlrpclib.Server('http://pypi.python.org/pypi')
        self._downloads = {}

        self.first_upload = None
        self.first_upload_rel = None
        self.last_upload = None
        self.last_upload_rel = None

    @property
    def releases(self):
        """Retrieves the release number for each uploaded release"""

        result = self.proxy.package_releases(self.package_name, self.include_hidden)

        if len(result) == 0:
            # no matching package--search for possibles, and limit to 15 results
            results = self.proxy.search({
                'name': self.package_name,
                'description': self.package_name
            }, 'or')[:15]

            # make sure we only get unique package names
            matches = []
            for match in results:
                name = match['name']
                if name not in matches:
                    matches.append(name)

            # if only one package was found, return it
            if len(matches) == 1:
                self.package_name = matches[0]
                return self.releases

            error = """No such package found: %s

Possible matches include:
%s
""" % (self.package_name, '\n'.join('\t- %s' % n for n in matches))

            sys.exit(error)

        return result

    @property
    def downloads(self, force=False):
        """Calculate the total number of downloads for the package"""

        if len(self._downloads) == 0 or force:
            for release in self.releases:
                urls = self.proxy.release_urls(self.package_name, release)
                self._downloads[release] = 0
                for url in urls:
                    # upload times
                    uptime = datetime.strptime(url['upload_time'].value, "%Y%m%dT%H:%M:%S")
                    if self.first_upload is None or uptime < self.first_upload:
                        self.first_upload = uptime
                        self.first_upload_rel = release

                    if self.last_upload is None or uptime > self.last_upload:
                        self.last_upload = uptime
                        self.last_upload_rel = release

                    self._downloads[release] += url['downloads']

        return self._downloads

    def total(self):
        return sum(self.downloads.values())

    def average(self):
        return self.total() / len(self.downloads)

    def max(self):
        return max(self.downloads.values())

    def min(self):
        return min(self.downloads.values())

    def save(self):
        from os import path, environ
        from json import load, dump, dumps
        sep = str
        from time import mktime
        from datetime import date 
        save=path.join(environ["HOME"], ".pipy.stat.json"  )
        
        json = dict(
            date = "%s" % date.today(),
            name = self.package_name,
            first_upload = '%s'  % self.first_upload,
            first_release =  self.first_upload_rel,
            last_upload = '%s' % self.last_upload,
            last_release  = sep(self.last_upload_rel),
            nb_release = sep(len(self.releases)),
            max_dl = sep(self.max()),
            min_dl = sep(self.min()),
            av_dl = sep(self.average()),
            total_dl = sep(self.total()),
        )
        if not path.exists(save):
            with file(save,"w") as f:
                f.write("[]")
        
        result = load(open(save))
        ## would be better
        ## delete all existing entry for the existing date
        result = filter( lambda r : r["name"] != self.package_name or 
            r["date"] != str(date.today() ),
            result )
        result += [  json ]
        print dumps(result, indent=4)
        dump(result,open(save,"w"))


    def stats(self):
        """Prints a nicely formatted list of statistics about the package"""

        self.downloads # explicitly call, so we have first/last upload data
        fmt = locale.nl_langinfo(locale.D_T_FMT)
        sep = lambda s: locale.format('%d', s, 3)
        val = lambda dt: dt and dt.strftime(fmt) or '--'

        params = (
            self.package_name,
            val(self.first_upload),
            self.first_upload_rel,
            val(self.last_upload),
            self.last_upload_rel,
            sep(len(self.releases)),
            sep(self.max()),
            sep(self.min()),
            sep(self.average()),
            sep(self.total()),
        )

 

        print """PyPI Package statistics for: %s

    First Upload: %40s (%s)
    Last Upload:  %40s (%s)
    Number of releases: %34s
    Most downloads:    %35s
    Fewest downloads:  %35s
    Average downloads: %35s
    Total downloads:   %35s
""" % params
    ### gruiky to override coupling
        self.save()

def main():
    if len(sys.argv) < 2:
        sys.exit('Please specify at least one package name')

    for pkg in sys.argv[1:]:
        PyPIDownloadAggregator(pkg).stats()


if __name__ == '__main__':
    main()
   

