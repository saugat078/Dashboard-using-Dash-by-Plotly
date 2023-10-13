import dash_core_components as dcc
import plotly.express as px
from colour_constants import custom_colors
from dash import Input, Output

piechart_layout = dcc.Graph(
    id="pie-graph",
    config={"responsive": True},
    style={'width': '100%', 'height': '300px'},
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

        fig = px.pie(
            os_counts, 
            values='count', 
            names='operating_system', 
            hole=0.3)
        fig.update_layout(
            title="Operating System Distribution",
            plot_bgcolor=custom_colors['background'],
            paper_bgcolor=custom_colors['background'],
            font_color=custom_colors['text'],
            title_x=0.5,  # Horizontally center the title
            title_y=0.95,  # Adjust the vertical position of the title
            title_xanchor='center',  # Center align the title
            title_yanchor='top',  # Align the title to the top of the graph
            margin=dict(l=20, r=20, t=40, b=20)  # Add margins to create space around the graph
        )
        
        return fig
