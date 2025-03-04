from django_plotly_dash import DjangoDash
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from store.models import Order, Product, CustomUser
from dash.dependencies import Input, Output

# ✅ สร้าง Dash App
app = DjangoDash("DashboardApp")

# ✅ ฟังก์ชันดึงข้อมูล
def get_dashboard_data():
    total_sales = Order.objects.filter(status="delivered").aggregate(total=pd.Sum("total_amount"))["total"] or 0
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = CustomUser.objects.filter(role="customer").count()

    sales_data = Order.objects.values("created_at").annotate(total=pd.Sum("total_amount")).order_by("created_at")
    df_sales = pd.DataFrame(sales_data)

    product_data = Product.objects.values("category").annotate(total=pd.Count("id"))
    df_products = pd.DataFrame(product_data)

    orders_data = Order.objects.extra(select={"month": "MONTH(created_at)"}).values("month").annotate(total=pd.Count("id"))
    df_orders = pd.DataFrame(orders_data)

    customers_data = CustomUser.objects.extra(select={"month": "MONTH(date_joined)"}).values("month").annotate(total=pd.Count("id"))
    df_customers = pd.DataFrame(customers_data)

    return total_sales, total_products, total_orders, total_customers, df_sales, df_products, df_orders, df_customers

# ✅ Layout ของ Dash
app.layout = html.Div([
    html.H1("📊 Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([html.H3("💰 Total Sales"), html.P(id="total_sales")], className="stat-card"),
        html.Div([html.H3("📦 Total Products"), html.P(id="total_products")], className="stat-card"),
        html.Div([html.H3("🛒 Total Orders"), html.P(id="total_orders")], className="stat-card"),
        html.Div([html.H3("👥 Total Customers"), html.P(id="total_customers")], className="stat-card"),
    ], className="stats-container"),

    html.Div([
        dcc.Graph(id="sales_graph"),
        dcc.Graph(id="product_pie_chart"),
        dcc.Graph(id="monthly_orders_bar"),
        dcc.Graph(id="monthly_customers_line"),
    ], className="graphs-container"),

    html.Button("Reload Data", id="reload_button", n_clicks=0),
])

# ✅ Callback อัปเดตข้อมูล
@app.callback(
    [Output("total_sales", "children"),
     Output("total_products", "children"),
     Output("total_orders", "children"),
     Output("total_customers", "children"),
     Output("sales_graph", "figure"),
     Output("product_pie_chart", "figure"),
     Output("monthly_orders_bar", "figure"),
     Output("monthly_customers_line", "figure")],
    [Input("reload_button", "n_clicks")]
)
def update_dashboard(n_clicks):
    total_sales, total_products, total_orders, total_customers, df_sales, df_products, df_orders, df_customers = get_dashboard_data()

    # ✅ กราฟยอดขายรายวัน
    fig_sales = px.line(df_sales, x="created_at", y="total", title="📈 Sales Trend Over Time")

    # ✅ กราฟประเภทสินค้า (Pie Chart)
    fig_products = px.pie(df_products, names="category", values="total", title="📊 Product Categories")

    # ✅ กราฟจำนวนคำสั่งซื้อรายเดือน (Bar Chart)
    fig_orders = px.bar(df_orders, x="month", y="total", title="📅 Monthly Orders")

    # ✅ กราฟลูกค้ารายใหม่ต่อเดือน (Line Chart)
    fig_customers = px.line(df_customers, x="month", y="total", title="👥 New Customers Per Month")

    return f"฿{total_sales:,.2f}", total_products, total_orders, total_customers, fig_sales, fig_products, fig_orders, fig_customers
