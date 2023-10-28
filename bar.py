import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
from colour_constants import custom_colors
import numpy as np



# layout for the bar graph
bargraph_layout = dcc.Graph(
    id="graph",
    config={"responsive": True},
    style={'width': '100%', 'height': '300px'},
)

def bargraph_callback(app, data, default_processors):
    @app.callback(
        Output("graph", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_bar_chart(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]  # Convert to a list if it's a single value

        # Calculate both max and min prices for each CPU processor
        price_stats_df = data.groupby('cpu_processor').agg({'price_eur': ['max', 'min'], 'name': ['first', 'last']}).reset_index()
        price_stats_df.columns = ['cpu_processor', 'max_price_eur', 'min_price_eur', 'laptop_name_max', 'laptop_name_min']

        filtered_df = price_stats_df[price_stats_df['cpu_processor'].isin(selected_processors)]

        hover_template_max = '<b>CPU Processor</b>: %{x}' + '<br>' + \
                            '<b>Max Price</b>: %{y:.2f} EUR' + '<br>' + \
                            '<b>Laptop Name (Max)</b>: %{customdata[0]}' + '<extra></extra>'
        hover_template_min = '<b>CPU Processor</b>: %{x}' + '<br>' + \
                            '<b>Min Price</b>: %{y:.2f} EUR' + '<br>' + \
                            '<b>Laptop Name (Min)</b>: %{customdata[1]}' + '<extra></extra>'

        customdf = np.stack((filtered_df['laptop_name_max'], filtered_df['laptop_name_min']))

        fig = px.bar(
            filtered_df,
            x="cpu_processor",
            y=["max_price_eur", "min_price_eur"],  # Plot both max and min prices
            barmode='group',  # Display as grouped bars
            title="Max and Min CPU Processor Prices",
            labels={"max_price_eur": "Max Price", "min_price_eur": "Min Price"},
            custom_data=customdf
        )
        fig.update_yaxes(title_text="Price")
        fig.update_xaxes(title_text="CPU_Processor")
        y_range = [0, max(price_stats_df['max_price_eur'].max(), price_stats_df['min_price_eur'].max())]

        fig.update_layout(yaxis=dict(range=y_range))
        fig.update_layout(
            plot_bgcolor=custom_colors['background'],
            paper_bgcolor=custom_colors['background'],
            font_color=custom_colors['text'],
            font_family="FreeSerif",
            title_x=0.5, 
            title_y=0.95, 
            title_xanchor='center',
            title_yanchor='top',  
            margin=dict(l=20, r=20, t=60, b=20)  
            )
        fig.update_traces(hovertemplate=hover_template_max, selector=dict(name='max_price_eur'))
        fig.update_traces(hovertemplate=hover_template_min, selector=dict(name='min_price_eur'))

        return fig