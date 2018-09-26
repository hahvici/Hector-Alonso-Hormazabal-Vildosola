# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 02:17:12 2018

@author: Alonso
"""

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from statsmodels.graphics import tsaplots

def label(ax, string):
    ax.annotate(string,(1, 1),xytext=(-8,-8),ha='right', va='top',
                size=14, xycoords='axes fraction', textcoords='offset points')

np.random.seed(1977)
data = np.random.normal(0, 1, 100).cumsum()

fig, axes = plt.subplots(nrows=4, figsize=(8, 12))
fig.tight_layout()

axes[0].plot(data)
label(axes[0], 'Raw Data')

axes[1].acorr(data, maxlags=data.size-1)
label(axes[1], 'Matplotlib Autocorrelation')

tsaplots.plot_acf(data, axes[2])
label(axes[2], 'Statsmodels Autocorrelation')

pd.tools.plotting.autocorrelation_plot(data, ax=axes[3])
label(axes[3], 'Pandas Autocorrelation')

# Remove some of the titles and labels that were automatically added
for ax in axes.flat:
    ax.set(title='', xlabel='')
plt.show()