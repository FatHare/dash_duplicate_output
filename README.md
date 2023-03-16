## Install

```
pip install git+https://github.com/FatHare/dash_duplicate_output.git
```

## Description

Package can be used to solve the problem with duplicate callback outputs in <a href="https://dash.plotly.com/">dash plotly app.</a>

<b>Steps</b>:
1) init in app
2) used in callbacks

## Example
```python
from dash import Dash, html, Input, Output

from dash_duplicate_output import DuplicateOutputManager


app = Dash(__name__)
DuplicateOutput = DuplicateOutputManager(app)


class Identify:
    span_id = 'span'
    btn_left_id = 'button-left'
    btn_right_id = 'button-right'


app.layout = html.Div(
    children=[
        html.Div(
            children=['Last button pressed: ', html.Span(
                id=Identify.span_id, children='empty')]
        ),
        html.Button(
            id=Identify.btn_left_id,
            children='left'
        ),
        html.Button(
            id=Identify.btn_right_id,
            children='right'
        )
    ]
)


@app.callback(
    [
        # Note: DuplicateOutput can also be called from app, example: app.DuplicateOutput(Identify.span_id, 'children').
        DuplicateOutput(Identify.span_id, 'children'),
        Output(Identify.btn_left_id, 'children')
    ],
    Input(Identify.btn_left_id, 'n_clicks'),
    prevent_initial_call=True
)
def on_tuch_btn_left(n_clicks):
    return 'left', f'left {n_clicks}'


@app.callback(
    [
        DuplicateOutput(Identify.span_id, 'children'),
        Output(Identify.btn_right_id, 'children')
    ],
    Input(Identify.btn_right_id, 'n_clicks'),
    prevent_initial_call=True
)
def on_tuch_btn_right(n_clicks):
    return 'right', f'right {n_clicks}'


if __name__ == '__main__':
    app.run_server(debug=True, port=2023)
```

## How does it work?
Each time output is called, the passed properties are written to the relationship and an intermediate output on the dataset is returned. Further, when the application is initialized, clientside callbacks are generated and then, when rendering, tags with intermediate datasets are added to the dom. Done, everything works on the client side with minimal costs.

## TODO
- refactoring
- add comments
