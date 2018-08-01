#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 10:23:55 2018

@author: pradeepburugu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm

csk_data = pd.read_csv('csk.csv')

plt.figure()

hist1,edges1 = np.histogram(csk_data.viewCount)
plt.bar(edges1[:-1],hist1,width=edges1[1:]-edges1[:-1])

print(csk_data.corr())

plt.scatter(csk_data.viewCount,csk_data.likeCount)
plt.scatter(csk_data.viewCount,csk_data.dislikeCount)

y = csk_data.likeCount
X = csk_data.viewCount
X = sm.add_constant(X)

lr_model = sm.OLS(y,X).fit()

print(lr_model.summary())

X_prime=np.linspace(X.viewCount.min(),X.viewCount.max(),100)
X_prime = sm.add_constant(X_prime)

y_hat =lr_model.predict(X_prime)
plt.scatter(X.viewCount,y)
plt.xlabel("View Count")
plt.ylabel("Like Count")
plt.plot(X_prime[:,1],y_hat)