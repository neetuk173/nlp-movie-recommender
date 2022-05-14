#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install ruamel-yaml


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


# In[5]:


data = pd.read_csv('hulu_titles.csv')
data.head()


# In[6]:


data.columns[data.isna().any()].tolist() #intermediary steps


# In[7]:


data[data.columns[data.isnull().any()]].isnull().sum() * 100 / data.shape[0] #intermediary steps


# In[8]:


data.columns #intermediary steps


# In[9]:


data.listed_in.value_counts() #intermediary steps


# In[10]:


categories = ", ".join(data['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
counter_list #intermediary steps


# In[11]:


Genres = pd.DataFrame(counter_list, columns=['Genre', 'Genre_count'])
top_10_genres = Genres.head(10)
top_10_genres #intermediary steps


# In[12]:


data.info() #intermediary steps


# In[13]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english') #need to ensure we don't come across stop words


# In[14]:


tfidf_matrix = tfidf.fit_transform(data['listed_in']) #I chose listed in to recommed similarly genred works
tfidf_matrix.shape #the matrix we will use for our recommendations 


# In[15]:


from sklearn.metrics.pairwise import linear_kernel 
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #recommendation algorithm


# In[16]:


indices = pd.Series(data.index, index=data['title']).drop_duplicates() #intermediary steps


# In[17]:


#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = indices[title]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:11]

    show_indices = [i[0] for i in scores]
    return data['title'].iloc[show_indices]


# In[18]:


recs('Settlers') #testing


# In[19]:


recs('The Bachelorette') #testing


# In[20]:


recs('Demon Slayer Kimetsu No Yaiba') #testing


# In[27]:


recs('Signs')#testing


# In[ ]:




