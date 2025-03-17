import dash
from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from pycaret.time_series import load_model as load_ts_model, predict_model as predict_ts
from pycaret.classification import load_model as load_classification_model, predict_model as predict_classification
from datetime import datetime, timedelta

# นำเข้า layout จาก web.py
from web import layout

# สร้างแอป Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# โหลดโมเดล Time Series (ARIMA)
forecast_model = load_ts_model('arima_model_4')

# โหลดโมเดล Classification
classification_model = load_classification_model('pm25_rf_classification_model_20250317_065046')

# ฟังก์ชันสำหรับพยากรณ์ค่า PM2.5 ด้วย ARIMA (7 วัน)
def predict_pm25_arima(n_periods=7):
    """พยากรณ์ PM2.5 ด้วย ARIMA สำหรับ n วันข้างหน้า"""
    forecast = predict_ts(forecast_model, fh=n_periods)
    return forecast['yhat']

# ฟังก์ชันสำหรับตรวจสอบค่าเกินมาตรฐาน (Classification)
def classify_pm25(pm25_value):
    """ตรวจสอบว่า PM2.5 เกินมาตรฐานหรือไม่"""
    data = pd.DataFrame({
        'pm_2_5': [pm25_value]
    })
    prediction = predict_classification(classification_model, data=data)
    return prediction['prediction_label'].iloc[0] # 1=เกิน, 0=ไม่เกิน

# ตั้งค่า layout ของแอป
app.layout = layout

# Callback สำหรับการอัปเดตกราฟเมื่อคลิกปุ่ม "Predict"
# ในส่วนของ Callback
@app.callback(
    Output('pm25-forecast-graph', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_graph(n_clicks):
    if n_clicks > 0:
        # ... (ส่วนโค้ดอื่นไม่เปลี่ยน) ...

        # 4. สร้างกราฟ (แสดงค่า PM2.5 และสถานะ)
        fig = go.Figure()

        # ... (ส่วนเพิ่ม Trace ไม่เปลี่ยน) ...

        # ปรับแต่ง Layout ของกราฟ
        fig.update_layout(
            template='plotly_dark',  # สีเข้ม
            paper_bgcolor='rgba(0,0,0,0)',  # โปร่งใส
            plot_bgcolor='rgba(0,0,0,0)',  # โปร่งใส
            title=dict(
                text='PM2.5 Forecast (7 Days)',
                x=0.5,
                font=dict(size=24, color='#ffffff')  # สีขาว
            ),
            xaxis=dict(
                title=dict(text='วันที่', font=dict(color='#ffffff')),
                tickfont=dict(color='#ffffff')
            ),
            yaxis=dict(
                title=dict(text='ค่า PM2.5 (ug/m³)', font=dict(color='#ffffff')),
                tickfont=dict(color='#ffffff')
            )
        )

        return fig
    else:
        return {}


# รันแอปพลิเคชัน Dash
if __name__ == '__main__':
    app.run_server(debug=True)
