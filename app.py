import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Create the data dictionary
data = {
    'Year': [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 
             1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],

    'Winner': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'West Germany', 'Brazil', 
               'Brazil', 'England', 'Brazil', 'West Germany', 'Argentina', 'Italy', 
               'Argentina', 'West Germany', 'Brazil', 'France', 'Brazil', 'Italy', 
               'Spain', 'Germany', 'France', 'Argentina'],

    'Runner-Up': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 
                  'Czechoslovakia', 'West Germany', 'Italy', 'Netherlands', 'Netherlands', 
                  'West Germany', 'West Germany', 'Argentina', 'Italy', 'Brazil', 'Germany', 
                  'France', 'Netherlands', 'Argentina', 'Croatia', 'France'],

    'Score': ['4-2', '2-1', '4-2', '2-1', '3-2', '5-2', '3-1', '4-2', '4-1', '2-1', 
              '3-1', '3-1', '3-2', '1-0', '0-0 (3-2 pen)', '3-0', '2-0', '1-1 (5-3 pen)', 
              '1-0', '1-0', '4-2', '3-3 (4-2 pen)']
}

df = pd.DataFrame(data)
df['Winner_Count'] = df.groupby('Winner')['Winner'].transform('count')

app = Dash(__name__)
server = app.server  

app.layout = html.Div([
    html.H1("FIFA World Cup Finals Dashboard A7", style={'textAlign': 'center'}),
    html.P("View the history of FIFA World Cup winners and runner-ups from 1930 to 2022.", 
           style={'textAlign': 'center', 'fontSize': '16px', 'marginBottom': '20px'}),

    html.H3("World Cup Winners Map"),
    html.P("This map shows the countries that have won the World Cup."),
    dcc.Graph(id='world-map'),

    html.H3("Select a Country to View Wins"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['Winner'].unique()],
        value='Brazil',
        clearable=False
    ),
    
    html.Div(id='country-info', style={'fontSize': '18px', 'marginTop': '10px', 'fontWeight': 'bold'}),

    html.H3("Select a Year to View Match Details"),
    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=4,
        marks={str(year): str(year) for year in df['Year']},
        value=df['Year'].min()
    ),
    html.Div(id='year-info', style={'fontSize': '25px', 'marginTop': '25px', 'fontWeight': 'bold'})
])

# Callbacks
@app.callback(
    Output('world-map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(selected_year):
    fig = px.choropleth(
        df, 
        locations='Winner', 
        locationmode='country names',
        color='Winner_Count', 
        hover_name='Winner',
        title=f'World Cup Winners (Up to {selected_year})'
    )
    fig.update_layout(coloraxis_colorbar=dict(title="# of Wins"))
    return fig

@app.callback(
    Output('country-info', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_info(selected_country):
    wins = df[df['Winner'] == selected_country].shape[0]
    return f"{selected_country} has won the FIFA World Cup {wins} times."

@app.callback(
    Output('year-info', 'children'),
    Input('year-slider', 'value')
)
def update_year_info(selected_year):
    match = df[df['Year'] == selected_year]
    if not match.empty:
        winner = match['Winner'].values[0]
        runner_up = match['Runner-Up'].values[0]
        score = match['Score'].values[0]
        return f"In the year {selected_year}, {winner} won the final against {runner_up} with a score of {score}."
    return "No data available."

if __name__ == "__main__":
    app.run_server(debug=False)