#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:28:16 2019

@author: zbi.zi
"""

#%%
#settings

import pingouin as pg
import pandas as pd
import scipy as sci
import numpy as np
import csv
import os

#os.chdir('C:\Users\Monik\Downloads\stats_par')

#%%
#load data
#dt = pd.read_csv('alcohol_results_complete_09_07_2019.csv', index_col=0)

dt = pd.read_csv('alcohol_aggregated.csv', index_col=0)

dt = dt.sort_values(by='idx', ascending=True)
dt = dt.reset_index(drop=True)

#decode data
groups = {0: 'HD', 1: 'CR', 2: 'AR', 3: 'NC'}
cases = {28: 'A1', 39: 'W1', 40: 'A2', 41: 'A5', 42: 'W3', 43: 'A7', 44: 'A8',
         45: 'A9', 46: 'W4', 47: 'W5', 48: 'A10', 49: 'A11', 50: 'A12',
         51: 'A13', 52: 'A14', 53: 'A15', 54: 'A16', 55: 'A17', 56: 'A18',
         57: 'W2'}

dt['group_id'].replace(to_replace=groups, inplace=True)
dt['case_id'].replace(to_replace=cases, inplace=True)

#select subset of ROIs
dt_out = dt.where(dt['L5'] == '>').dropna().index
dt.drop(index=dt_out, axis=0, inplace=True)

#remove inconsistent ROIs
dt_out = dt['idx'].value_counts()
dt_out = dt_out.where(dt_out < 20).dropna()
dt_out = list(dt_out.index.values)

for l in dt_out:
    l_idx = dt.where(dt['idx'] == l).dropna().index
    dt.drop(index=l_idx, axis=0, inplace=True)

#split data by groups
dt_NC = dt[dt['group_id'] == 'NC']
dt_NC = dt_NC.dropna()
dt_HD = dt[dt['group_id'] == 'HD']
dt_HD = dt_HD.dropna()
dt_CR = dt[dt['group_id'] == 'CR']
dt_CR = dt_CR.dropna()
dt_AR = dt[dt['group_id'] == 'AR']
dt_AR = dt_AR.dropna()

#find inconsistent labels
NCHD_diff = list(set(dt_NC['idx']).symmetric_difference(set(dt_HD['idx'])))
NCCR_diff = list(set(dt_NC['idx']).symmetric_difference(set(dt_CR['idx'])))
NCAR_diff = list(set(dt_NC['idx']).symmetric_difference(set(dt_AR['idx'])))
HDCR_diff = list(set(dt_HD['idx']).symmetric_difference(set(dt_CR['idx'])))
HDAR_diff = list(set(dt_HD['idx']).symmetric_difference(set(dt_AR['idx'])))
CRAR_diff = list(set(dt_CR['idx']).symmetric_difference(set(dt_AR['idx'])))
outs = list(set(NCHD_diff).union(set(NCCR_diff).union(set(NCAR_diff).union(set(HDCR_diff).union(set(HDAR_diff).union(set(CRAR_diff)))))))

#list ROI labels
ROI_lbs = np.unique(dt['name'])

#load & decode actual data
dt_00 = pd.read_csv('summarized_new_densities_alcohol_atlas.csv')

dt_00['case_id'].replace(to_replace=cases, inplace=True)

dt_00 = dt_00.sort_values(by='name', ascending=True)
dt_00 = dt_00.reset_index(drop=True)

dt_00_out = dt_00['name'].value_counts()
dt_00_out = dt_00_out.where(dt_00_out < 20).dropna()
dt_00_out = list(dt_00_out.index.values)

for l in dt_00_out:
    l_idx = dt.where(dt_00['name'] == l).dropna().index
    dt_00.drop(index=l_idx, axis=0, inplace=True)

#load data for ROIs
#dt_tbl_ord = ['case_id', 'group_id', 'label_id', 'name', 'signal_density']
#dt_tbl = pd.DataFrame(columns=['case_id', 'group_id', 'label_id', 'name', 'signal_density'])
dt_tbl_ord = ['case_id', 'group_label', 'depth', 'abbrev', 'name',
              'signal_density']
dt_tbl = pd.DataFrame(columns=['case_id', 'group_label', 'depth', 'abbrev',
                               'name', 'signal_density'])
dt_tbl = dt_tbl.reindex(columns=dt_tbl_ord)

for i in list(ROI_lbs):
    ROI_dt = dt_00.where(dt_00['name'] == i).dropna()
    dt_tbl = pd.concat([dt_tbl,ROI_dt],axis=0,sort=False, ignore_index=True)

#dt_tbl = dt_00

#check and remove inconsistencies
dt_NC = dt_tbl[dt_tbl['group_label'] == 'control'].dropna()
dt_HD = dt_tbl[dt_tbl['group_label'] == 'alcohol'].dropna()
dt_CR = dt_tbl[dt_tbl['group_label'] == 'cue'].dropna()
dt_AR = dt_tbl[dt_tbl['group_label'] == 'relapse'].dropna()

NCHD_diff = list(set(dt_NC['name']).symmetric_difference(set(dt_HD['name'])))
NCCR_diff = list(set(dt_NC['name']).symmetric_difference(set(dt_CR['name'])))
NCAR_diff = list(set(dt_NC['name']).symmetric_difference(set(dt_AR['name'])))
HDCR_diff = list(set(dt_HD['name']).symmetric_difference(set(dt_CR['name'])))
HDAR_diff = list(set(dt_HD['name']).symmetric_difference(set(dt_AR['name'])))
CRAR_diff = list(set(dt_CR['name']).symmetric_difference(set(dt_AR['name'])))
outs_tbl = list(set(NCHD_diff).union(set(NCCR_diff).union(set(NCAR_diff).union(set(HDCR_diff).union(set(HDAR_diff).union(set(CRAR_diff)))))))

for o in outs_tbl:
    o_lbl = dt_tbl.where(dt_tbl['name'] == o).dropna().index
    dt_tbl.drop(index=o_lbl, axis=0, inplace=True)

dt_tbl = dt_tbl.reset_index(drop=True)

dpt_out = dt_tbl.where(dt_tbl['depth'] < 5).dropna().index
dt_tbl.drop(index=dpt_out, axis=0, inplace=True)

vrbl_out = dt_tbl.where(dt_tbl['group_label'] == 'control').dropna().index
dt_tbl.drop(index=vrbl_out, axis=0, inplace=True)

dt_tbl = dt_tbl.reset_index(drop=True)


#list ROIs
ROI_nms = np.unique(dt_tbl['name'])

#dt_tabs = [dt_NC, dt_HD, dt_CR, dt_HD]
#mmxdt_tbl = [[i, j] for i in mm_labels for j in dt_tabs]

#for e in mmxdt_tbl:
#    idx = e[1].where(e[1]['label_id'] == e[0]).dropna().index
#    e[1].drop(idx, axis=0, inplace=True)

#regroup data
#dt_NCHD = pd.concat([dt_NC,dt_HD],axis=0,sort=False, ignore_index=True)
#dt_NCCR = pd.concat([dt_NC,dt_CR],axis=0,sort=False, ignore_index=True)
#dt_NCAR = pd.concat([dt_NC,dt_AR],axis=0,sort=False, ignore_index=True)
#dt_HDCR = pd.concat([dt_HD,dt_CR],axis=0,sort=False, ignore_index=True)
#dt_HDAR = pd.concat([dt_HD,dt_AR],axis=0,sort=False, ignore_index=True)
#dt_CRAR = pd.concat([dt_CR,dt_AR],axis=0,sort=False, ignore_index=True)


#%%
#analyze data

##anova

aov = pg.mixed_anova(data=dt_tbl, dv='signal_density', between='group_label',
                     within='name', subject='case_id', correction=True)
#
#export_csv = aov.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\densities_anova_all.csv',
#                       header=True)

#posthoc t-tests

#3-way

way_post_hocs = pg.pairwise_ttests(data=dt_tbl, dv='signal_density',
                                   within='name', between='group_label',
                                   subject='case_id', parametric=True,
                                   marginal=True, tail='one-sided',
                                   padjust='fdr_bh', effsize='cohen',
                                   return_desc=True)

way_ph_all = way_post_hocs.reset_index(drop=True)

#find group comparisons for every brain area

way_ph_int = way_ph_all[way_ph_all['Contrast'] == 'name * group_label']
way_ph_int = way_ph_int.reset_index(drop=True)

#reject, pvals_corr = pg.multicomp(list(way_ph_int['p-unc']), method='fdr_bh')

#select significant uncorrected

way_ph_sig_u = way_ph_int[way_ph_int['p-unc'] < 0.05].dropna()
way_ph_sig_u = way_ph_sig_u.reset_index(drop=True)

#select significant corrected for multiple comparisons

way_ph_sig_c = way_ph_int[way_ph_int['p-corr'] < 0.05].dropna()
way_ph_sig_c = way_ph_sig_c.reset_index(drop=True)

#save to csv

export_csv = way_ph_all.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\3way_densities_1sidettests_res_all.csv',
                                header=True)

export_csv = way_ph_int.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\3way_densities_1sidettests_res_int.csv',
                              header=True)

export_csv = way_ph_sig_u.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\3way_densities_1sidettests_res_sig_c.csv',
                                 header=True)

export_csv = way_ph_sig_c.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\3way_densities_1sidettests_res_sig_c.csv',
                                 header=True)

##alcohol vs relapse
#
#CR_out = dt_tbl.where(dt_tbl['group_label'] == 'cue').dropna().index
#HDAR_tbl = dt_tbl.drop(index=CR_out, axis=0)
#HDAR_tbl = HDAR_tbl.reset_index(drop=True)
#
#HDAR_post_hocs = pg.pairwise_ttests(data=HDAR_tbl, dv='signal_density',
#                                    within='name', between='group_label',
#                                    subject='case_id', parametric=True,
#                                    marginal=True, tail='two-sided',
#                                    padjust='fdr_bh', effsize='cohen',
#                                    return_desc=True)
#
#HDAR_ph_all = HDAR_post_hocs.reset_index(drop=True)
#
#HDAR_ph_int = HDAR_ph_all[HDAR_ph_all['Contrast'] == 'name * group_label']
#HDAR_ph_int = HDAR_ph_int.reset_index(drop=True)
#
#HDAR_ph_sig = HDAR_ph_int[HDAR_ph_int['p-corr'] < 0.05].dropna()
#HDAR_ph_sig = HDAR_ph_sig.reset_index(drop=True)
#
#export_csv = HDAR_ph_all.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDAR_densities_ttests_res_int.csv',
#                                header=True)
#
#export_csv = HDAR_ph_int.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDAR_densities_ttests_res_all.csv',
#                              header=True)
#
#export_csv = HDAR_ph_sig.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDAR_densities_ttests_res_sig.csv',
#                           header=True)
#
##alcohol vs cue
#
#AR_out = dt_tbl.where(dt_tbl['group_label'] == 'relapse').dropna().index
#HDCR_tbl = dt_tbl.drop(index=AR_out, axis=0)
#HDCR_tbl = HDCR_tbl.reset_index(drop=True)
#
#HDCR_post_hocs = pg.pairwise_ttests(data=HDCR_tbl, dv='signal_density',
#                                    within='name', between='group_label',
#                                    subject='case_id', parametric=True,
#                                    marginal=True, tail='two-sided',
#                                    padjust='fdr_bh', effsize='cohen',
#                                    return_desc=True)
#
#HDCR_ph_all = HDCR_post_hocs.reset_index(drop=True)
#
#HDCR_ph_int = HDCR_ph_all[HDCR_ph_all['Contrast'] == 'name * group_label']
#HDCR_ph_int = HDCR_ph_int.reset_index(drop=True)
#
#HDCR_ph_sig = HDCR_ph_int[HDCR_ph_int['p-corr'] < 0.05].dropna()
#HDCR_ph_sig = HDCR_ph_sig.reset_index(drop=True)
#
#export_csv = HDCR_ph_all.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDCR_densities_ttests_res_int.csv',
#                                header=True)
#
#export_csv = HDCR_ph_int.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDCR_densities_ttests_res_all.csv',
#                              header=True)
#
#export_csv = HDCR_ph_sig.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\HDCR_densities_ttests_res_sig.csv',
#                           header=True)
#
##relapse vs cue
#
#HD_out = dt_tbl.where(dt_tbl['group_label'] == 'alcohol').dropna().index
#ARCR_tbl = dt_tbl.drop(index=HD_out, axis=0)
#ARCR_tbl = ARCR_tbl.reset_index(drop=True)
#
#ARCR_post_hocs = pg.pairwise_ttests(data=ARCR_tbl, dv='signal_density',
#                                    within='name', between='group_label',
#                                    subject='case_id', parametric=True,
#                                    marginal=True, tail='two-sided',
#                                    padjust='fdr_bh', effsize='cohen',
#                                    return_desc=True)
#
#ARCR_ph_all = ARCR_post_hocs.reset_index(drop=True)
#
#ARCR_ph_int = ARCR_ph_all[ARCR_ph_all['Contrast'] == 'name * group_label']
#ARCR_ph_int = ARCR_ph_int.reset_index(drop=True)
#
#ARCR_ph_sig = ARCR_ph_int[ARCR_ph_int['p-corr'] < 0.05].dropna()
#ARCR_ph_sig = ARCR_ph_sig.reset_index(drop=True)
#
#export_csv = ARCR_ph_all.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\ARCR_densities_ttests_res_int.csv',
#                                header=True)
#
#export_csv = ARCR_ph_int.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\ARCR_densities_ttests_res_all.csv',
#                              header=True)
#
#export_csv = ARCR_ph_sig.to_csv(r'E:\zbizieli\Processing\MDID_NI\an_results\ARCR_densities_ttests_res_sig.csv',
#                           header=True)
