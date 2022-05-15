#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import pickle
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

hulu_cosine_sim = np.load('hulu_cosine_sim.npy')
hulu_indices = pd.read_pickle("hulu_indices.pkl")
hulu_data = pd.read_pickle("hulu_data.pkl")


#here we will build the recommendation function itself. We will call this with an existing title.
def recs(title):
    idx = hulu_indices[title]
    scores = list(enumerate(hulu_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:11]

    show_indices = [i[0] for i in scores]
    result = hulu_data['title'].iloc[show_indices]
    return result.values.tolist()



recs('Settlers') #testing

print(recs('The Bachelorette')) #testing

recs('Demon Slayer Kimetsu No Yaiba') #testing

recs('Signs')#testing
