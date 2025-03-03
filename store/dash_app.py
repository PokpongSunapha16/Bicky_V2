import dash
from dash import dcc, html  # ✅ แก้ Import ตามเวอร์ชันใหม่
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from django.db.models import Count, Sum
from store.models import Product, Order, StorePayment

# ✅ สร้าง Dash App
app = DjangoDash('SalesDashboard')

# ✅ ฟังก์ชันดึงข้อมูลแบบ Lazy Load (หลีกเลี่ยงการดึงข้อมูลตอน import)
def get_dashboard_data():
    category_data = list(Product.objects.values("category").annotate(total=Count("id")))
    sales_data = list(Order.objects.values("created_at").annotate(total_sales=Sum("total_amount")))
    payment_data = list(StorePayment.objects.values("payment_method").annotate(total=Count("id")))

    df_category = pd.DataFrame(category_data)
    df_sales = pd.DataFrame(sales_data)
    df_payment = pd.DataFrame(payment_data)

    return df_category, df_sales, df_payment

# ✅ Callback ใน Dash เพื่อโหลดข้อมูลเมื่อรัน
def update_dashboard():
    df_category, df_sales, df_payment = get_dashboard_data()

    # ✅ ป้องกัน Error กรณีไม่มีข้อมูล
    if df_sales.empty:
        df_sales = pd.DataFrame({"created_at": [], "total_sales": []})

    # ✅ สร้างกราฟ
    fig_category = px.pie(df_category, names="category", values="total", title="Product Categories")
    fig_sales = px.line(df_sales, x="created_at", y="total_sales", title="Sales Over Time") if not df_sales.empty else None
    fig_payment = px.pie(df_payment, names="payment_method", values="total", title="Payment Methods")

    return fig_category, fig_sales, fig_payment

# ✅ อัปเดต Layout โดยไม่โหลดข้อมูลล่วงหน้า
app.layout = html.Div([
    html.H1("📊 Sales Dashboard"),
    
    html.Div([
        dcc.Graph(id="category_graph"),
        dcc.Graph(id="sales_graph"),
        dcc.Graph(id="payment_graph"),
    ]),

    # ✅ ปุ่มโหลดข้อมูล (กดแล้วคำนวณใหม่)
    html.Button("Reload Data", id="reload_button", n_clicks=0),
])

# ✅ Callback เพื่ออัปเดตกราฟเมื่อกดปุ่ม
from dash.dependencies import Input, Output

@app.callback(
    [Output("category_graph", "figure"),
     Output("sales_graph", "figure"),
     Output("payment_graph", "figure")],
    Input("reload_button", "n_clicks")
)
def update_graph(n_clicks):
    return update_dashboard()
