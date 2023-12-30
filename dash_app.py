import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

# Use the Dash Bootstrap Components theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Incorporate data
data_all_years = pd.read_excel('datasheets.xlsx', sheet_name="India_SA_Implants_Data")
data_all_years_my_region = pd.read_excel('datasheets.xlsx', sheet_name="My Region")

year_choices = [
    "All Years",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023"
]

tenures = {
    "Overall": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "First Quarter": [1, 2, 3],
    "Second Quarter": [4, 5, 6],
    "Third Quarter": [7, 8, 9],
    "Fourth Quarter": [10, 11, 12],
}

# App layout using Bootstrap components
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H3(children='Select Region'),
            dcc.RadioItems(options=["All India", "My Region"], value='All India', id='region_selected'),
        ], className='col-md-4'),

        html.Div([
            html.H3(children='Select Year'),
            dcc.RadioItems(options=year_choices, value='All Years', id='year_selected'),
        ], className='col-md-4'),

        html.Div([
            html.H3(children='Select Tenure'),
            dcc.RadioItems(options=list(tenures.keys()), value='Overall', id='tenure_selected'),
        ], className='col-md-4'),
    ], className='row'),

    dcc.Graph(figure={}, id='product_graph'),
    dcc.Graph(figure={}, id='patient_graph'),
], className='container-fluid')

@callback(
    Output(component_id='product_graph', component_property='figure'),
    Output(component_id='patient_graph', component_property='figure'),
    Input(component_id='region_selected', component_property='value'),
    Input(component_id='year_selected', component_property='value'),
    Input(component_id='tenure_selected', component_property='value'),
)
def update_graph(region_chosen, year_chosen, tenure_chosen):

    if region_chosen == "My Region":
        df = data_all_years_my_region
    else:
        df = data_all_years

    df['Implant Date'] = pd.to_datetime(df['Implant Date'], format='%d/%m/%Y')
    if year_chosen=="All Years":
        final_df = df[df['Implant Date'].dt.month.isin(tenures[tenure_chosen])]
    else:
        selected_year_df = df[df['Implant Date'].dt.year.isin([int(year_chosen)])]
        final_df = selected_year_df[selected_year_df['Implant Date'].dt.month.isin(tenures[tenure_chosen])]

    key_product_frequency_df = pd.DataFrame({'Values': final_df["Key Product"].value_counts().index, 'Count': final_df["Key Product"].value_counts().values})

    fig1 = px.bar(key_product_frequency_df,
                  x='Values',
                  y='Count',
                  title=f'{tenure_chosen} {year_chosen}',
                  labels={'Values': "Key Product", 'Count': 'Frequency'},
                  text_auto=True)

    patient_type_frequency_df = pd.DataFrame({'Values': final_df["Patient Type"].value_counts().index, 'Count': final_df["Patient Type"].value_counts().values})

    fig2 = px.pie(patient_type_frequency_df,
                  names='Values',
                  values='Count',
                  title=f'{tenure_chosen} {year_chosen}',
                  labels={'Values': "Key Product", 'Count': 'Frequency'},
                  hover_data=['Values'])

    fig = [fig1, fig2]
    return fig

if __name__ == '__main__':
    app.run_server()
