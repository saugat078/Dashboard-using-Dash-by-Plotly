import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from colour_constants import custom_colors

scatter_plot_layout = dcc.Graph(
    id="scatter-plot",
    config={"responsive": True},
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

        fig = px.scatter(
            filtered_data, 
            x='display_inch', 
            y='weight_kg',
            color='operating_system',
            title="Display size vs Weight Scatter Plot",
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
        
        return fig
