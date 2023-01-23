from dash import Dash, html, dcc 
from dash.dependencies import Input, Output

from . import ids
from data.loader import DataSchema

def render(app, data):
  all_year = data[DataSchema.YEAR].tolist()
  unique_years = sorted(set(all_year), key=int)

  @app.callback(
    Output(ids.YEAR_DROPDOWN, "value"),
    Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
  )
  def select_all_years(_):
    return unique_years

  return html.Div(
    children=[
      html.H6("Year"),
      dcc.Dropdown(
        id = ids.YEAR_DROPDOWN,
        options=[{"label":year, "value": year} for year in unique_years],
        value=unique_years,
        multi=True,
      ),
      html.Button(
        className="dropdown-button",
        children=["Select All"],
        id=ids.SELECT_ALL_YEARS_BUTTON
      )

    ]
  )