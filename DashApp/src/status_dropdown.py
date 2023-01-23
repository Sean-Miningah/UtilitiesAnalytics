from dash import Dash, html, dcc 
from dash.dependencies import Input, Output

from . import ids

def render(app):
  all_status = [1, 0]

  @app.callback(
    Output(ids.STATUS_DROPDOWN, "value"),
    Input(ids.SELECT_ALL_STATUS_BUTTON, "n_clicks")
  )
  def select_all_status(i):
    return all_status

  return html.Div(
    children=[
      html.H6("status"),
      dcc.Dropdown(
        id=ids.STATUS_DROPDOWN,
        options=[{"label": status, "value":status} for status in all_status],
        value=all_status,
        multi=True,
      ),
      html.Button(
        className="dropdown-button",
        children=["Select All"],
        id=ids.SELECT_ALL_STATUS_BUTTON
      )
    ]
  )