"""
Bash commands for various file operations
=========================================

Those commands use CDO and NCO.

 * Concatenate records
 * Create monthly climatologies over specified periods.

The core functions simply return the command string. Users are then
responsible to launch those on their system. 


"""
import esg
import os, warnings, glob
from general import NestedDict

def concatenate(path):
    """Identify all files within the directory `path` that belong to the
    same simulation and that could be concatenated along their record 
    dimension, ie time, concatenate them and remove the original files.
    
    Parameters
    ----------
    path : str
      Path to a directory containing netCDF datasets.
    """
    F = NestedDict()
    files = glob.glob(os.path.join(path, '*.nc'))
    files.sort()
    
    cmds = []
    rm = []
    # Create a structure holding all files, stored by attributes
    for f in files:
        d = esg.fn_split(f)
        if d['MIPtable'] == 'fx':
            continue

        period, MIPtable, experiment, variable, model, ensemble = d.values()

        if not F[variable][MIPtable][model][experiment].has_key(ensemble):
            F[variable][MIPtable][model][experiment][ensemble] = []
    
        F[variable][MIPtable][model][experiment][ensemble].append(f)
        
    # Concatenate files belonging to the same simulation.
    for keys, files in F.walk():
        if len(files) == 1:
            continue  

        n1 = esg.fn_split(files[0])['period'].split('-')[0]
        n2 = esg.fn_split(files[-1])['period'].split('-')[1]
        
        d = esg.fn_split(files[0])
        d['period'] = '-'.join((n1, n2))
        ofile = esg.fn_from(**d)
        
#        cmds.append("ncrcat " + ' '.join(files) + ' ' + ofile )
        cmds.append("cdo cat " + ' '.join(files) + ' ' + ofile )
        rm.append("rm " + ' '.join(files))

    return cmds, rm
    

def monthly_clim(ifile, ofile=None, years=None):
    """Compute the monthly climatology from a file over the specified years.
    
    The function returns a call to cdo operator ymonavg.
        
    Parameters
    ----------
    ifile : str
      Path to input file.
    ofile : str
      Path to output file, if None, a file name will be created in the
      current directory.
    years : (y1, y2) 
      Tuple of start and end years.
      
      
    Example
    -------
    >>> monthly_clim('../data/sic_OImon_CCSM4_rcp85_r1i1p1_200601-210012.nc', years=(2040, 2069))
    'cdo ymonavg -seldate,2040-01-01,2069-12-31 ../data/sic_OImon_CCSM4_rcp85_r1i1p1_200601-210012.nc sic_OImon_CCSM4_rcp85_r1i1p1_204001-206912-clim.nc'
    
    """
    a1, a2, clim = esg.fn_date(esg.fn_split(ifile)['period'])
    if clim:
        return

    r = range(a1.year,a2.year+1)
    if years:
        if type(years) == slice:
            years = r[years][0], r[years][-1]

    if ofile is None:
        d = esg.fn_split(ifile)
        if years:
            d['period'] = "{0}01-{1}12".format(*years)
        
        ofile = esg.fn_from(clim=True, **d)
        
    if years:
        y1,y2 = years
           
        start = "{0}-01-01".format(y1)
        end = "{0}-12-31".format(y2)
        cmd = "cdo ymonavg -seldate,{0},{1} {2} {3}".format(start, end, ifile, ofile)
    	
    else:
        cmd = "cdo ymonavg {0} {1}".format(ifile, ofile)

    if not os.path.exists(ifile):
        warnings.warn("Input file does not exist: {0}".format(ifile))

    return cmd

    
