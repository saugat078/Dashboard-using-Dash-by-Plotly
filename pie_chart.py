import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output

piechart_layout = dcc.Graph(
    id="pie-graph",
    config={"responsive": True},
    style={'width': '50%', 'height': '300px'},
)

def pie_chart_callback(app, data, default_processors):
    @app.callback(
        Output("pie-graph", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_pie_chart(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]

        filtered_data = data[data['cpu_processor'].isin(selected_processors)]
        print(filtered_data)
        os_counts = filtered_data['operating_system'].value_counts().reset_index()
        print(os_counts)

        fig = px.pie(os_counts, values='count', names='operating_system', hole=0.3)
        return fig
