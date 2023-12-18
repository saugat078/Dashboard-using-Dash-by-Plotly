from dash import Dash, dcc, html
from bar import bargraph_layout, bargraph_callback
from data_loader import load_data
from line_plot import linechart_callback,linechart_layout
from pie_chart import pie_chart_callback,piechart_layout
from scatter_plot import scatter_plot_callback,scatter_plot_layout
from gpu_bar_chart import bar_chart_layout,gpu_distribution_callback
from boxplot import dimensions_boxplot_callback,boxplot_layout_dimensions
from bool_bar import bargraph_layout_boolean,bargraph_callback_boolean
from battery_boxplot import battery_boxplot_callback,battery_boxplot_layout
from ram_scatter_plot import ram_scatter_callback,ram_scatter_layout
from container import container
from dash_iconify import DashIconify


app = Dash(__name__, external_stylesheets=['/assets/style.css'])
server=app.server
data = load_data()
print(type(data))

# Filter out rows with missing or incorrect values in the 'cpu_processor' column
valid_processors = data['cpu_processor'].dropna().unique()

# options for the Dropdown
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
s=int(data['display_inch'].mean())
p=int(data['weight_kg'].mean())
display_resolution_counts = data['display_resolution'].value_counts()
q=display_resolution_counts.idxmax()
print(z)
app.layout = html.Div(
    children=[
        html.Div([
            html.Div([html.H3("NOTEBOOK DASHBOARD",style={"color":"white","font-family":"FreeSerif"}),],style={"display":"flex","justify-content":"center"}),
            html.Div([
                container(f"$ {z}","Mean Price",DashIconify(icon="fa-solid:dollar-sign"),),
                container(f"{y}","Total Products ",DashIconify(icon="fa-brands:shopify"),),
                container(f"{s} inch","Avgerage Display Size ",DashIconify(icon="fa-solid:tv"),),
                container(f"{p} kg","Average Weight",DashIconify(icon="fa-solid:dumbbell"),),
                container(f"{q} ","Popular Resolution",DashIconify(icon="fa-solid:desktop"),),
                # container("bla", "50"),
                # container("bla", "50"),
            ], className="cont-child"),
             html.Div([html.H3("Select processors from drop down to view the analytics",style={"font-family":"FreeSerif","color":"white"}),],style={"display":"flex","margin-left":"20px"}),
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
                ],className="barchart-container"),
            html.Div([
               boxplot_layout_dimensions
                ],className="box-plot"),
                ],className="line-gpu-container"),
            html.Div([
                html.Div([
               battery_boxplot_layout],className="linechart-container"),
                html.Div([
               bargraph_layout_boolean],className="barchart-container"),
                html.Div([
               ram_scatter_layout],className="box-plot"),
            ],className="line-gpu-container"),
        ],className="parent-div"),
    ]
)



#  callback function execution
bargraph_callback(app, data, default_values) 
linechart_callback(app,data)
pie_chart_callback(app,data,default_values)
scatter_plot_callback(app,data,default_values)
gpu_distribution_callback(app,data,default_values)
dimensions_boxplot_callback(app,data,default_values)
bargraph_callback_boolean(app,data,default_values)
battery_boxplot_callback(app,data,default_values)
ram_scatter_callback(app,data,default_values)

if __name__ == '__main__':
    app.run_server(debug=True,port="8050")
