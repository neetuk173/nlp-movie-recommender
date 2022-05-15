#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt



data = pd.read_csv('hulu_titles.csv')
data.head()

data.columns[data.isna().any()].tolist() #intermediary steps

data[data.columns[data.isnull().any()]].isnull().sum() * 100 / data.shape[0] #intermediary steps

data.columns #intermediary steps

data.listed_in.value_counts() #intermediary steps

categories = ", ".join(data['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
counter_list #intermediary steps

Genres = pd.DataFrame(counter_list, columns=['Genre', 'Genre_count'])
top_10_genres = Genres.head(10)
top_10_genres #intermediary steps

data.info() #intermediary steps

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english') #need to ensure we don't come across stop words

tfidf_matrix = tfidf.fit_transform(data['listed_in']) #I chose listed in to recommed similarly genred works
tfidf_matrix.shape #the matrix we will use for our recommendations 

from sklearn.metrics.pairwise import linear_kernel 
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #recommendation algorithm

indices = pd.Series(data.index, index=data['title']).drop_duplicates() #intermediary steps

#np.save('cosine_sim2', cosine_sim)
#indices.to_pickle("indices.pkl")
#data.to_pickle("data.pkl")

#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = indices[title]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:11]

    show_indices = [i[0] for i in scores]
    result = data['title'].iloc[show_indices]
    return result.values


""" 
recs('Settlers') #testing

print(recs('The Bachelorette')) #testing

recs('Demon Slayer Kimetsu No Yaiba') #testing

recs('Signs')#testing
 """