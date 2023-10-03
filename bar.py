import dash_core_components as dcc
import plotly.express as px
from dash import Input, Output

# Define the layout for the bar graph
bargraph_layout = dcc.Graph(
    id="graph",
    config={"responsive": True},
    style={'width': '50%', 'height': '300px'},
)

# Define the callback for the bar graph
def bargraph_callback(app, data, default_processors):
    @app.callback(
        Output("graph", "figure"),
        Input("cpu-processor-dropdown", "value")
    )
    def update_bar_chart(selected_processors):
        if not selected_processors:
            selected_processors = default_processors
        elif not isinstance(selected_processors, list):
            selected_processors = [selected_processors]  # Convert to a list if it's a single value.

        max_prices_df = data.groupby('cpu_processor')['price_eur'].max().reset_index()
        max_prices_df.rename(columns={'price_eur': 'max_price_eur'}, inplace=True)

        filtered_df = max_prices_df[max_prices_df['cpu_processor'].isin(selected_processors)]
        fig = px.bar(
            filtered_df, x="cpu_processor", y="max_price_eur",
            title="Max CPU Processor Price"
        )

        y_range = [0, max(max_prices_df['max_price_eur'])]
        fig.update_layout(yaxis=dict(range=y_range))

        return fig





# data = pd.read_csv("https://raw.githubusercontent.com/saugat078/files/main/mindfactory_updated%20-%20mindfactory_updated%20(1).csv")
# data = data.dropna(subset=['price_eur', 'cpu_processor'])
# amd_cpu=data[data['cpu_processor'].str.contains("AMD SoC")]
# max_amd_price = amd_cpu['price_eur'].max()
# print(max_amd_price)
