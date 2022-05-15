#!/usr/bin/env python
# coding: utf-8

# In[21]:


# In[23]:


import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


# In[24]:


data = pd.read_csv('amazon_prime_titles.csv')
data.head()


# In[25]:


data.columns[data.isna().any()].tolist() #intermediary steps


# In[26]:


data.isna().any()


# In[27]:


data["director"] = data.director.fillna("null")
data["cast"] = data.cast.fillna("null")
data["country"] = data.country.fillna("null")
data["date_added"] = data.date_added.fillna("null")
data["rating"] = data.rating.fillna("null")
data["duration"] = data.duration.fillna("null")


# In[28]:


data.isna().any()


# In[29]:


data[data.columns[data.isnull().any()]].isnull().sum() * 100 / data.shape[0] #intermediary steps


# In[30]:


data.columns #intermediary steps


# In[31]:


data.listed_in.value_counts() #intermediary steps


# In[32]:


categories = ", ".join(data['listed_in']).split(", ")
counter_list = Counter(categories).most_common(50)
counter_list #intermediary steps


# In[33]:


Genres = pd.DataFrame(counter_list, columns=['Genre', 'Genre_count'])
top_10_genres = Genres.head(10)
top_10_genres #intermediary steps


# In[34]:


data.info() #intermediary steps


# In[35]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english') #need to ensure we don't come across stop words


# In[36]:


tfidf_matrix = tfidf.fit_transform(data['listed_in']) #I chose listed in to recommed similarly genred works
tfidf_matrix.shape #the matrix we will use for our recommendations 


# In[37]:


from sklearn.metrics.pairwise import linear_kernel 
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) #recommendation algorithm


# In[38]:


indices = pd.Series(data.index, index=data['title']).drop_duplicates() #intermediary steps


# In[39]:

indices.to_pickle("amazon_indices.pkl")
data.to_pickle("amazon_data.pkl")
np.save('amazon_cosine_sim', cosine_sim)


#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = indices[title]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    return data['title'].iloc[show_indices]


# In[40]:


print(recs('Pink: Staying True')) #testing


# In[41]:


recs('Hired Gun') #testing


# In[42]:


recs("Zoombies") #testing


# In[43]:


recs('Yoga to Break Any Habit')#testing


# In[ ]:




