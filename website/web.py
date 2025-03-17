from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Layout ของหน้าเว็บ
layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1(
                "PM2.5 Forecast Dashboard",
                className='text-center my-4',
                style={
                    'color': '#2c3e50',  # สีข้อความสีขาว
                    'textShadow': '2px 2px 5px rgba(0,0,0,0.3)'
                }
            )
        )
    ),
    dbc.Row(
        dbc.Col(
            html.P(
                "Predict PM2.5 levels for the next 7 days",
                className='text-center',
                style={
                    'fontSize': '1.5rem',
                    'fontFamily': 'Prompt',
                    'color': '#2c3e50',  # สีข้อความสีนํ้าเงิน
                    'textShadow': '2px 2px 5px rgba(0,0,0,0.3)'
                }
            )
        )
    ),
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id='date-picker',
                display_format='DD/MM/YYYY',
                placeholder='Select Date',
                style={
                    'backgroundColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'borderColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'color': '#ffffff'  # สีข้อความสีขาว
                }
            ),
            width=6
        ),
        dbc.Col(
            dcc.Dropdown(
                id='hour-dropdown',
                options=[{'label': f'{i:02d}:00', 'value': i} for i in range(24)],
                value=0,
                clearable=False,
                placeholder='Select Hour',
                style={
                    'backgroundColor': '#FFC0CB',  # สีพื้นหลังสีชมพู
                    'borderColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'color': '#000000'  # สีข้อความสีขาว
                }
            ),
            width=6
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Input(
                id='humidity-input',
                type='number',
                placeholder='Humidity (%)',
                className="form-control",
                style={
                    'backgroundColor': '#87CEEB',  # สีพื้นหลังสีฟ้า
                    'color': '#ffffff',  # สีข้อความสีขาว
                    'borderColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'marginBottom': '10px'
                }
            ),
            width=3
        ),
        dbc.Col(
            dcc.Input(
                id='temperature-input',
                type='number',
                placeholder='Temperature (°C)',
                className="form-control",
                style={
                    'backgroundColor': '#FFA500',  # สีพื้นหลังสีส้ม
                    'color': '#ffffff',  # สีข้อความสีขาว
                    'borderColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'marginBottom': '10px'
                }
            ),
            width=3
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Button(
                'Predict',
                id='predict-button',
                n_clicks=0,
                className='btn btn-primary',
                style={
                    'width': '200px',
                    'borderRadius': '15px',
                    'padding': '8px',
                    'fontSize': '1rem',
                    'marginBottom': '10px',
                    'margin': '0 auto',
                    'backgroundColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'borderColor': '#2c3e50',  # สีพื้นหลังสีน้ำเงิน
                    'color': '#ffffff'  # สีข้อความสีขาว
                }
            ),
            width=12,
            className='text-center'
        )
    ]),
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                id='pm25-forecast-graph',
                style={'backgroundColor': '#2c3e50'}  # สีพื้นหลังสีน้ำเงิน
            )
        )
    ),
    dbc.Row(
        dbc.Col(
            dcc.Graph(
                figure=go.Figure(go.Scattermapbox(
                    lat=[6.9939],
                    lon=[100.6162],
                    mode='markers',
                    marker={'size': 30, 'color': '#2c3e50'},  # ขยายขนาดจุด
                    text=['VL Hat Yai Hotel'],
                    hoverinfo='text'
                )).update_layout(
                    title=dict(
                        text="PM2.5 Measurement Location",
                        x=0.5,
                        font=dict(
                            size=18,
                            color='#ffffff',  # สีข้อความสีขาว
                            family='Prompt'
                        )
                    ),
                    mapbox_style="open-street-map",
                    mapbox=dict(
                        center=dict(lat=6.9939, lon=100.6162),
                        zoom=11,  # ปรับการซูม
                        pitch=35  # เพิ่มมุมมองให้ดูหรูหรา
                    ),
                    uirevision="mapbox",
                    dragmode="zoom",
                    margin=dict(l=0, r=0, t=30, b=0)
                ),
                id='pm25-map',
                style={"width": "95%", "height": "650px", "margin": "20px auto", "boxShadow": "0px 4px 10px rgba(0,0,0,0.3)"}
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
