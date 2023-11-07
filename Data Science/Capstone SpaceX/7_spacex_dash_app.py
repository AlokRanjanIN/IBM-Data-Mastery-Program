# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label': 'Select a Launch Site here', 'value': 'placeholder', 'disabled': True},
                                                     {'label': 'All Sites', 'value': 'ALL'}]
                                                    +
                                                    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                            
                                            value='ALL' # The default select value is for All Sites
                                           ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                               min=0,
                                               max=10000,
                                               step=1000,
                                               value=[min_payload,max_payload]
                                              ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div([],id='success-payload-scatter-chart'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback([Output(component_id='success-pie-chart',component_property='children')],
              [Input(component_id='site-dropdown',component_property='value')]
             )
def pie_chart (site):
    if site=='ALL':
        pie_fig=px.pie(spacex_df[spacex_df['class']==1]['Launch Site'].value_counts().reset_index(),
                       values='count',
                       names='Launch Site',
                       title='Total Success Launches by Site')
    else:
        pie_fig=px.pie(spacex_df[spacex_df['Launch Site']==site]['class'].value_counts().reset_index(),
                       values='count',
                       names='class',
                       title=f'Total Success Launches for site {site}'
                      )
    return [dcc.Graph(figure=pie_fig)]
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback([Output(component_id='success-payload-scatter-chart',component_property='children')],
              [Input(component_id='site-dropdown',component_property='value'),
               Input(component_id='payload-slider',component_property='value')]
             )
def scatter_chart (site,payload):
    if site=='ALL':
        scatter_fig=px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])],
                               x='Payload Mass (kg)',
                               y='class',
                               color='Booster Version Category',
                               title='Correlation between Payload & Success for all Sites'
                              )
    else:
        scatter_fig=px.scatter(spacex_df[(spacex_df['Payload Mass (kg)'].between(payload[0],payload[1]))& (spacex_df['Launch Site']==site)],
                               x='Payload Mass (kg)',
                               y='class',
                               color='Booster Version Category',
                               title=f'Correlation between Payload & Success for site {site}'
                              )
    return [dcc.Graph(figure=scatter_fig)]

# Run the app
if __name__ == '__main__':
    app.run_server()
