import dash                     # pip install dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd             # pip install pandas
# Data: https://www.dallasopendata.com/Services/Animals-Inventory/qgg6-h4bd

df = pd.read_excel("./data.xlsx")
print(df.columns.tolist())
print(df.head())
df["postcode"] = df["postcode"].apply(str).str.split(".").str.get(0)
df["Licence_type"] = df["Licence_type"].str.split("-").str.get(1).str.title()
opts=[{'label' : x, 'value' : x}for x in df["postcode"].unique()]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("EGMs by License Type in NSW", style={"textAlign":"center"}),
    html.Hr(),
    html.P("select postcodes:"),
    html.Div(html.Div([
        dcc.Dropdown(id='dropdownSelection', clearable=False,
                    multi=True,
                    value=["2022","2021"],
                    placeholder="select postcodes",
                    options=opts),
    ],className="seven columns"),className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="dropdownSelection", component_property="value"),
)
def dropdown_changed(year_chosen): 
    
    if(year_chosen is not None):
        # HISTOGRAM
        df_hist = df[df["postcode"].isin(year_chosen)]
        fig_hist = px.histogram(df_hist, x="Licence_type", y='EGMs', color="postcode",barmode="group", histfunc='avg')
        fig_hist.update_xaxes(categoryorder="mean descending")
    else:
        df_hist = df[df["postcode"].isin(["2000","2009"])]
        fig_hist = px.histogram(df_hist, x="Licence_type", y='EGMs', color="Licence_type", histfunc='avg')
        fig_hist.update_xaxes(categoryorder="mean descending")

   

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
        ], className="row"),
        html.Hr(),
      
    ]


if __name__ == '__main__':
    app.run_server(debug=True)