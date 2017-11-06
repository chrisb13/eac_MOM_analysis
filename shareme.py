#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Mon, 06 Nov 2017 11:42:04
#   Machine created on: chris-VirtualBox2
#
"""
This module is for commonly used variables and functions for the EAC mom trades project.
"""

import glob
from _smlogger import _LogStart

import inputdirs as ind

_lg=_LogStart().setup()

import collections

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

#for inset axes
#hacked from:
#http://matplotlib.org/examples/axes_grid/inset_locator_demo.html
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

def grab_ocean(epath):
    """function to grab ocean.nc file from Nic's experiments.
    
    :arg1: @todo
    :returns: @todo
    """
    ifiles=sorted(glob.glob(ind.mom_fols[epath][0]+'output*/ocean.nc'))
    assert(ifiles!=[]),"glob didn't find anything!"
    fs=collections.OrderedDict()
    for f in ifiles:
        fs[int(os.path.basename(os.path.dirname(f))[-3:])+1791]=f
    # print ifiles
    return pd.Series(fs)

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def mom_fixdateline(netcdf_datasetobj):
    """function to return fixed version of netcdf nav_lon variable
    
    Update 2016.11.08: now can cope with ORCA025's global output

    :netcdf_datasetobj: netCDF4 Dataset object of nemo file
    :returns: nemo_lons numpy array with fixed dateline
    """
    mom_lons=netcdf_datasetobj.variables['xt_ocean'][:]
    #fix the dateline
    for index in np.arange(np.shape(mom_lons)[0]):
        # start=np.where(np.sign(nemo_lons[index,:])==-1)[0][0]
        # nemo_lons[index,start:]=nemo_lons[index,start:]+360

        if np.sign(mom_lons[index])==-1:
            mom_lons[index]=mom_lons[index]+360
    return mom_lons 

def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       _lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

def exp_colours_nic(hex=True):
    """function to return nice colorbrewer colours for the experiments we focus on

    :hex: @todo
    :returns: @todo
    """

    if hex:
        ecolours=collections.OrderedDict()
        ecolours['gfdl_nyf_1080_all']   ='#e41a1c'
        ecolours['gfdl_nyf_1080_allF']  ='#e41a1c'
        ecolours['gfdl_nyf_1080_base']  ='#4daf4a'
        ecolours['gfdl_nyf_1080_full']  ='#984ea3'
        ecolours['gfdl_nyf_1080_windo'] ='#ff7f00'
        ecolours['gfdl_nyf_1080_windoF']='#ff7f00'
        
        ecolours_names=collections.OrderedDict()
        # ecolours_names['CTRL']             ='#e41a1c'
        # # ecolours_names['nemo_cordex24_ERAI01b']          
        # ecolours_names['noNZ500']  ='#377eb8'
        # ecolours_names['noNZ80']   ='#4daf4a'
        # ecolours_names['FB']       ='#984ea3'
        # ecolours_names['FBnoNZ']   ='#ff7f00'
        # ecolours_names['SugarLoaf']      ='#ffff33'
        return ecolours,ecolours_names


def pl_inset_title_box(ax,title,bwidth="20%",location=1):
    """
    Function that puts title of subplot in a box
    
    :ax:    Name of matplotlib axis to add inset title text box too
    :title: 'string to put inside text box'
    :returns: @todo
    """

    axins = inset_axes(ax,
                       width=bwidth, # width = 30% of parent_bbox
                       height=.30, # height : 1 inch
                       loc=location)

    plt.setp(axins.get_xticklabels(), visible=False)
    plt.setp(axins.get_yticklabels(), visible=False)
    axins.set_xticks([])
    axins.set_yticks([])

    axins.text(0.5,0.3,title,
            horizontalalignment='center',
            transform=axins.transAxes,size=10)
    return


def exp_names(exp_subset=None):
    """function to return nice names for the EAC variability paper
    :exp_subset=None:
    :returns: @todo

    Example
    --------
    >>> enames=sm.exp_names(exp_subset=['nemo_cordex24_FLATFCNG_ERAI01','nemo_cordex24_FLATOBC_ERAI01'])
    """
    enames=collections.OrderedDict()
    enames['nemo_cordex24_FLATFCNG_ERAI01']='CONSTANT'
    enames['nemo_cordex24_FLATERAI_ERAI01']='VARY-OBC'
    enames['nemo_cordex24_FLATOBC_ERAI01'] ='VARY-LOCAL'
    enames['nemo_cordex24_ERAI01']         ='VARY-ALL'

    enames['nemo_cordex24_DFLX_0ERAIWND_01']=        '0mean'
    enames['nemo_cordex24_DFLX_3xVERAIWNDBND_01']=   '3x_330-400'
    enames['nemo_cordex24_DFLX_3xVERAIWNDBND0MN_01']='3x_300-400+0mean'
    enames['nemo_cordex24_DFLX_3xVERAIWNDHGH_01']=   '3x_>400'
    enames['nemo_cordex24_DFLX_3xVERAIWNDLOW_01']=   '3x_<400'
    enames['nemo_cordex24_DFLX_VERAIWNDBND_01']=     '330-400'
    enames['nemo_cordex24_DFLX_VERAIWNDBND0MN_01']=  '300-400+0mean'
    enames['nemo_cordex24_DFLX_VERAIWNDHGH_01']=     '<400'
    enames['nemo_cordex24_DFLX_VERAIWNDLOW_01']=     '>400'
    enames['nemo_cordex24_DFLX_VERAIW330H_01']=      '<330'
    enames['nemo_cordex24_DFLX_VERAIWB148330_01']=   '148-330'
    enames['nemo_cordex24_DFLX_VERAIWB056148_01']=   '56-148'
    enames['nemo_cordex24_DFLX_VERAIW330L_01']=      '>330'
    enames['nemo_cordex24_DFLX_VERAIW056H_01']=      '<56'
    enames['nemo_cordex24_DFLX_VERAITR_01']=         'VERAI_TR'
    enames['nemo_cordex24_DFLX_VERAIBR_01']=         'VERAI_BR'

    #see /home/z3457920/hdrive/repos/nemo/nemo_analysis/configs/README

    if exp_subset is None:
        pass
    else:
        enames={k: enames[k] for k in exp_subset}

    return enames


if __name__ == "__main__":                                     #are we being run directly?
    pass
