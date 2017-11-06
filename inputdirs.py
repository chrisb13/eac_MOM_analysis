#!/usr/bin/env python 
#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Mon, 06 Nov 2017 11:22:44
#   Machine created on: chris-VirtualBox2
#

"""
This module is for adjusting the input dirs and experiments.
"""

import collections
from _indlogger import _LogStart

_lg=_LogStart().setup()

paper_case='20171106_EACtrades'


#this is used by shareme to glob fewer files. If years is undefined, then it will glob everyfile it can. Must only contain two dates
# years=[\
# ('1994-01-01','2009-12-31')\
# ]



if paper_case=='20171106_EACtrades':
    output_folder='/srv/ccrc/data48/z3457920/20171106_EACtrades/'
    # output_folder='/home/chris/mount_win/nic/'
    plot_outputs=output_folder+'plots/'
    
    #new experiments to fix different stress problem
    mom_fols=collections.OrderedDict()
    mom_fols['gfdl_nyf_1080_all']    =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_all/']
    mom_fols['gfdl_nyf_1080_allF']   =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_allF/']
    mom_fols['gfdl_nyf_1080_base']   =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_base/']
    mom_fols['gfdl_nyf_1080_full']   =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_full/']
    mom_fols['gfdl_nyf_1080_windo']  =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_windo/']
    mom_fols['gfdl_nyf_1080_windoF'] =['/srv/ccrc/data33/z3400368/gfdl_nyf_1080_windoF/']

if __name__ == "__main__":                                     #are we being run directly?
    pass
