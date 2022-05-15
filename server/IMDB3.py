import numpy as np
import pandas as pd
import pickle
import json
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

cosine_sim3 = np.load('cosine_sim2.npy')
sr_indices = pd.read_pickle("indices.pkl")
sr_movie_df = pd.read_pickle("movie_df.pkl")

def get_recommendations(title, cosine_sim):
    idx = sr_indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    movie_similarity = [i[1] for i in sim_scores]
    reco_result = pd.DataFrame(zip(sr_movie_df['title'].iloc[movie_indices]), columns=["title"])
    return reco_result["title"]




hulu_cosine_sim = np.load('hulu_cosine_sim.npy')
hulu_indices = pd.read_pickle("hulu_indices.pkl")
hulu_data = pd.read_pickle("hulu_data.pkl")

def recs(title):
    idx = hulu_indices[title]
    scores = list(enumerate(hulu_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:11]

    show_indices = [i[0] for i in scores]
    result = hulu_data['title'].iloc[show_indices]
    return result.values.tolist()
    #return 123





app = FastAPI(
    title='Movie Stream',
    description='Movie recommendation service',
    docs_url='/'
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/imdb/{movie_id}")
async def getimdb(movie_id):
    output = get_recommendations(movie_id, cosine_sim3)
    #output = movie_id
    return output


@app.get("/hulu/{movie_id}")
async def gethulu(movie_id):
    output = recs(movie_id)
    return output


if __name__ == '__main__':
    uvicorn.run(app)
