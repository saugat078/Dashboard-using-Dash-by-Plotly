import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from src.colour_constants import custom_colors

# Layout for the bar graph
bargraph_layout_boolean = dcc.Graph(
    id="graph-boolean",
    config={"responsive": True},
    style={'width': '100%', 'height': '300px'},
)

def bargraph_callback_boolean(app, data, default_processors):
    @app.callback(
        Output("graph-boolean", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_bar_chart_boolean(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]  

        # Selecting boolean columns for analysis
        boolean_columns = ['has_touchscreen', 'keyboard_backlit', 'has_webcam', 'has_bluetooth']

        # Group by CPU processor and count occurrences of boolean values
        boolean_stats_df = data.groupby('cpu_processor')[boolean_columns].sum().reset_index()

        # Filter the data based on selected processors
        filtered_df = boolean_stats_df[boolean_stats_df['cpu_processor'].isin(selected_processors)]

        fig = px.bar(
            filtered_df,
            x="cpu_processor",
            y=boolean_columns,
            barmode='group',
            title="Boolean Feature Counts by CPU Processor",
            labels={'value': 'Count'},
        )
        fig.update_xaxes(title_text="CPU Processor")
        fig.update_yaxes(title_text="Count")
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

        return fig
