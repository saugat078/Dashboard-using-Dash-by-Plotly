import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from colour_constants import custom_colors
import numpy as np

scatter_plot_layout = dcc.Graph(
    id="scatter-plot",
    config={"responsive": True, "displayModeBar": False},
    style={'width': '100%', 'height': '300px'},
)

def scatter_plot_callback(app, data, default_processors):
    @app.callback(
        Output("scatter-plot", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_scatter_plot(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]

        filtered_data = data[data['cpu_processor'].isin(selected_processors)]
        print(filtered_data)
        hover_template = '<b>NAME</b>: %{customdata[0]}' + '<br>' + \
                         '<b>Display Inch</b>: %{x}' + '<br>' + \
                         '<b>Weight</b>: %{y}' + '<extra></extra>'
        max_name_length = 20  # trim laptop names
        filtered_data['name'] = filtered_data['name'].str[:max_name_length]

        fig = px.scatter(
            filtered_data,
            x='display_inch',
            y='weight_kg',
            color='cpu_processor',
            title="Display size vs Weight Scatter Plot",
            custom_data=['name']
        )

        fig.update_layout(
            plot_bgcolor=custom_colors['background'],
            paper_bgcolor=custom_colors['background'],
            font_color=custom_colors['text'],
            font_family="FreeSerif",
            title_x=0.5,
            title_y=0.95,
            title_xanchor='center',
            title_yanchor='top',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_traces(hovertemplate=hover_template)

        return fig
