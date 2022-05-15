#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[3]:


import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


# In[4]:


data = pd.read_csv('netflix_titles.csv')
data.head()


# In[5]:


data.columns[data.isna().any()].tolist() #intermediary steps


# In[6]:


data[data.columns[data.isnull().any()]].isnull().sum() * 100 / data.shape[0] #intermediary steps


# In[7]:


data.columns #intermediary steps


# In[8]:


data.isna().any()


# In[9]:


data["director"] = data.director.fillna("null")
data["cast"] = data.cast.fillna("null")
data["country"] = data.country.fillna("null")
data["date_added"] = data.date_added.fillna("null")
data["rating"] = data.rating.fillna("null")
data["duration"] = data.duration.fillna("null")


# In[10]:


data.listed_in.value_counts() #intermediary steps


# In[11]:


categories = ", ".join(data['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
counter_list #intermediary steps


# In[12]:


Genres = pd.DataFrame(counter_list, columns=['Genre', 'Genre_count'])
top_10_genres = Genres.head(10)
top_10_genres #intermediary steps


# In[13]:


data.info() #intermediary steps


# In[14]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english') #need to ensure we don't come across stop words


# In[15]:


tfidf_matrix = tfidf.fit_transform(data['listed_in']) #I chose listed in to recommed similarly genred works
tfidf_matrix.shape #the matrix we will use for our recommendations 


# In[16]:


from sklearn.metrics.pairwise import linear_kernel 
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #recommendation algorithm


# In[17]:


indices = pd.Series(data.index, index=data['title']).drop_duplicates() #intermediary steps


# In[18]:
indices.to_pickle("netflix_indices.pkl")
data.to_pickle("netflix_data.pkl")
np.save('netflix_cosine_sim', cosine_sim)

#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = indices[title]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    return data['title'].iloc[show_indices]


# In[19]:


recs('Midnight Mass') #testing


# In[20]:


print(recs('Sankofa')) #testing


# In[21]:


recs("Europe's Most Dangerous Man: Otto Skorzeny in Spain") #testing


# In[22]:


recs('Jaws')#testing


# In[ ]:




