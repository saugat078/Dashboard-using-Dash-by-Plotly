from dash import Dash, dcc, html
from bar import bargraph_layout, bargraph_callback
from data_loader import load_data
from line_plot import linechart_callback,linechart_layout
from pie_chart import pie_chart_callback,piechart_layout
from scatter_plot import scatter_plot_callback,scatter_plot_layout
from gpu_bar_chart import bar_chart_layout,gpu_distribution_callback
from container import container
from dash_iconify import DashIconify


app = Dash(__name__, external_stylesheets=['/assets/style.css'])
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
z=int(data['price_eur'].mean())
y=int(data['price_eur'].count())
print(z)
app.layout = html.Div(
    children=[
        html.Div([
            html.Div([html.H3("NOTEBOOK DASHBOARD",style={"color":"white","font-family":"FreeSerif"}),],style={"display":"flex","justify-content":"center"}),
            html.Div([
                container(f"$ {z}","Mean Price",DashIconify(icon="fa-solid:dollar-sign"),),
                container(f"{y}","Total Products ",DashIconify(icon="fa-solid:shield-alt"),),
                # container("bla", "50"),
                # container("bla", "50"),
            ], className="cont-child"),
             html.Div([html.H3("select processors from drop down to view the analytics",style={"font-family":"FreeSerif","color":"white"}),],style={"display":"flex","margin-left":"20px"}),
                dcc.Dropdown(
                    id="cpu-processor-dropdown",
                    options=options,
                    value=default_values,
                    multi=True,
                    className="dropdown-style",
                ),
                html.Div([
                html.Div(
                    bargraph_layout,
                className="bargraph-container"),
                html.Div(
                    piechart_layout,
                 className="piechart-container"),
                html.Div(
                    scatter_plot_layout,
                 className="scatterplot-container"),
                ],className='container'),
            html.Div([
            html.Div([
                linechart_layout,
                ],className="linechart-container"),
            html.Div([
                bar_chart_layout,
                ],className="barchart-container"),],className="line-gpu-container")
        ], className="parent-div")
    ]
)



#  callback function execution
bargraph_callback(app, data, default_values) 
linechart_callback(app,data)
pie_chart_callback(app,data,default_values)
scatter_plot_callback(app,data,default_values)
gpu_distribution_callback(app,data,default_values)


if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.254.6', port=8050)
