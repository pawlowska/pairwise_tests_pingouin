# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:17:35 2020

@author: Monik
"""


import pingouin as pg
import pandas as pd

#%%
demo = pd.read_csv('anxiety_demo.csv')


#%% time * group
demo_post_hocs = pg.pairwise_ttests(data=demo, dv='score',
                                   within='time', between='group',
                                   subject='id', parametric=True,
                                   marginal=True, tail='two-sided',
                                   padjust='fdr_bh', effsize='cohen',
                                   return_desc=True)

demo_ph_int =demo_post_hocs[demo_post_hocs['Contrast'] == 'time * group'].dropna().reset_index(drop=True)
