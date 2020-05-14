import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc


from dataframe_manipulation import get_ratings_range


app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])
app.layout = html.Div([dbc.Row([dbc.Col([
    html.H1(["My Ratings"], style={"textAlign": "center"}),
    dcc.RangeSlider(
        id="my-range-slider",
        min=0,
        max=5,
        step=0.5,
        value=[2, 3],
    ),
    html.H4(id="values", style={"textAlign": "center"}),
    dbc.Table(id="ratings")], className="mx-auto")], className="mx-auto", style={"textAlign": "center"})
], style={"textAlign": "center"})


@app.callback(
    [dash.dependencies.Output("ratings", "children"),
     dash.dependencies.Output("values", "children")],
    [dash.dependencies.Input("my-range-slider", "value")])
def update_output(value):
    int_val = f"{value[0]} to {value[1]}"
    value = get_ratings_range(value[0], value[1])
    return dbc.Table.from_dataframe(value,  bordered=True, dark=True, responsive=True, striped=True), int_val


if __name__ == "__main__":
    app.run_server(debug=True)
