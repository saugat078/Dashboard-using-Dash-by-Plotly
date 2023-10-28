import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from colour_constants import custom_colors

# Define the layout for the bar chart component
bar_chart_layout = dcc.Graph(
    id="gpu-distribution-bar-chart",
    config={"responsive": True, "displayModeBar": False},
    style={'width': '100%', 'height': '300px'},
)

# Create a callback to update the GPU distribution bar chart
def gpu_distribution_callback(app, data,default_processors):
    @app.callback(
        Output("gpu-distribution-bar-chart", "figure"),
        Input("cpu-processor-dropdown", "value")  # Use the same dropdown as the CPU processor dropdown
    )
    def update_scatter_plot(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]

        filtered_data = data[data['cpu_processor'].isin(selected_processors)]
        print(filtered_data)

        fig = px.bar(
            filtered_data, 
            x=['gpu_integrated', 'gpu_extra'], 
            title=f"GPU Type Distribution for Selected Processors")

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
