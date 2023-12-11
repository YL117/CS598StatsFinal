from dash import Dash, html, dcc, Input, Output, callback, dash_table
import lib

g_p1_dropdown_id = 'dropdown_genres'
g_p1_table_id = 'table_genre_recommendations'

def get_p1_components():
    components = html.Div([
        html.Div(['Select Genre'], style={'width': '150px', 'margin': '20px',
                                          'top':'30px', 'text-align':'center',
                                          'background-color': 'lightgray'}),
        dcc.Dropdown(id=g_p1_dropdown_id, searchable=True, options=lib.g_genres, value=None,
                     style={'width':'250px', 'margin':'10px'}),
        html.Div([dash_table.DataTable(id=g_p1_table_id, columns=[{'name':'Movie', 'id':'name'},
                                                        {'name':'Genre', 'id':'genres'}])],
                                                        style={'position':'absolute', 'width':'600px',
                                                               'margin':'10px', 'top':'300px'})
    ], id = 'div_p1')
    return components

def register_p1_callback(app):
    @app.callback(
        Output(g_p1_table_id, 'data'),
        Input(g_p1_dropdown_id, 'value')
    )
    def update_p1_table(genre: str):
        if genre == None or genre == '' or genre not in lib.g_genres:
            return None
        movie_ids = lib.g_genreRecommendations[genre].to_list()
        # print(movie_ids)
        # print(lib.g_movies[lib.g_movies['id'].isin(movie_ids)].drop('id',axis=1))
        # print(lib.g_movies.head)
        return lib.g_movies[lib.g_movies['id'].isin(movie_ids)].drop('id',axis=1).to_dict(orient='records')

