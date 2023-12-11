import pandas as pd
import numpy as np

g_S: pd.DataFrame | None = None
g_genreRecommendations: pd.DataFrame | None = None
g_movies: pd.DataFrame | None = None
g_movieIDs: list[str] | None = None
g_genres: list[str] | None = None
g_rng = None

def load_tables():
    global g_S
    global g_genreRecommendations
    global g_movies
    global g_movieIDs
    global g_genres
    global g_rng
    if g_S == None:
        g_S = pd.read_csv('S_reduced.csv', index_col=0, sep=',', na_values=['NA'])
    if g_genreRecommendations == None:
        g_genreRecommendations = pd.read_csv('GenreRecom.csv', index_col=None)
    if g_movies == None:
        g_movies = pd.read_csv('movies.dat', sep='::',
                               names=['id','name','genres'], encoding='latin1',
                               header=None, index_col=None)
        g_movies['id'] = g_movies['id'].map(lambda x: 'm' + str(x))
    if g_movieIDs == None:
        g_movieIDs = g_S.columns.to_list()
    if g_genres == None:
        g_genres = g_genreRecommendations.columns.to_list()
    if g_rng == None:
        g_rng = np.random.default_rng()

def get_random_elements(list_, count = 10):
    global g_rng
    n = len(list_)
    indexes = np.arange(n, dtype=int)
    g_rng.shuffle(indexes)
    elements = []
    for i in range(count):
        elements.append(list_[indexes[i]])
    return elements

def make_vector(user_dict: dict, movie_ids: list[str]):
    n = len(movie_ids)
    user = np.zeros(n) + np.nan
    for id, review in user_dict.items():
        user[movie_ids.index(id)] = review
    if np.logical_not(np.isnan(user)).all():
        return None
    return user

def myIBCF(newuser: np.array, S_):
    assert newuser.shape[0] == S_.shape[0]
    assert S_.shape[0] == S_.shape[1]
    # cols = S_df.columns.to_list()

    scores = -np.ones(newuser.shape[0]) * np.inf
    for i in range(newuser.shape[0]):
        valid_row_index = np.arange(newuser.shape[0],dtype=int)[np.logical_not(np.isnan(S_[i,:]))]
        assert len(valid_row_index) <= 30
        # if len(valid_row_index) < 30:
        #     print('row ', i, ', fewer than 30', len(valid_row_index))
        nominator = 0.0
        denominator = 0.0
        for j in valid_row_index:
            if not np.isnan(newuser[j]):
                nominator += S_[i, j] * newuser[j]
                denominator += S_[i, j]
        if denominator != 0.0:
            scores[i] = nominator / denominator

    # S_nona = np.where(np.isnan(S_), 0, S_)
    # newuser_nona = np.where(np.isnan(newuser), 0, newuser)
    # nominator = np.matmul(S_nona, newuser_nona)
    # newuser_isna = np.where(np.isnan(newuser),0,1)
    # denominator = np.matmul(S_nona, newuser_isna)
    # scores = np.where(denominator != 0, nominator / denominator, -1)

    return (scores[np.argsort(scores)[::-1][0:10]], np.argsort(scores)[::-1][0:10])
