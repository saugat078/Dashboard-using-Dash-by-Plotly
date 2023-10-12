import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def container(title,value):
    return html.Div(
        className="box-shadow-container",
        children=[
            html.H3(title),
            dcc.Loading(
                type="default",
                children=[
                    html.P(value),
                ],
            ),
        ],
    )