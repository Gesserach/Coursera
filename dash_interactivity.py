import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'Site 1', 'value': 'site1'},
        {'label': 'Site 2', 'value': 'site2'},
        {'label': 'Site 3', 'value': 'site3'},
        {'label': 'Site 4', 'value': 'site4'}
    ],
    value='ALL',  # Default value is 'ALL', which means all sites will be selected initially
    placeholder="Select a Launch Site here",  # Placeholder text to guide the user
    searchable=True  # Allow searching for launch sites
)

# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # If 'ALL' sites are selected, use the entire dataframe
    filtered_df = spacex_df
    if entered_site != 'ALL':
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    # Calculate success and failure counts
    success_count = filtered_df[filtered_df['class'] == 1].shape[0]
    failure_count = filtered_df[filtered_df['class'] == 0].shape[0]
    
    # Data for the pie chart
    labels = ['Success', 'Failure']
    values = [success_count, failure_count]
    
    # Create the pie chart figure
    fig = px.pie(
        names=labels,
        values=values,
        title=f'Success Rate for {entered_site}' if entered_site != 'ALL' else 'Total Launch Success Rate',
        hole=0.3  # Donut style chart
    )
    
    # Return the figure to update the pie chart
    return fig

dcc.RangeSlider(
    id='payload-slider',
    min=0,  # Starting point of the slider (0 Kg)
    max=10000,  # Ending point of the slider (10000 Kg)
    step=1000,  # Interval for each step (1000 Kg)
    marks={i: f'{i} Kg' for i in range(0, 10001, 1000)},  # Markings on the slider for each 1000 Kg increment
    value=[0, 10000]  # Initial range for the slider (from min_payload to max_payload)
)

# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id="payload-slider", component_property="value")
    ]
)
def get_scatter_plot(entered_site, payload_range):
    # Filter the dataframe based on the selected payload range
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                             (spacex_df['Payload Mass (kg)'] <= max_payload)]
    
    # If a specific launch site is selected, filter the dataframe further
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    # Create the scatter plot
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',  # Color by booster version
        title=f'Success vs Payload for {entered_site}' if entered_site != 'ALL' else 'Success vs Payload for All Sites',
        labels={'class': 'Launch Outcome (Success=1, Failure=0)', 'Payload Mass (kg)': 'Payload Mass (kg)'},
        hover_data=['Booster Version Category', 'Launch Site'],  # Additional data on hover
        opacity=0.7  # Set opacity for better visualization
    )
    
    # Return the figure to update the scatter chart
    return fig
