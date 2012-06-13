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
import urllib, json, os
import datetime as dt

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
    
    
def fn_split(fn):
    """Return a dictionary of the file name components:
        * variable
        * MIP table
        * model
        * experiment
        * ensemble member
        * [period]
        
    Example
    -------
    >>> fn_split("tas_Amon_HADCM3_historical_r1i1p1_185001-200512.nc")
    {'MIPtable': 'Amon',
     'ensemble': 'r1i1p1',
     'experiment': ' historical',
     'model': 'HADCM3',
     'period': '185001-200512',
     'variable': 'tas'}

    """
    keys = 'variable', 'MIPtable', 'model', 'experiment', 'ensemble'
    
    head, tail = os.path.split(fn)
    vals = tail.split('_')
    
    meta = dict(zip(keys, vals))
    
    if len(vals) == 6:
        meta['period'] = os.path.splitext(vals[-1])[0]
        
    return meta
    
def fn_from(variable, MIPtable, model, experiment, ensemble, period=None, clim=False):
    fn = "_".join((variable, MIPtable, model, experiment, ensemble))
    if period:
        fn = fn + "_" + period
    
        if clim:
            fn = fn + "-clim"
         
    fn = fn + ".nc"
    return fn
    
    
def fn_date(period):
    """Return datetime objects for the start and end instants and a 
    boolean indicating whether or not the file is a climatological mean.
    
    Example
    -------
    >>> fn_date("185001-200512")
    (datetime.datetime(1850, 1, 1, 0, 0),
     datetime.datetime(2005, 12, 1, 0, 0),
     False)
     
    Notes
    -----
    Only support a single date format for now.
    """
    
    vals = period.split('-')
    n1 = dt.datetime.strptime(vals[0], '%Y%m')
    n2 = dt.datetime.strptime(vals[1], '%Y%m')
    clim =  len(vals) == 3
    if clim:
        assert vals[-1] == 'clim'
    return n1, n2, clim
    
#sock = urllib.urlopen(url)
#return json.load(sock)

    
