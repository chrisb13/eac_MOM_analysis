#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Mon, 06 Nov 2017 11:34:05
#   Machine created on: chris-VirtualBox2
#
"""
This file is for using calculating transports from Nicola's mom outputs
"""
#
#python logging
import logging as lg
import time
import os

import sys

pathfile = os.path.dirname(os.path.realpath(__file__)) 
sys.path.insert(1,os.path.dirname(pathfile)+'/')

from cb2logger import *

import inputdirs as ind
import shareme as sm

import os
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import glob

import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from matplotlib import gridspec

def get_sect_local():
    """@todo: Docstring for get_sect_local
    
    :arg1: @todo
    :returns: @todo
    """
    #From Figure 4 caption in:
    #Oliver, E. C. J., and N. J. Holbrook (2014), Extending our understanding of South Pacific gyre spin-up: Modelling the East Australian Current in a future climate, J. Geophys. Res. Ocean.

    #A 148    -43  
    #B 150    -43  
    #C 170.5  -43 
    #D 173    -28 
    #E 155.7  -28 
    #F 153.5  -28  
    #G 173    -34.4 
    #H 146.5  -43.5 
    #I 146.5  -46 

    # we can find where these sections are using 

    section_description_dict=collections.OrderedDict()

    exp=ind.mom_fols.keys()[0]
    lg.info("We are using :" + exp + " for our section definitions")
    ifiles=sm.grab_ocean(exp)

    f=ifiles.values[0]
    lg.info("We are working file (for sect def):" + f)
    ifile=Dataset(f, 'r')
    newlons=sm.mom_fixdateline(ifile)
    lats=ifile['yu_ocean'][:]

    section_description_dict['FE']=\
    [sm.find_nearest(newlons,153.6),\
     sm.find_nearest(newlons,155.6),\
     sm.find_nearest(lats,-27.8),\
     sm.find_nearest(lats,-27.8),\
     0,\
     33,\
     'zonal']

    section_description_dict['AB']=\
    [sm.find_nearest(newlons,148.2),\
     sm.find_nearest(newlons,150.8),\
     sm.find_nearest(lats,-42.6),\
     sm.find_nearest(lats,-42.6),\
     0,\
     33,\
     'zonal']

    section_description_dict['JK']=\
    [sm.find_nearest(newlons,150.1),\
     sm.find_nearest(newlons,151.7),\
     sm.find_nearest(lats,-37.1),\
     sm.find_nearest(lats,-37.1),\
     0,\
     33,\
     'zonal']

    #REALLY should check these sections CHRIS!
    #plt.close('all')
    #fig=plt.figure()
    #ax=fig.add_subplot(1, 1,1)
    ## x,y=np.meshgrid(newlons,lats)
    #ax.contourf(ifile['sea_level'][0,:],30)
    #plt.show()
    #import pdb
    #pdb.set_trace()

    #ifile.close()
    return section_description_dict

def main_trans():
    """@todo: Docstring for main_trans
    :returns: @todo
    """
    for exp in ind.mom_fols.keys():
        efile=ofol+exp+'_trans_tseries_table.h5'
        # print efile
        if os.path.exists(efile):
            lg.info("Transport already calculated for experiment :" + exp + ". Skipping..")
            continue

        lg.info("We are working experiment :" + exp)
        ifiles=sm.grab_ocean(exp)

        df_trans=collections.OrderedDict()
        df_trans['FE']=collections.OrderedDict()
        df_trans['AB']=collections.OrderedDict()
        df_trans['JK']=collections.OrderedDict()
        for f in ifiles.iteritems():
            lg.info("We are working file:" + f[1])
            ifile=Dataset(f[1], 'r')

            #early kill switch
            # if f[0]==1995:
                # break

            for sect in sect_dict.keys():
                idxs=sect_dict[sect]
                # ty_trans(time, st_ocean, yu_ocean, xt_ocean)

                # df_trans[sect]=\
                for t in np.arange(np.shape(ifile['ty_trans'])[0]):
                    trans=\
                    ifile['ty_trans'][t,\
                          idxs[4]:idxs[5],\
                          idxs[2]:idxs[3]+1,\
                          idxs[0]:idxs[1]+1]
                    
                    df_trans[sect]\
                    [pd.to_datetime(str(f[0])+'-'+str(t+1).zfill(2))]=\
                    np.sum(trans)
                    
            ifile.close()
        df=pd.DataFrame(df_trans)

        #Due to Pandas 'TypeError' had to use put rather than append...
        store = pd.HDFStore(efile,complevel=9, complib='blosc')
        store.put('df',df)
        store.close()
        print efile
    return

