from dash import Dash, html

from . import status_dropdown, bar_charts, year_dropdown

def create_layout(app, data): 
  return html.Div(
    className="app-div", 
    children=[
      html.H1(app.title),
      html.Hr(),

      bar_charts.render(app,data),
      html.Div(
        className="dropdown-container",
        children = [
          year_dropdown.render(app, data),
        ]
      ),
      # bar_charts.render(app, data)
      # html.Div(
      #   className="dropdown-container",
      #   children=[
      #     status_dropdown.render(app)
      #   ]
      # ),
      
    ]
  )