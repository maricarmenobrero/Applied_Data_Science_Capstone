# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Marks for the payload slider
payload_marks = {i: f'{i}' for i in range(0, 10001, 2500)}

# Dropdown options for Launch Sites
unique_sites = sorted(spacex_df['Launch Site'].unique())
site_options = ([{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in unique_sites]
)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 40}),
    
    # ---- DROPDOWN FOR LAUNCH SITES ----
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    html.Div([
        html.Label('Select Launch Site', style={'color': '#503D36', 'fontWeight': 'bold'}),
        dcc.Dropdown(id='site-dropdown',
                     options=site_options,
                     value='ALL',  # Default value for the dropdown
                     searchable=True,
                     clearable=False  # Prevent clearing the selection
                     )
              ]
            ),
    html.Br(),

    # ---- PIE CHART FOR SUCCESSFUL LAUNCHES ----
    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # ---- SLIDER FOR PAYLOAD RANGE ----
    html.Label('Payload Range (kg)', style={'color': '#503D36', 'fontWeight': 'bold'}),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    value=[min_payload, max_payload],  # Default range
                    marks=payload_marks,
                    tooltip={'placement': 'bottom', 'always_visible': True},  # Tooltip for the slider
                    allowCross=False  # Prevent crossing of the two slider handles
                    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Decorator for the callback function
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

# Callback function to update the pie chart based on selected launch site
def update_success_pie(selected_site):
    if selected_site == 'ALL':
        # If 'All Sites' is selected, show the total successful launches (class=1) for all sites
        df_group = (spacex_df.groupby('Launch Site', as_index=False)['class']
                    .sum()
                    .rename(columns={'class': 'successes'}))
        
        fig = px.pie(
            df_group,
            names='Launch Site',
            values='successes',
            title='Total Successful Launches by Site'
        )
    else:
        # Success vs. Failure for the selected site
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = df_site['class'].value_counts().reindex([1, 0], fill_value=0)

        fig = px.pie(
            names=['Success', 'Failure'],
            values=[counts[1], counts[0]],
            title=f'Success vs. Failure for {selected_site}'
        )
    
    fig.update_traces(textinfo='percent+label')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Decorator for the callback function
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
# Callback function to update the scatter chart based on selected launch site and payload range
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    # Filter the dataframe based on payload range
    df = spacex_df.copy()
    df = df[(df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)]

    # Filter by selected launch site
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
        title = f'Payload vs. Success for {selected_site}'
    else:
        title = 'Payload vs. Success for All Sites'

    # Create a scatter plot
    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',                 # 0 = Failure, 1 = Success
        color='Booster Version Category',
        hover_data=['Launch Site', 'Payload Mass (kg)'],
        labels={'class': 'Success (1) / Failure (0)'},
        title=title
    )

    fig.update_layout(
        xaxis_title='Payload Mass (kg)',
        yaxis_title='Class (1 = success, 0 = failure)',
        legend_title='Booster Version Category',
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
