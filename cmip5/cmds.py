"""
Bash commands for various file operations
=========================================

Those commands use CDO and NCO.

 * Concatenate records
 * Create monthly climatologies over specified periods.

The core functions simply return the command string. Users are then
responsible to launch those on their system.


"""

import os
import glob
from cmip5 import esg
from cmip5.general import NestedDict


def cluster_time_slices(path):
    """Identify all files within the directory `path` that belong to the
    same simulation and that could be concatenated along their record
    dimension (time).

    Parameters
    ----------
    path : str
      Path to a directory containing netCDF datasets.

    Returns
    -------
    A NestedDict holding a sequence of files belonging to the same simulation
    and variable.
    """
    F = NestedDict()
    files = glob.glob(os.path.join(path, '*.nc'))
    files.sort()

    # Create a structure holding all files, stored by attributes
    for f in files:
        d = esg.fn_split(f)
        if d['MIPtable'] == 'fx':
            continue

        period, MIPtable, experiment, variable, model, ensemble = d.values()

        if not F[variable][MIPtable][model][experiment].has_key(ensemble):
            F[variable][MIPtable][model][experiment][ensemble] = []

        F[variable][MIPtable][model][experiment][ensemble].append(f)

    return F


def agg_file_name(*args):
    """Return a new file name constructed from aggregating multiple files
    spanning consecutive periods.
    """

    if len(args) == 1:
        return args[0]
    else:
        files = args
        n1 = esg.fn_split(files[0])['period'].split('-')[0]
        n2 = esg.fn_split(files[-1])['period'].split('-')[1]

        d = esg.fn_split(files[0])
        d['period'] = '-'.join((n1, n2))
        return esg.fn_from(**d)


def concatenate(path):
    """Return bash commands to concatenate files belonging to the same
    simulation and variable using CDO, and bash commands that remove the
    original files.
    """

    F = cluster_time_slices(path)
    cmds = []; rm = []
    # Concatenate files belonging to the same simulation.
    for keys, files in F.walk():
        if len(files) == 1:
            continue

        n1 = esg.fn_split(files[0])['period'].split('-')[0]
        n2 = esg.fn_split(files[-1])['period'].split('-')[1]

        d = esg.fn_split(files[0])
        d['period'] = '-'.join((n1, n2))
        ofile = esg.fn_from(**d)
        if os.path.exists(ofile):
            continue
        cmds.append("cdo cat " + ' '.join(files) + ' ' + ofile )
        rm.append("rm " + ' '.join(files))

    return cmds, rm


def monthly_clim(ifile, ofile=None, years=None, tag='', options='-f nc4'):
    """Return bash commands to compute the monthly climatology from a file or
    a sequence of files over the specified years using CDO.

    The function returns a call to cdo operator ymonavg.

    Parameters
    ----------
    ifile : str
      Path to input file or sequence of paths.
    ofile : str
      Path to output file, if None, a file name will be created in the
      current directory.
    years : (y1, y2)
      Tuple of start and end years. If None compute the climatology over the
      complete time span.
    tag : str
       Identifying tag used when generating `ofile` to identify individual
       periods. Useful if many climatologies are computed for the same experiment.
       For example, use `ctl` to refer to the 1970-1999 period.

    Example
    -------
    >>> monthly_clim('../data/sic_OImon_CCSM4_rcp85_r1i1p1_200601-210012.nc', years=(2040, 2069), tag='<f50>')
    'cdo ymonavg -seldate,2040-01-01,2069-12-31 ../data/sic_OImon_CCSM4_rcp85_r1i1p1_200601-210012.nc sic_OImon_CCSM4_rcp85_r1i1p1_204001-206912-clim<f50>.nc'

    """
    import collections

    if type(ifile) == str:
        ifile = [ifile,]

    # Check that all files belong to the same simulation.
    S = collections.defaultdict(set)
    for f in ifile:
        for key, val in esg.fn_split(f).items():
            S[key].add(val)
    for key, val in S.items():
        if len(val) > 1 and key != 'period':
            raise ValueError("Files don't all belong to the same simulation and variable.")


    # Find the start and end dates of the input files
    starts, ends, clims = zip(*[esg.fn_date(esg.fn_split(f)['period']) for f in ifile])
    if any(clims):
        raise ValueError("Climatology file found.")
    start, end = starts[0], ends[-1]


    # If years is a slice, convert to a tuple of years using the range between
    # the start and end dates.
    r = range(start.year, end.year+1)
    if years:
        if type(years) == slice:
            years = r[years][0], r[years][-1]


    # Select only the files that fall within that range.
    infile = []
    for i, f in enumerate(ifile):
        if ends[i].year > years[0] and starts[i].year < years[1]:
            infile.append(f)

    if len(infile) == 0:
        return

    # Create output file if none is given.
    if ofile is None:
        d = esg.fn_split(infile[0])
        if years:
            d['period'] = "{0}01-{1}12".format(*years)
        else:
            d['period'] = "{0}01-{1}12".format(start.year, end.year)

        ofile = esg.fn_from(clim='clim{0}'.format(tag), **d)

    # Create the CDO commands
    cmd = ["cdo", options, "ymonavg"]

    if years:
        y1,y2 = years
        cmd.append("-seldate,{0}-01-01,{1}-12-31".format(y1, y2))

    if len(infile) > 1:
        cmd.extend(["-cat", ] + infile)
    else:
        cmd.append(infile[0])

    cmd.append(ofile)

    return ' '.join(cmd)
