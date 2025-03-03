import pandas as pd
import dash
from dash import dcc, html, Input, Output
from django_plotly_dash import DjangoDash
from store.models import Order, OrderItem, Product
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import numpy as np

# ✅ สร้าง Dash App
app = DjangoDash('SalesDashboard')

# ✅ ฟังก์ชันดึงข้อมูลจากโมเดล Django
def get_data():
    order_items = OrderItem.objects.select_related("order", "product").values(
        "order__created_at", "price", "quantity", "product__name", "product__category"
    )
    df = pd.DataFrame.from_records(order_items)

    if not df.empty:
        df["order__created_at"] = pd.to_datetime(df["order__created_at"]).dt.date  # แปลงเป็นรูปแบบวันที่
        df["total_price"] = df["price"] * df["quantity"]  # คำนวณยอดขายรวมต่อสินค้า

    return df

# ✅ โหลดข้อมูล
df = get_data()

# ✅ Layout ของ Dash
app.layout = html.Div([
    html.H1("📊 ระบบวิเคราะห์ยอดขาย", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id="period-filter",
        options=[
            {"label": "สัปดาห์นี้", "value": "week"},
            {"label": "เดือนนี้", "value": "month"},
            {"label": "ปีนี้", "value": "year"},
            {"label": "ทั้งหมด", "value": "all"},
        ],
        value="week",
        placeholder="เลือกช่วงเวลา"
    ),

    dcc.Graph(id="sales-line-chart"),  # ✅ กราฟเส้นยอดขาย

    # ✅ กราฟแท่งและวงกลมอยู่คู่กัน
    html.Div([
        html.Div(dcc.Graph(id="sales-bar-chart"), style={'width': '50%', 'padding': '10px'}),
        html.Div(dcc.Graph(id="sales-pie-chart"), style={'width': '50%', 'padding': '10px'}),
    ], style={'display': 'flex'}),

    dcc.Graph(id="category-bar-chart"),  # ✅ กราฟหมวดหมู่สินค้าขายดีที่สุด
    dcc.Graph(id="sales-prediction-chart")  # ✅ กราฟพยากรณ์ยอดขาย
])

@app.callback(
    [Output("sales-line-chart", "figure"), 
     Output("sales-bar-chart", "figure"), 
     Output("sales-pie-chart", "figure"), 
     Output("category-bar-chart", "figure"),  # ✅ กราฟหมวดหมู่สินค้า
     Output("sales-prediction-chart", "figure")],
    Input("period-filter", "value")
)
def update_charts(period):
    df = get_data()
    current_date = datetime.now().date()

    if period == "week":
        start_date = current_date - timedelta(weeks=1)
    elif period == "month":
        start_date = current_date.replace(day=1)
    elif period == "year":
        start_date = current_date.replace(month=1, day=1)
    else:
        start_date = df["order__created_at"].min()

    filtered_df = df[df["order__created_at"] >= start_date]

    # ✅ **กราฟเส้นยอดขายรายวัน**
    if not filtered_df.empty:
        sales_summary = filtered_df.groupby("order__created_at")["total_price"].sum().reset_index()
        line_fig = px.line(sales_summary, x="order__created_at", y="total_price",
                           title="📈 ยอดขายรายวัน",
                           labels={"order__created_at": "วันที่", "total_price": "ยอดขาย (บาท)"})
    else:
        line_fig = px.line(title="ไม่มีข้อมูลยอดขายรายวัน")

    # ✅ **กราฟแท่งยอดขายตามจำนวนออเดอร์**
    if not filtered_df.empty:
        product_summary = filtered_df.groupby("product__name")["quantity"].sum().reset_index()
        bar_fig = px.bar(product_summary, x="product__name", y="quantity",
                         title="📊 จำนวนสินค้าที่ขายได้",
                         labels={"product__name": "ชื่อสินค้า", "quantity": "จำนวนที่ขาย"})
    else:
        bar_fig = px.bar(title="ไม่มีข้อมูลยอดขายสินค้า")

    # ✅ **กราฟวงกลมสินค้าขายดีที่สุด**
    if not filtered_df.empty:
        pie_fig = px.pie(product_summary, names="product__name", values="quantity",
                         title="🥧 สินค้าที่ขายดีที่สุด",
                         labels={"product__name": "ชื่อสินค้า", "quantity": "จำนวนที่ขาย"})
    else:
        pie_fig = px.pie(title="ไม่มีข้อมูลยอดขายสินค้า")

    # ✅ **กราฟแท่งหมวดหมู่สินค้าขายดีที่สุด**
    if not filtered_df.empty():
        category_summary = filtered_df.groupby("product__category")["total_price"].sum().reset_index()
        category_fig = px.bar(category_summary, x="product__category", y="total_price",
                              title="📦 หมวดหมู่สินค้าที่ขายดีที่สุด",
                              labels={"product__category": "หมวดหมู่สินค้า", "total_price": "ยอดขายรวม (บาท)"},
                              color="total_price", color_continuous_scale="greens")
    else:
        category_fig = px.bar(title="ไม่มีข้อมูลหมวดหมู่สินค้า")

    # ✅ **พยากรณ์ยอดขาย 30 วันข้างหน้า**
    if not filtered_df.empty():
        sales_summary["order__created_at"] = pd.to_datetime(sales_summary["order__created_at"])
        sales_summary["days_since_start"] = (sales_summary["order__created_at"] - sales_summary["order__created_at"].min()).dt.days

        # Train Model
        X = sales_summary["days_since_start"].values.reshape(-1, 1)
        y = sales_summary["total_price"].values
        model = LinearRegression().fit(X, y)

        # Predict Future Sales for the Next 30 Days
        future_days = np.arange(X[-1][0] + 1, X[-1][0] + 31).reshape(-1, 1)
        future_dates = [sales_summary["order__created_at"].max() + timedelta(days=i) for i in range(1, 31)]
        future_sales = model.predict(future_days)

        # Plot Predictions
        prediction_df = pd.DataFrame({"order__created_at": future_dates, "predicted_sales": future_sales})
        prediction_fig = px.line(prediction_df, x="order__created_at", y="predicted_sales",
                                 title="🔮 พยากรณ์ยอดขาย 30 วันข้างหน้า",
                                 labels={"order__created_at": "วันที่", "predicted_sales": "ยอดขายที่คาดการณ์ (บาท)"},
                                 line_shape="spline")
        prediction_fig.add_scatter(x=sales_summary["order__created_at"], y=sales_summary["total_price"], mode="markers+lines",
                                   name="ยอดขายจริง")
    else:
        prediction_fig = px.line(title="ไม่สามารถคำนวณพยากรณ์ยอดขายได้")

    return line_fig, bar_fig, pie_fig, category_fig, prediction_fig
