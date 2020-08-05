# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:17:35 2020

@author: Monika Pawłowska, Zbigniew Zieliński
"""

import pingouin as pg
import pandas as pd

#%% loading
#dane = pd.read_csv('alcohol_depth5_remove0.csv')
dane_lvl6 = pd.read_csv('alcohol_depth6_with_cat.csv')

#%% cleanup. More than one value per group needed for calculating Standard Deviation
dane=dane_lvl6
counts=dane.groupby([ 'group_label', 'abbrev']).agg(['count'])
counts.columns = ["_".join(x) for x in counts.columns.ravel()]
to_remove=counts[counts['signal_density_count']<=1]
to_remove.reset_index(inplace=True)

dane=dane[~dane.abbrev.isin(to_remove['abbrev'].to_list())]

#%% pairwise t tests
#see https://pingouin-stats.org/generated/pingouin.pairwise_ttests.html#pingouin.pairwise_ttests
post_hocs_2sided_6 = pg.pairwise_ttests(data=dane, 
                                      dv='signal_density',
                                      within='abbrev', 
                                      between='group_label',
                                      subject='case_id', 
                                      parametric=True,
                                      marginal=True, 
                                      tail='two-sided',
                                      padjust='fdr_bh', 
                                      effsize='cohen',
                                      return_desc=True)

post_hocs_2_6 = post_hocs_2sided_6[post_hocs_2sided_6['Contrast'] == 'abbrev * group_label'].reset_index(drop=True)

#%% saving

export_csv = post_hocs_2_6.to_csv('pairwise_2sided_depth6.csv', header=True)
