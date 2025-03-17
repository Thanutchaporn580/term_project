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
    # ตรวจสอบว่ามีข้อมูลที่ถูกต้องถูกส่งไปยังโมเดล
    if forecast_model is not None:
        forecast = predict_ts(forecast_model, fh=n_periods)
        return forecast['yhat']
    else:
        raise ValueError("Forecast model is not loaded properly.")

# ฟังก์ชันสำหรับตรวจสอบค่าเกินมาตรฐาน (Classification)
def classify_pm25(pm25_value):
    """ตรวจสอบว่า PM2.5 เกินมาตรฐานหรือไม่"""
    data = pd.DataFrame({'pm_2_5': [pm25_value]})
    prediction = predict_classification(classification_model, data=data)
    return prediction['prediction_label'].iloc[0] # 1=เกิน, 0=ไม่เกิน

# ฟังก์ชันสำหรับดึงวันล่าสุดจากไฟล์ข้อมูลจริง
def get_latest_date_from_file(file_path="pm25_data.csv"):
    df = pd.read_csv(file_path)  # อ่านไฟล์ CSV
    df['Date'] = pd.to_datetime(df['Date'])  # แปลงคอลัมน์ Date เป็น datetime
    return df['Date'].max()  # คืนค่าวันล่าสุด

# ตั้งค่า layout ของแอป
app.layout = layout

# Callback สำหรับการอัปเดตกราฟเมื่อคลิกปุ่ม "Predict"
@app.callback(
    Output('pm25-forecast-graph', 'figure'),
    Input('predict-button', 'n_clicks')
)
def update_graph(n_clicks):
    if n_clicks and n_clicks > 0:
        try:
            # 1. พยากรณ์ PM2.5 ด้วย ARIMA (7 วัน)
            forecast_series = predict_pm25_arima()

            # 2. ใช้วันล่าสุดจากไฟล์เป็นจุดเริ่มต้นของการพยากรณ์
            latest_date = get_latest_date_from_file()
            forecast_dates = [latest_date + timedelta(days=i) for i in range(len(forecast_series))]

            # 3. สร้าง DataFrame สำหรับแสดงผล
            forecast_df = pd.DataFrame({'Date': forecast_dates, 'PM2.5': forecast_series.values})

            # 4. ตรวจสอบสถานะ PM2.5 (เกิน/ไม่เกิน) สำหรับแต่ละค่าที่พยากรณ์
            forecast_df['Status'] = forecast_df['PM2.5'].apply(classify_pm25)
            forecast_df['Status'] = forecast_df['Status'].replace({1: 'Exceeding', 0: 'Not Exceeding'})

            # 5. สร้างกราฟ (แสดงค่า PM2.5 และสถานะ)
            fig = go.Figure()

            # เพิ่มเส้นแสดงค่า PM2.5 ที่ทำนาย
            fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['PM2.5'],
                                     mode='lines', name='Predicted PM2.5',
                                     line=dict(color='blue')))

            # เพิ่มเส้นแสดงค่า PM2.5 ที่เกินมาตรฐาน
            exceeding_df = forecast_df[forecast_df['Status'] == 'Exceeding']
            if not exceeding_df.empty:
                fig.add_trace(go.Scatter(x=exceeding_df['Date'], y=exceeding_df['PM2.5'],
                                         mode='lines', name='Exceeding',
                                         line=dict(color='red', dash='dot')))

            # เพิ่มเส้นแสดงค่า PM2.5 ที่ไม่เกินมาตรฐาน
            not_exceeding_df = forecast_df[forecast_df['Status'] == 'Not Exceeding']
            if not not_exceeding_df.empty:
                fig.add_trace(go.Scatter(x=not_exceeding_df['Date'], y=not_exceeding_df['PM2.5'],
                                         mode='lines', name='Not Exceeding',
                                         line=dict(color='green')))

            # ปรับแต่ง Layout ของกราฟ
            fig.update_layout(title='PM2.5 Forecast (7 Days)',
                              xaxis_title='Date',
                              yaxis_title='PM2.5 Value (ug/m3)',
                              template='plotly_dark')

            return fig
        except Exception as e:
            print(f"Error in update_graph: {e}")
            return go.Figure()
    else:
        return go.Figure()

# รันแอปพลิเคชัน Dash
if __name__ == '__main__':
    app.run_server(debug=True)