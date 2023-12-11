import plotly
from dash import Dash, html, Input, Output, callback, callback_context
from dash.exceptions import PreventUpdate
import lib
import pageI
import pageII

g_switcher_p1_id = 'switch_button_p1'
g_switcher_p2_id = 'switch_button_p2'
g_main_div_left = 'div_l'
g_main_div_right = 'div_r'

# css_switcher_p1 = html.Style('''
# #switch_button_p1{
#     height:20%
#     text-align: center
# }
# #switch_button_p1:hover{
#     background-color: orange
# }
# ''')

# css_switcher_p2 = html.Style('''
# #switch_button_p1{
#     height:20%
#     text-align: center
# }
# #switch_button_p1:hover{
#     background-color: cyan
# }
# ''')

def register_visiblity_callbacks(app):
    pass
    @app.callback(
        [Output('div_p1', 'style'),
         Output('div_p2', 'style')],
        [Input(g_switcher_p1_id, 'n_clicks'),
         Input(g_switcher_p2_id, 'n_clicks')]
    )
    def change_p1_hover(clickI, clickII):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate()
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == g_switcher_p1_id:
            return ({'visibility':'visible', 'display':'block',},
                    {'visibility':'hidden', 'display':'block',
                     'pointer-event':'none','user-select':'none'})
        if button_id == g_switcher_p2_id:
            return ({'visibility':'hidden', 'display':'block',
                     'pointer-event':'none','user-select':'none'},
                    {'visibility':'visible', 'display':'block'})
    
    # @app.callback(
    #     [Output('div_p1', 'disabled'),
    #      Output('div_p1', 'style'),
    #      Output('div_p2', 'disabled'),
    #      Output('div_p2', 'style')],
    #     Input(g_switcher_p1_id, 'n_clicks')
    # )
    # def change_p1_hover(hover):
    #     if hover == None:
    #         raise PreventUpdate()
    #     return (False, {'visibility':'hidden', 'display':'block'},
    #             True, {'visibility':'visible', 'display':'block'})
        

if __name__ == '__main__':
    
    app = Dash(__name__)

    lib.load_tables()
    
    p1 = pageI.get_p1_components()
    pageI.register_p1_callback(app)
    p1.style = {'visibility':'visible', 'display':'block'}

    p2 = pageII.get_p2_components()
    pageII.register_p2_callbacks(app)
    p2.style = {'visibility':'hidden', 'display':'block', 'pointer-event':'none','user-select':'none'}

    ButtonI = html.Div(id=g_switcher_p1_id, children=['Recommendation By Genre'],
                          style={'height':'200px', 'text-align':'center', 'vertical-align':'middle'})
    ButtonII = html.Div(id=g_switcher_p2_id, children=['Recommendation By User Input'],
                          style={'height':'200px', 'text-align':'center', 'vertical-align':'middle'})
    register_visiblity_callbacks(app)

    Div_left = html.Div(id=g_main_div_left, children=[ButtonI, ButtonII],
                        style={'width':'20%', 'background-color': 'lightgray', 'top':'10%', 'float':'left', 'display':'inline-block'})
    
    Div_right= html.Div(id=g_main_div_right, children=[p1, p2],
                        style={'width':'80%', 'background-color': 'darkgray', 'top':'10%',
                               'height':'650px', 'float':'right', 'display':'inline-block'})

    app.layout = html.Div([Div_left,Div_right], id='div_main')

    app.run(host='0.0.0.0', debug=False)
