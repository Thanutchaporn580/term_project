from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Layout ของหน้าเว็บ
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("PM2.5 Forecast Dashboard", className='text-center my-4')
        )
    ),
    dbc.Row(
        dbc.Col(html.P("พยากรณ์ค่าฝุ่น PM2.5 ล่วงหน้า 7 วัน", className='text-center'))
    ),
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id='date-picker',
            ),
            width=6
        ),
        dbc.Col(
            dcc.Dropdown(
                id='hour-dropdown',
                options=[{'label': f'{i:02d}:00', 'value': i} for i in range(24)],
                value=0,
                clearable=False
            ),
            width=6
        ),
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id='humidity-input', type='number', placeholder='Humidity (%)'), width=3),
        dbc.Col(dcc.Input(id='temperature-input', type='number', placeholder='Temperature (°C)'), width=3),
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Button('Predict', id='predict-button', n_clicks=0),
            width=12,
            className='text-center'
        )
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                id='pm25-forecast-graph'
            )
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                figure=go.Figure(go.Scattermapbox(
                    lat=[6.9939],  # โรงแรมวีแอล หาดใหญ่
                    lon=[100.6162],
                    mode='markers',
                    marker={'size': 12, 'color': 'blue'},
                    text=['โรงแรมวีแอล หาดใหญ่'],
                    hoverinfo='text'
                )).update_layout(
                    mapbox_style="open-street-map",
                    title="ตำแหน่งที่ตรวจวัด PM2.5 (โรงแรมวีแอล หาดใหญ่)",
                    mapbox=dict(
                        center=dict(lat=6.9939, lon=100.6162),
                        zoom=8
                    ),
                    uirevision="mapbox",
                    dragmode="zoom"
                ),
                id='pm25-map',
                style={"width": "80%", "height": "500px", "margin": "auto"}
            ),
            width=12
        )
    )
], fluid=True, style={
    'backgroundImage': 'url("/assets/background_pm2_5.jpg")',
    'backgroundSize': 'cover',
    'backgroundRepeat': 'no-repeat',
    'minHeight': '100vh'
})
