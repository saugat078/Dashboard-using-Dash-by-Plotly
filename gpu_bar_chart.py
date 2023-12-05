import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash import Input, Output
from colour_constants import custom_colors

# layout for the bar chart component
bar_chart_layout = dcc.Graph(
    id="gpu-distribution-bar-chart",
    config={"responsive": True, "displayModeBar": False},
    style={'width': '100%', 'height': '300px'},
)

# callback to update the GPU distribution bar chart
def gpu_distribution_callback(app, data, default_processors):
    @app.callback(
        Output("gpu-distribution-bar-chart", "figure"),
        Input("cpu-processor-dropdown", "value") 
    )
    def update_scatter_plot(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]

        filtered_data = data[data['cpu_processor'].isin(selected_processors)]

        # count of GPU types for 'gpu_integrated' and 'gpu_extra'
        filtered_data['gpu_integrated_count'] = filtered_data.groupby('gpu_integrated')['gpu_integrated'].transform('count')
        filtered_data['gpu_extra_count'] = filtered_data.groupby('gpu_extra')['gpu_extra'].transform('count')

        customdf = np.stack((filtered_data['gpu_integrated_count'], filtered_data['gpu_extra_count'],filtered_data['gpu_integrated'],filtered_data['gpu_extra']))

        fig = px.bar(
            filtered_data, 
            x=['gpu_integrated', 'gpu_extra'],
            title=f"GPU Type Distribution for Selected Processors",
            custom_data=customdf,
        )
       
        hover_template_integrated = '<b>GPU</b>: %{customdata[2]}' + '<br>' + \
                            '<b>COUNT</b>: %{customdata[0]}' + '<extra></extra>'
        hover_template_extra = '<b>GPU</b>: %{customdata[3]}' + '<br>' + \
                            '<b>COUNT</b>: %{customdata[1]}' + '<extra></extra>'
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
        fig.update_traces(hovertemplate=hover_template_integrated, selector=dict(name='gpu_integrated'))
        fig.update_traces(hovertemplate=hover_template_extra, selector=dict(name='gpu_extra'))
        return fig
