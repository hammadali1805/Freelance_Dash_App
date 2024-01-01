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

def count_total_sales_anually(data):    
    # Extracting the year from 'Implant Date'
    data['Year'] = data['Implant Date'].dt.year
    

    total_sales_anually =  pd.DataFrame({'Year': data["Year"].value_counts().index.astype(int).astype(str), 'Sales': data["Year"].value_counts().values})
    
    return total_sales_anually.sort_values(by=['Year'])

def graph_total_sales_anually(data, region_chosen):

    fig = px.bar(data,
                  x='Year',
                  y='Sales',
                  title=f'Key Product Anual Sales Analysis {region_chosen}',
                  text_auto=True,
                  width=700)
    
    return fig

def count_total_sales_quarterly(df):
    # Convert 'Implant Date' to datetime format
    df['Implant Date'] = pd.to_datetime(df['Implant Date'], format='%d/%m/%Y')

    # Extract Year and Quarter from 'Implant Date'
    df['Year'] = df['Implant Date'].dt.year
    df['Quarter'] = df['Implant Date'].dt.quarter

    # Create a pivot table to get the count of rows for each quarter of every year
    pivot_table = pd.pivot_table(df, values='Account Name', index=['Year', 'Quarter'], aggfunc='count', fill_value=0).reset_index()
    pivot_table.rename(columns={'Account Name': 'Sales'}, inplace=True)

    pivot_table['Year'] = pivot_table['Year'].astype(int).astype(str)
    pivot_table['Quarter'] = pivot_table['Quarter'].astype(int).astype(str)

    return pivot_table.sort_values(by=['Year'])


def graph_total_sales_quarterly(data, region_chosen):

    fig = px.bar(data,
                  x='Year',
                  y='Sales',
                  color="Quarter",
                  category_orders={'Quarter': ["1", "2", "3", "4"]},
                  title=f'Key Product Quarterly Sales Analysis {region_chosen}',
                  text_auto=True,
                  barmode="group",
                  width=700)
    
    return fig

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

        dcc.Graph(figure={}, id='sales_graph_anually', config={'toImageButtonOptions': {
    'filename': 'custom_image',
    'height': 500,
    'width': 700,
  }}),
        dcc.Graph(figure={}, id='sales_graph_quarterly', config={'toImageButtonOptions': {
    'filename': 'custom_image',
    'height': 500,
    'width': 700,
  }}),
        dcc.Graph(figure={}, id='product_graph', config={'toImageButtonOptions': {
    'filename': 'custom_image',
    'height': 500,
    'width': 700,
  }}),
        dcc.Graph(figure={}, id='patient_graph', config={'toImageButtonOptions': {
    'filename': 'custom_image',
    'height': 500,
    'width': 700,
  }}),
])



@callback(
    Output(component_id='sales_graph_anually', component_property='figure'),
    Output(component_id='sales_graph_quarterly', component_property='figure'),
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
    df = df[df['Implant Date'].dt.year != 2017]

    fig1 = graph_total_sales_anually(count_total_sales_anually(df), region_chosen)
    fig2 = graph_total_sales_quarterly(count_total_sales_quarterly(df), region_chosen)


    if year_chosen=="All Years":
        final_df = df[df['Implant Date'].dt.month.isin(tenures[tenure_chosen])]
    else:
        selected_year_df = df[df['Implant Date'].dt.year.isin([int(year_chosen)])]
        final_df = selected_year_df[selected_year_df['Implant Date'].dt.month.isin(tenures[tenure_chosen])]

    key_product_sales_df = pd.DataFrame({'Values': final_df["Key Product"].value_counts().index, 'Count': final_df["Key Product"].value_counts().values})

    fig3 = px.bar(key_product_sales_df,
                  x='Values',
                  y='Count',
                  title=f'Key Product Analysis {tenure_chosen} {year_chosen} {region_chosen}',
                  labels={'Values': "Key Product", 'Count': 'Sales'},
                  text_auto=True,
                  width=700)
    
    patient_type_sales_df = pd.DataFrame({'Values': final_df["Patient Type"].value_counts().index, 'Count': final_df["Patient Type"].value_counts().values})

    fig4 = px.pie(patient_type_sales_df,
                  names='Values',
                  values='Count',
                  title=f'Patient Type Analysis {tenure_chosen} {year_chosen} {region_chosen}',
                  labels={'Values': "Key Product", 'Count': 'Frequency'},
                  width=700,
                  hover_data=['Values'])


    fig = [fig1, fig2, fig3, fig4]
    return fig

if __name__ == '__main__':
    app.run_server()
