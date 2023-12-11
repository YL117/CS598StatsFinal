from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
from dash.exceptions import PreventUpdate
import lib

g_p2_movie_table_id = 'table_score_info'
g_p2_score_table_id = 'table_score_assignment'
g_p2_recommmendation_table_id = 'table_score_recommendation'
g_p2_store_id = 'store_movie_ids'
g_p2_button_id = 'get_recommendation_button'
g_p2_review_count = 6

def get_p2_components():
    movie_ids = lib.get_random_elements(lib.g_movieIDs, g_p2_review_count)
    # print(movie_ids)
    movie_data = lib.g_movies[lib.g_movies['id'].isin(movie_ids)].drop('id',axis=1).to_dict(orient='records')
    # print(movie_data)
    components = html.Div(id = 'div_p2', children=[
        html.Div([
            html.Div([
                dash_table.DataTable(id=g_p2_movie_table_id,
                            data=movie_data,
                            columns=[{'name':'Movie', 'id':'name'},
                                    {'name':'Genre', 'id':'genres'}])],
                style={'width': '500px', 'display': 'inline-block', 'padding':'10px'}),
            
            html.Div([
                dash_table.DataTable(id=g_p2_score_table_id,
                                data=[{'review':''}] * g_p2_review_count,
                                columns=[{'name':'Review', 'id':'review'}],
                                editable=True)],
                style={'width': '100px', 'display': 'inline-block', 'padding':'20px'}),
            html.Button(id=g_p2_button_id, children=['Get Recommendations'],
                        style={'width': '150px', 'text_align':'center',
                               'height': '30%', 'display': 'inline-block', 'padding':'10px',
                               'vertical-align':'bottom',
                               'margin-left':'auto','margin-right':'auto'})
        ], style={'position':'absolute', 'top':'10px', 'margin': '10px'}),
        html.Div([
            dash_table.DataTable(id=g_p2_recommmendation_table_id,
                             columns=[{'name':'Movie', 'id':'name'},
                                      {'name':'Genre', 'id':'genres'}])],
                                      style={'position':'absolute', 'top':'250px',
                                             'width':'600px', 'margin':'20px'}),
        dcc.Store(id=g_p2_store_id, storage_type='session', data=movie_ids)
    ])
    return components

def register_p2_callbacks(app):
    @app.callback(
        Output(g_p2_recommmendation_table_id, 'data'),
        Input(g_p2_button_id, 'n_clicks'),
        [State(g_p2_score_table_id, 'data'),
         State(g_p2_store_id, 'data')]
    )
    def update_recommendation(n_clicks, scores, sampled_ids):
        if n_clicks == None:
            raise PreventUpdate()
        # print(scores)
        # print(sampled_ids)
        review_dict = {}
        for i in range(g_p2_review_count):
            score_str = scores[i]['review']
            if score_str == None or score_str == '':
                continue
            try:
                score_i = float(score_str)
            except:
                continue
            if score_i < 0.0:
                continue
            review_dict[sampled_ids[i]] = score_i
        # print(review_dict)
        if len(review_dict.keys()) <= 0:
            return None
        user = lib.make_vector(review_dict, lib.g_movieIDs)
        # print(user)
        _, indexes = lib.myIBCF(user, lib.g_S.to_numpy())
        # print(indexes)
        movie_ids = [lib.g_movieIDs[i] for i in indexes]
        return lib.g_movies[lib.g_movies['id'].isin(movie_ids)].drop('id',axis=1).to_dict(orient='records')
