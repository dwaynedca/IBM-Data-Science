# require import libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# load file and set max and min payload
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Creating Layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),

# Task 1 Add a Launch Site Drop-down Input Component
dcc.Dropdown(id='site-dropdown',
            options=[
            {'label': 'All Sites', 'value': 'All Sites'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                ],
            placeholder='Select a Launch Site Here One of the Option',
            value='All',
            searchable=True
            ),
                                html.Br(),

# Task 2 Add a callback function to render
html.Div(dcc.Graph(id='success-pie-chart')),
html.Br(),

# Task 3 Add a Range Slider to Select Payload
dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0:'0', 2000:'2000', 
                        4000:'4000', 6000:'6000', 
                        8000:'8000', 10000:'10000'},
                value=[min_payload, max_payload]),

#Task 4 Add a callback function to rende
html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2 Function
# Function decorator to specify function input and output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(launch_site):
    if launch_site == 'All':
        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].mean(), 
                     names=spacex_df.groupby('Launch Site')['Launch Site'].first(),
                     title='Total Success Launches by Site')
    else:
        fig = px.pie(values=spacex_df[spacex_df['Launch Site']==str(launch_site)]['class'].value_counts(normalize=True), 
                     names=spacex_df['class'].unique(), 
                     title='Total Success Launches for Site {}'.format(launch_site))
    return fig

# Task 4
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider',component_property='value')])
def get_payload_chart(launch_site, payload_mass):
    if launch_site == 'All':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], 
                x="Payload Mass (kg)",
                y="class",
                color="Booster Version Category",
                hover_data=['Launch Site'],
                title='Correlation Between Payload and Success for All Sites')
    else:
        df = spacex_df[spacex_df['Launch Site']==str(launch_site)]
        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])], 
                x="Payload Mass (kg)",
                y="class",
                color="Booster Version Category",
                hover_data=['Launch Site'],
                title='Correlation Between Payload and Success for Site {}'.format(launch_site))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
