import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from colour_constants import custom_colors

# Layout for the box plot
battery_boxplot_layout = dcc.Graph(
    id="battery-capacity-boxplot",
    config={"responsive": True},
    style={'width': '100%', 'height': '300px'},
)

def battery_boxplot_callback(app, data, default_processors):
    @app.callback(
        Output("battery-capacity-boxplot", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_battery_capacity_boxplot(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]  

        # Filter the data based on selected processors
        filtered_data = data[data['cpu_processor'].isin(selected_processors)]
        hover_template = '<b>Processor</b>: %{x}' + '<br>' + \
                         '<b>Battery Capacity</b>: %{y} Wh' + '<br>' + \
                         '<b>Name</b>: %{customdata[0]}' + '<extra></extra>'
        max_name_length = 20 
        filtered_data['name'] = filtered_data['name'].str[:max_name_length]
        fig = px.box(
            filtered_data,
            x="cpu_processor",
            y="battery_capacity_wh",
            title="Box Plot of Battery Capacity",
            custom_data=['name'])

        # Customize layout if needed
        fig.update_layout(
            plot_bgcolor=custom_colors['background'],
            paper_bgcolor=custom_colors['background'],
            font_color=custom_colors['text'],
            font_family="FreeSerif",
            title_x=0.5,
            title_y=0.95,
            title_xanchor='center',
            title_yanchor='top',
            margin=dict(l=20, r=20, t=60, b=20),
        )
        fig.update_traces(hovertemplate=hover_template)

        return fig
