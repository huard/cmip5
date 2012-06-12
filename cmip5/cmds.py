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


def monthly_clim(ifile, ofile=None, years=None):
    """Compute the monthly climatology from a file over the specified years.
    
    Parameters
    ----------
    ifile : str
      Path to input file.
    ofile : str
      Path to output file, if None, a file name will be created in the
      current directory.
    years : (y1, y2) 
      Tuple of start and end years.
      
    """
    if not os.path.exists(ifile):
        raise IOError("Input file does not exist: {0}".format(ifile))
        
    if ofile is None:
        d = esg.fn_split(ifile)
        if years:
            d['period'] = "{0}01-{1}12".format(*years)
        
        fn_from(**d, clim=True)
        
    
    if years:
        y1,y2 = years
        start = "{0}-01-01".format(y1)
        end = "{0}-12-31".format(y2+1)
        cmd = "cdo ymonavg -seldate,{0},{1} {2} {3}".format(start, end, ifile, ofile)
    	
    else:
        cmd = "cdo ymonavg {0} {1}".format(ifile, ofile)

    return cmd

    
