import dash
import dash_core_components as dcc
import dash_html_components as html



def container(value,title,icon_component):
    return html.Div(
        className="kpi-card",
        children=[
            html.H3(value,className="card-value"),
            html.Div([icon_component,],className="icon-i"),
            dcc.Loading(
                type="default",
                children=[
                    html.P(title,className="card-text "),
                ],
            ),
        ],
    )