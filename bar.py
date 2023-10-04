import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output
import numpy as np

# Define the layout for the bar graph
bargraph_layout = dcc.Graph(
    id="graph",
    config={"responsive": True},
    style={'width': '50%', 'height': '300px'},
)

# Define the callback for the bar graphz
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
        price_stats_df = data.groupby('cpu_processor').agg({'price_eur': ['max', 'min']}).reset_index()
        price_stats_df.columns = ['cpu_processor', 'max_price_eur', 'min_price_eur']

        filtered_df = price_stats_df[price_stats_df['cpu_processor'].isin(selected_processors)]

        laptop_names_max = []
        laptop_names_min = []
        for processor in selected_processors:
            max_idx = data[data['cpu_processor'] == processor]['price_eur'].idxmax()
            min_idx = data[data['cpu_processor'] == processor]['price_eur'].idxmin()
            laptop_names_max.append(data.loc[max_idx, 'name'])
            laptop_names_min.append(data.loc[min_idx, 'name'])

        filtered_df['laptop_name_max'] = laptop_names_max
        filtered_df['laptop_name_min'] = laptop_names_min
        
        hover_template_max = '<b>CPU Processor</b>: %{x}' + '<br>' + \
                        '<b>Max Price</b>: %{y:.2f} EUR' + '<br>' + \
                        '<b>Laptop Name (Max)</b>: %{customdata[0]}' + '<extra></extra>'
        hover_template_min = '<b>CPU Processor</b>: %{x}' + '<br>' + \
                        '<b>Min Price</b>: %{y:.2f} EUR' + '<br>' + \
                        '<b>Laptop Name (Min)</b>: %{customdata[1]}' + '<extra></extra>'
                        
        
        customdf = np.stack((filtered_df['laptop_name_max'],filtered_df['laptop_name_min']))     
            
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
        fig.update_traces(hovertemplate=hover_template_max, selector=dict(name='max_price_eur'))
        fig.update_traces(hovertemplate=hover_template_min, selector=dict(name='min_price_eur'))


        return fig
