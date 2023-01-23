from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output

from data.loader import DataSchema
from . import ids


def render(app, data):

  @app.callback(
    Output(ids.BAR_CHART, "children"),
    Input(ids.YEAR_DROPDOWN, "value")
  )
  def update_bar_chart(years):
    filtered_data = data.query("year in @years")
    print(filtered_data)
    if filtered_data.shape[0] == 0:
      return html.Div("No data Selected.")  


    def create_pivot_table():
      pt = filtered_data.pivot(
        values=DataSchema.QUANTITY,
        index=[DataSchema.STATUS],
        aggfunc="sum",
        fill_value=0
      )
      return pt.reset_index().sort_values(DataSchema.QUANTITY, ascending=False)

    fig = px.bar(
      create_pivot_table(),
      x=DataSchema.STATUS,
      y=DataSchema.QUANTITY,
      color=DataSchema.STATUS
    )

    return html.Div(
      dcc.Graph(figure=fig), 
      id=ids.BAR_CHART
      )
# MEDAL_DATA = px.data.medals_long()


# def render(app):

#   @app.callback(
#     Output(ids.BAR_CHART, "children"),
#     Input(ids.YEAR_DROPDOWN, "value")
#   )
#   def update_bar_chart(status):
#     #filter the data based on the status value in the input column
#     filtered_data = MEDAL_DATA.query("nation in @status")

#     if filtered_data.shape[0] == 0:
#       return html.Div("No data selected")
#     fig = px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
#     return html.Div(
#       dcc.Graph(figure=fig),
#       id=ids.BAR_CHART,
#       )
#     return html.Div(id=ids.BAR_CHART)