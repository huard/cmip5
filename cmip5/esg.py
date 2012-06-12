"""
Functions to handle Earth System Grid queries
=============================================

There is some documentation on the API for queries to the ESG gateways
on the [ESGF wiki](http://esgf.org/wiki/ESGF_Search_Service).

Note: I'm just a newbie user, don't take the following too literally. 

The ESGF maintains a network of gateways, ie servers running largely 
the same software that provides access to data archived locally and 
at the other gateways. These gateways can be queried to return the 
set of files hosted over the entire network of gateways. 

There are two kind of queries: search and wget. "search" returns 
a text file containing the search results. With wget we get a 
script ready (almost) to be launched to download the selected files.

The syntax for these queries can be found at the links given above, 
but here are the selection criteria that I find most helpful:

      Ensemble: ensemble, e.g. r1i1p1. 
      Experiment: experiment, e.g. historical
      Model: model
      Project: project, e.g. CMIP5
      Product: product, e.g. output1
      Realm: realm, e.g. seaIce
      Time Frequency: time_frequency, e.g. mon
      Variable: variable
      Variable Long Name: variable_long_name
   
Other useful parameters are 

    latest : true, false (to dimiss older replicas)
    type : File, Dataset
    format : application/solr+json or application/solr+xml (format of the return file)
"""
import urllib, json

ESG_NODE = "http://pcmdi9.llnl.gov/"
#node = r"http://www.earthsystemgrid.org/"
#node = r"http://esg-datanode.jpl.nasa.gov/"
    
    
def search_url(latest=True, type='Dataset', format='application/solr+json', **kwds):
    """Return the search URL.
    
    The keyword parameters are defined in the top module documentation.
    
    Example
    -------
    >>> search_url(project='CMIP5', variable='tas', time_frequency='mon', experiment='rcp85')
    
    """
    info = r'&'.join( [r"{0}={1}".format(key, urllib.quote(val)) for key, val in kwds.items()] )
    return ESG_NODE + 'esg-search/search?' + info
    
    
#sock = urllib.urlopen(url)
#return json.load(sock)

    
