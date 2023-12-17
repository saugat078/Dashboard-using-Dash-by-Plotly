import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from src.colour_constants import custom_colors

# Layout for the scatter plot
ram_scatter_layout = dcc.Graph(
    id="ram-scatter-plot",
    config={"responsive": True, "displayModeBar": False},
    style={'width': '100%', 'height': '300px'},
)

# Callback to update the scatter plot
def ram_scatter_callback(app, data, default_processors):
    @app.callback(
        Output("ram-scatter-plot", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_ram_scatter(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]

        filtered_data = data[data['cpu_processor'].isin(selected_processors)]
        #neglect null values
        filtered_data = filtered_data.dropna(subset=['psu_watts'])

        max_name_length = 20 
        filtered_data['name'] = filtered_data['name'].str[:max_name_length]
        fig = px.scatter(
            filtered_data,
            x="ram_memory",
            y="psu_watts",
            color="cpu_processor",
            size="psu_watts",
            hover_data=["name"],
            title="RAM Size vs Power Supply Scatter Plot",
            labels={"ram_memory": "RAM Size (GB)", "psu_watts": "Power Supply Unit (Watts)"},
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
            margin=dict(l=20, r=20, t=40, b=20),
        )

        return fig

