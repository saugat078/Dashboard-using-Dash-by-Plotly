from dash import Dash, dcc, html

# Import the components and data_loader module
from bar import bargraph_layout, bargraph_callback
from data_loader import load_data
from line_plot import linechart_callback,linechart_layout
from pie_chart import pie_chart_callback,piechart_layout

app = Dash(__name__, external_stylesheets=['/assets/style.css'])

# Load the dataset using the data_loader module
data = load_data()
print(type(data))

# Filter out rows with missing or incorrect values in the 'cpu_processor' column
valid_processors = data['cpu_processor'].dropna().unique()

# Create options for the Dropdown
options = [{"label": processor, "value": processor} for processor in valid_processors]

def default(count,index,valid_processors):
    z=[]
    for i in range(index,len(valid_processors)):
        if count<3:
            z.append(valid_processors[i])
            count+=1
        else:
            break
    return z
default_values = default(0,3,valid_processors)
print(default_values)


# app.layout = html.Div([
#     html.Div([
#     html.H4('Max CPU Processor Price'),
#     dcc.Dropdown(
#         id="cpu-processor-dropdown",
#         options=options,
#         value=default_values,
#         multi=True,
#         style={'width': '50%'},
#     ),
#     bargraph_layout,
#     piechart_layout
#     ]),
#     linechart_layout,
#     ])
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="cpu-processor-dropdown",
            options=options,
            value=default_values,
            multi=True,
            className="dropdown-container",
        ),
        html.Div([
            bargraph_layout,
            piechart_layout,
        ], className="bargraph-piechart-container"),
    ], className="main-container"),

    html.Div([
        linechart_layout,
    ], className="linechart-container"),
])

#  callback function execution
bargraph_callback(app, data, default_values) 
linechart_callback(app,data)
pie_chart_callback(app,data,default_values)
if __name__ == '__main__':
    app.run_server(debug=True)