def pl_trans(meanonly=False):
    """@todo: Docstring for pl_trans()
    :returns: @todo
    """
    ifiles=sorted(glob.glob(ofol+'*_trans_tseries_table.h5'))
    assert(ifiles!=[]),"glob didn't find anything!"
    plt.close('all')
    fig=plt.figure()

    ax1=fig.add_subplot(3, 1,1)
    ax2=fig.add_subplot(3, 1,2)
    ax3=fig.add_subplot(3, 1,3)

    ecos=sm.exp_colours_nic(hex=True)[0]

    #Pzos was a dictinoary containing names and the number of subplots
    
    plt.close('all')
    row=3
    col=1
    fig=plt.figure(figsize=(14.0*col,8*1))
    gs = gridspec.GridSpec(row, col,height_ratios=[1]*row,width_ratios=[1]*col,hspace=.045,wspace=0.045)
    
    axis=[]
    for r in range(row):
        axis.append(plt.subplot(gs[r]))
    
    sects=['FE','JK','AB']
    for idx,ax in enumerate(axis):
        sect=sects[idx]
        for f in ifiles:
            # print f,idx,sect
            ename=os.path.basename(f)[:-23]
            colour=ecos[ename]
            df=pd.HDFStore(f).select('df')

            if ename[-1:]=='F':
                ls='--'
            else:
                ls='-'

            #really not sure why these didn't work...
            # df.index = df.index.to_datetime()
            # df['date']=df.index
            # df['date']=[time.to_datetime() for time in df.index.tolist()]
            dates=[time.to_datetime() for time in df.index.tolist()]

            dfroll=df[sect].rolling(window=24,center=True).mean()
            ax.plot(dates,dfroll,color=colour,alpha=0.7,lw=3.5,label=ename,linestyle=ls)

            #not very helpful (I think a rolling correlation would be more interesting.)
            # dfroll=df[sect].rolling(window=24,center=True).std()
            # ax.plot(dates,dfroll,color=colour,alpha=0.9,lw=1.5,label=os.path.basename(f)[:-23],linestyle='--')

            vars=df[sect].values
            if not meanonly:
                ax.plot(dates,vars,color=colour,alpha=0.8,lw=1.5,label=ename,linestyle='-')

            ax.hlines(y=vars.mean(), xmin=dates[0], xmax=dates[-1],linewidth=1.0, color=colour, zorder=1,alpha=0.7)

            ax.set_ylabel('Transport (Sv)')

            sm.pl_inset_title_box(ax,sect,bwidth="5%",location=2)

        # ax.legend(handles, labels,loc=1)
        handles, labels = ax.get_legend_handles_labels()
        plt.figlegend( handles, labels, loc = 'lower center', ncol=6, labelspacing=0. )

    # plt.show()
    pfile=pfol+'nic_exp_one.png'
    if meanonly:
        pfile=pfol+'nic_exp_one_meanonly.png'
    
    fig.savefig(pfile,dpi=300,bbox_inches='tight')
    # fig.savefig('./.pdf',format='pdf',bbox_inches='tight')
    print pfile
    return


if __name__ == "__main__":                                     #are we being run directly?
    LogStart('',fout=False)

    ofol=ind.output_folder+'mk_mom_transport_tseries/'
    pfol=ind.plot_outputs+'mk_mom_transport_tseries/'
    sm.mkdir(ofol)
    sm.mkdir(pfol)

    # sect_dict=get_sect_local()

    # main_trans()

    pl_trans(meanonly=True)
    pl_trans(meanonly=False)


    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
