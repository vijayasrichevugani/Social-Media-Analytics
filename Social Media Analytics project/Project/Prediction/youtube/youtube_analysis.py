#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 09:48:51 2018

@author: pradeepburugu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


youtube_data = pd.read_csv('video_result.csv')

plt.figure()

hist1,edges1 = np.histogram(youtube_data.viewCount)
plt.bar(edges1[:-1],hist1,width=edges1[1:]-edges1[:-1])

print(youtube_data.corr())

plt.scatter(youtube_data.viewCount,youtube_data.likeCount)
plt.scatter(youtube_data.viewCount,youtube_data.dislikeCount)

y = youtube_data.likeCount
X = youtube_data.viewCount
X = sm.add_constant(X)

y1 = youtube_data.dislikeCount
X1 = youtube_data.viewCount
X1 = sm.add_constant(X1)



lr_model = sm.OLS(y,X).fit()
lr_model1 = sm.OLS(y1,X1).fit()


print(lr_model.summary())
print(lr_model1.summary())

X_prime=np.linspace(X.viewCount.min(),X.viewCount.max(),100)
X_prime = sm.add_constant(X_prime)

X_prime1=np.linspace(X1.viewCount.min(),X1.viewCount.max(),100)
X_prime1 = sm.add_constant(X_prime1)

y_hat =lr_model.predict(X_prime)
y_hat1 =lr_model1.predict(X_prime1)

plt.scatter(X.viewCount,y)
plt.scatter(X1.viewCount,y1)

plt.xlabel("View Count")
plt.ylabel("Like Count && Dislike Count")

plt.plot(X_prime[:,1],y_hat)
plt.plot(X_prime1[:,1],y_hat1)

