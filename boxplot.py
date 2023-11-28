import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
import numpy as np
from dash import dcc
from colour_constants import custom_colors

# Define the layout for the boxplot component
boxplot_layout_dimensions = dcc.Graph(
    id="dimensions-boxplot",
    config={"responsive": True, "displayModeBar": False},
    style={'width': '100%', 'height': '300px'},
)

# Create a callback to update the dimensions boxplot
def dimensions_boxplot_callback(app, data,default_processors):
    @app.callback(
        Output("dimensions-boxplot", "figure"),
        Input("cpu-processor-dropdown", "value")  # Assuming you have a CPU processor dropdown for selection
    )
    def update_dimensions_boxplot(selected_processors):
        if not selected_processors:
            # Provide default processors if none selected
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            # Ensure selected_processors is a list
            selected_processors = [selected_processors]

        # Filter data based on selected processors
        filtered_data = data[data['cpu_processor'].isin(selected_processors)]

        # Selecting relevant columns for dimensions boxplot
        dimension_columns = ['height_mm', 'width_mm', 'depth_mm']

        # Create a boxplot using Plotly Express
        fig = px.box(filtered_data, y=dimension_columns,title="Boxplot of Dimensions")

        # Customize layout
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

        return fig