import dash_core_components as dcc
import plotly.express as px
from dash import Output,Input
from colour_constants import custom_colors

# layout for the line chart
linechart_layout = dcc.Graph(
    id="line-chart",
    config={"responsive": True},
    style={'width': '100%', 'height': '300px'},
)

# callback for the line chart
def linechart_callback(app, data):
    @app.callback(
        Output("line-chart", "figure"),
        Input("cpu-processor-dropdown", "value") 
    )
    def update_line_chart(dummy):
        db = data[['release_year', 'price_eur']]
        
        # Drop rows with null values in any column
        db.dropna(inplace=True)    
        avg_data = db.groupby('release_year').mean().reset_index()
        print(avg_data)
        fig = px.line(
            avg_data,
            x="release_year",
            y="price_eur",
            title="Year vs. Price Line Chart",
            labels={"year": "release_Year", "price": "price_eur"},
        )
        fig.update_xaxes(tickmode='linear', dtick=1)
        fig.update_layout(
            plot_bgcolor=custom_colors['texture'],
            paper_bgcolor=custom_colors['background'],
            font_color=custom_colors['text'],
        )
        return fig
    