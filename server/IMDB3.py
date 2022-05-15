import numpy as np
import pandas as pd
import pickle
import json
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

cosine_sim3 = np.load('binaries/cosine_sim2.npy')
sr_indices = pd.read_pickle("binaries/indices.pkl")
sr_movie_df = pd.read_pickle("binaries/movie_df.pkl")

def get_recommendations(title, cosine_sim):
    idx = sr_indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    movie_similarity = [i[1] for i in sim_scores]
    reco_result = pd.DataFrame(zip(sr_movie_df['title'].iloc[movie_indices]), columns=["title"])
    return reco_result["title"]




hulu_cosine_sim = np.load('binaries/hulu_cosine_sim.npy')
hulu_indices = pd.read_pickle("binaries/hulu_indices.pkl")
hulu_data = pd.read_pickle("binaries/hulu_data.pkl")

def hulurecs(title):
    idx = hulu_indices[title]
    scores = list(enumerate(hulu_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:11]

    show_indices = [i[0] for i in scores]
    result = hulu_data['title'].iloc[show_indices]
    return result.values.tolist()
    #return 123



disney_cosine_sim = np.load('binaries/disney_cosine_sim.npy')
disney_indices = pd.read_pickle("binaries/disney_indices.pkl")
disney_data = pd.read_pickle("binaries/disney_data.pkl")

#here we will build the recommendation function itself. We will call this with an existing title.
def disneyrecs(title):
    idx = disney_indices[title]
    scores = list(enumerate(disney_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    result = disney_data['title'].iloc[show_indices]
    return result.values.tolist()



amazon_cosine_sim = np.load('binaries/amazon_cosine_sim.npy')
amazon_indices = pd.read_pickle("binaries/amazon_indices.pkl")
amazon_data = pd.read_pickle("binaries/amazon_data.pkl")


#here we will build the recommendation function itself. We will call this with an existing title.
def amazonrecs(title):
    idx = amazon_indices[title]
    scores = list(enumerate(amazon_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    result = amazon_data['title'].iloc[show_indices]
    return result.values.tolist()



netflix_cosine_sim = np.load('binaries/netflix_cosine_sim.npy')
netflix_indices = pd.read_pickle("binaries/netflix_indices.pkl")
netflix_data = pd.read_pickle("binaries/netflix_data.pkl")


#here we will build the recommendation function itself. We will call this with an existing title.
def netflixrecs(title):
    idx = netflix_indices[title]
    scores = list(enumerate(netflix_cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    scores = scores[1:6]

    show_indices = [i[0] for i in scores]
    result = netflix_data['title'].iloc[show_indices]
    return result.values.tolist()



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
    output = hulurecs(movie_id)
    return output


@app.get("/disney/{movie_id}")
async def getdisney(movie_id):
    output = disneyrecs(movie_id)
    return output


@app.get("/amazon/{movie_id}")
async def getamazon(movie_id):
    output = amazonrecs(movie_id)
    return output


@app.get("/netflix/{movie_id}")
async def getnetflix(movie_id):
    output = netflixrecs(movie_id)
    return output


if __name__ == '__main__':
    uvicorn.run(app)
