#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


# In[4]:


data = pd.read_csv('disney_plus_titles.csv')
data.head()


# In[5]:


data.columns[data.isna().any()].tolist() #intermediary steps


# In[6]:


data[data.columns[data.isnull().any()]].isnull().sum() * 100 / data.shape[0] #intermediary steps


# In[7]:


data.columns #intermediary steps


# In[8]:


data.listed_in.value_counts() #intermediary steps


# In[9]:


categories = ", ".join(data['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
counter_list #intermediary steps


# In[10]:


Genres = pd.DataFrame(counter_list, columns=['Genre', 'Genre_count'])
top_10_genres = Genres.head(10)
top_10_genres #intermediary steps


# In[11]:


data.info() #intermediary steps


# In[12]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english') #need to ensure we don't come across stop words


# In[13]:


tfidf_matrix = tfidf.fit_transform(data['listed_in']) #I chose listed in to recommed similarly genred works
tfidf_matrix.shape #the matrix we will use for our recommendations 


# In[14]:


from sklearn.metrics.pairwise import linear_kernel 
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #recommendation algorithm


indices = pd.Series(data.index, index=data['title']).drop_duplicates() #intermediary steps

""" indices.to_pickle("disney_indices.pkl")
data.to_pickle("disney_data.pkl")
np.save('disney_cosine_sim', cosine_sim) """

disney_cosine_sim = np.load('disney_cosine_sim.npy')
disney_indices = pd.read_pickle("disney_indices.pkl")
disney_data = pd.read_pickle("disney_data.pkl")

#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = disney_indices[title]
    scores = list(enumerate(disney_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    return disney_data['title'].iloc[show_indices]


# In[23]:


recs('Feast') #testing


# In[24]:


recs('Get a Horse!') #testing


# In[25]:


recs('Planes') #testing


# In[26]:


recs('Spin')#testing


# In[29]:


print(recs('Gus'))#testing


# In[ ]:




