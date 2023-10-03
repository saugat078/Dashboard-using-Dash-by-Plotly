from dash import Dash, dcc, html

# Import the components and data_loader module
from bar import bargraph_layout, bargraph_callback
from data_loader import load_data

app = Dash(__name__)

# Load the dataset using the data_loader module
data = load_data()

# Filter out rows with missing or incorrect values in the 'cpu_processor' column
valid_processors = data['cpu_processor'].dropna().unique()

# Create options for the Dropdown
options = [{"label": processor, "value": processor} for processor in valid_processors]

# Set the default values to the first three processors
default_values = valid_processors[:3]

app.layout = html.Div([
    html.H4('Max CPU Processor Price'),
    dcc.Dropdown(
        id="cpu-processor-dropdown",
        options=options,
        value=default_values,
        multi=True,
        style={'width': '50%'},
    ),
    bargraph_layout,
])

# Register the callback from the bargraph module
bargraph_callback(app, data, default_values) 




if __name__ == '__main__':
    app.run_server(debug=True)
