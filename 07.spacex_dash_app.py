import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Read the data
data = pd.read_csv('spacex_launch_dash.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# TASK 1: Layout with Dropdown and Slider
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in data['Launch Site'].unique()]

app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(id='site-dropdown', options=dropdown_options, value='ALL',
                 placeholder='Select a Launch Site', searchable=True),
    html.Br(),
    # TASK 2: Pie Chart
    dcc.Graph(id='success-pie-chart'),
    html.P('Payload range (Kg):'),
    # TASK 3: Slider for Payload
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'}, value=[data['Payload Mass (kg)'].min(), data['Payload Mass (kg)'].max()]),
    # TASK 4: Scatter Chart
    dcc.Graph(id='success-payload-scatter-chart')
])

# TASK 2: Callback for Pie Chart
@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_data = data[data['Launch Site'] == selected_site]
        fig = px.pie(filtered_data, names='class', title=f'Success vs Failure for {selected_site}')
    return fig

# TASK 4: Callback for Scatter Chart
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    filtered_data = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])]
    if selected_site != 'ALL':
        filtered_data = filtered_data[filtered_data['Launch Site'] == selected_site]
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version',
                     title='Correlation between Payload and Success')
    return fig

if __name__ == '__main__':
    app.run_server()