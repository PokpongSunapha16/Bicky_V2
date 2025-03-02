from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone  # ✅ เพิ่มบรรทัดนี้
from django.urls import reverse
import json
from decimal import Decimal
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('Agg')  # ใช้ backend แบบไม่ต้องเปิด GUI
# ฟังก์ชันตรวจสอบว่า user ไม่ใช่ customer
def is_not_customer(user):
    return user.is_authenticated and user.role != "customer"

def index_view(request):
    """ แสดงหน้าหลัก พร้อมรายการสินค้าทั้งหมด แต่ห้ามกดสั่งซื้อ """
    products = Product.objects.all()  # ✅ ดึงสินค้าทั้งหมดจากฐานข้อมูล
    return render(request, 'index.html', {"products": products})


@login_required(login_url='login')
def home_view(request):
    products = Product.objects.all()  # ✅ ดึงสินค้าทั้งหมดจากฐานข้อมูล
    return render(request, "login/home.html" , {"products": products})  # ✅ ชี้ไปที่ templates/login/home.html


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # ✅ ยังไม่บันทึกลงฐานข้อมูล
            user.role = "customer"  # ✅ กำหนดค่า role เป็น "member" อัตโนมัติ
            user.set_password(form.cleaned_data["password1"])  # ✅ เข้ารหัสรหัสผ่าน
            user.save()  # ✅ บันทึกข้อมูลลงฐานข้อมูล
            login(request, user)  # ✅ ล็อกอินอัตโนมัติหลังสมัคร
            return redirect("home")  # ✅ ไปยังหน้า Dashboard
        else:
            messages.error(request, "❌ กรุณาตรวจสอบข้อมูลที่กรอก!")
    else:
        form = RegisterForm()
    
    return render(request, "login/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")  # ✅ เปลี่ยนให้ไปหน้า home หลัง login
        else:
            messages.error(request, "❌ Username หรือ Password ไม่ถูกต้อง!")

    return render(request, "login/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)  # ✅ ลบ session ผู้ใช้ปัจจุบัน
    messages.success(request, "คุณได้ออกจากระบบเรียบร้อยแล้ว")
    return redirect('index')  # ✅ กลับไปหน้า index หลังจากออกจากระบบ



# ป้องกัน customer ไม่ให้เข้าถึงหน้า product list
@login_required
@user_passes_test(is_not_customer, login_url='home')
@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()

    # ✅ Debug: ตรวจสอบค่า URL ของรูปสินค้า
    for product in products:
        print(f"Product: {product.name}, Image URL: {product.image.url if product.image else 'No Image'}")

    return render(request, "products/product_list.html", {"products": products})

@login_required(login_url='login')
def pos_view(request):
    products = Product.objects.all()  # ✅ ดึงสินค้าทั้งหมดจากฐานข้อมูล
    return render(request, "pos.html", {"products": products})

# ป้องกัน customer ไม่ให้เข้าถึงหน้าเพิ่มสินค้า
@login_required
@user_passes_test(is_not_customer, login_url='home')
def add_product(request):
    if request.method == "POST":
        print(request.POST)  # ✅ Debug ดูว่ามีค่าอะไรถูกส่งมา

        name = request.POST.get("name", "")
        description = request.POST.get("description", "")
        price = request.POST.get("price", 0)
        stock = request.POST.get("stock", 0)  
        image = request.FILES.get("image")

        category = request.POST.get("category")  # ตรวจสอบว่า category ถูกดึงมาถูกต้อง
        Product.objects.create(
            seller=request.user,
            name=name,
            description=description,
            price=price,
            stock=int(stock),
            image=image,
            category=category,  # ตรวจสอบว่ามีการเก็บ category
        )

        return redirect("product_list")

    return render(request, "products/add_product.html")


# ✅ แก้ไขสินค้า
@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST["name"]
        product.description = request.POST["description"]
        product.price = request.POST["price"]
        product.stock = request.POST["stock"]
        product.category = request.POST["category"]  # ✅ เพิ่มบรรทัดนี้เพื่ออัปเดตประเภทสินค้า
        product.save()
        return redirect("product_list")

    return render(request, "products/edit_product.html", {"product": product})

# ✅ ลบสินค้า
@login_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # ✅ ถ้าไม่มีสินค้าจะขึ้น 404 ทันที

    if request.method == "POST":
        product.delete()
        return redirect("product_list")  # ✅ กลับไปยังหน้ารายการสินค้า

    return render(request, "products/delete_product.html", {"product": product})

# ✅ อัปเดตราคาและสต๊อกสินค้าแบบ AJAX
from django.http import JsonResponse
@login_required(login_url='login')
def update_product_info(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        field = request.POST["field"]
        value = request.POST["value"]
        
        product = get_object_or_404(Product, id=product_id)

        if field == "price":
            product.price = value
        elif field == "stock":
            product.stock = value
        
        product.save()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)

# ✅ หน้าการตั้งค่า
def settings_view(request):
    return render(request, "products/settings.html")

# ✅ ระบบตะกร้าสินค้า (Shopping Cart)
@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(customer=request.user)
    
    # ✅ คำนวณราคาทั้งหมดของแต่ละสินค้าในตะกร้า และเพิ่มเป็น attribute "total_price"
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # ✅ เพิ่ม total_price
    
    total_price = sum(item.total_price for item in cart_items)  # ✅ คำนวณราคารวมทั้งหมด
    
    return render(request, "cart/cart.html", {"cart_items": cart_items, "total_price": total_price})



@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(customer=request.user, product=product)

    if not created:
        if cart_item.quantity < product.stock:  # ✅ เช็คว่ายังมีสต็อกให้เพิ่มได้
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, f"❌ ไม่สามารถเพิ่ม {product.name} ได้เกิน {product.stock} ชิ้น")
    else:
        if product.stock > 0:
            cart_item.quantity = 1
            cart_item.save()
        else:
            messages.error(request, f"❌ สินค้า {product.name} หมดสต็อก!")

    return redirect("home")


# ✅ ลบสินค้าออกจากตะกร้า
@login_required(login_url='login')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, customer=request.user)
    cart_item.delete()
    messages.success(request, "❌ ลบสินค้าออกจากตะกร้าแล้ว!")
    return redirect("cart_view")

# ✅ อัปเดตจำนวนสินค้าในตะกร้า
@login_required(login_url='login')
def update_cart_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, customer=request.user)
    product = cart_item.product

    if request.method == "POST":
        new_quantity = int(request.POST["quantity"])

        if new_quantity > product.stock:
            messages.error(request, f"❌ จำนวนสินค้าเกินสต็อกสูงสุด ({product.stock} ชิ้น)")
        elif new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "✅ อัปเดตจำนวนสินค้าสำเร็จ!")
        else:
            cart_item.delete()
            messages.success(request, "❌ ลบสินค้าออกจากตะกร้าแล้ว!")

    return redirect("cart_view")



# ✅ ปรับ `checkout` ให้แสดง Alert 
@login_required(login_url='login')
def checkout(request):
    messages.success(request, "✅ สั่งซื้อสำเร็จแล้ว!")
    return redirect("cart_view")  # ✅ กลับไปที่หน้าตะกร้า




# ✅ ระบบคำสั่งซื้อ (Order Management)
@login_required(login_url='login')
def create_order(request):
    cart_items = Cart.objects.filter(customer=request.user)
    if not cart_items.exists():
        messages.error(request, "ตะกร้าของคุณว่างเปล่า!")
        return redirect("cart_view")
    
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order.objects.create(customer=request.user, total_amount=total_amount)
    
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    
    cart_items.delete()  # ล้างตะกร้าหลังสั่งซื้อ
    return redirect("order_list")


@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required(login_url='login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'pending':
        order.delete()
        messages.success(request, "คำสั่งซื้อถูกยกเลิกแล้ว!")
    else:
        messages.error(request, "ไม่สามารถยกเลิกคำสั่งซื้อที่ถูกส่งไปแล้ว!")
    return redirect("order_list")

# ✅ ระบบชำระเงิน (Payment System)
@login_required(login_url='login')
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == "POST":
        payment_method = request.POST["payment_method"]
        transaction_id = request.POST.get("transaction_id", "")
        Payment.objects.create(order=order, payment_method=payment_method, transaction_id=transaction_id, paid=True)
        order.status = "shipped"
        order.save()
        messages.success(request, "การชำระเงินสำเร็จ!")
        return redirect("order_list")
    return render(request, "payments/payment_form.html", {"order": order})

# ✅ ระบบสถิติยอดขาย (Sales Dashboard)
@login_required(login_url='login')
def sales_report(request):
    if not request.user.is_seller():
        return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้!")
    
    orders = Order.objects.filter(orderitem__product__seller=request.user).distinct()
    total_sales = sum(order.total_amount for order in orders)
    return render(request, "reports/sales_report.html", {"total_sales": total_sales, "orders": orders})

@login_required
def confirm_order(request):
    cart_items = Cart.objects.filter(customer=request.user)
    if not cart_items.exists():
        messages.error(request, "❌ ตะกร้าของคุณว่างเปล่า!")
        return redirect("cart_view")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, "orders/confirm_order.html", {  # ✅ แก้ให้ถูกต้อง
        "cart_items": cart_items,
        "total_price": total_price
    })



@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(customer=request.user)
    
    if not cart_items.exists():
        messages.error(request, "❌ ไม่สามารถสร้างคำสั่งซื้อได้เพราะตะกร้าว่างเปล่า!")
        return redirect("cart_view")

    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # ✅ สร้างคำสั่งซื้อใหม่
    order = Order.objects.create(customer=request.user, total_amount=total_amount)

    for item in cart_items:
        product = item.product

        # ✅ ตรวจสอบว่าสต็อกสินค้าพอหรือไม่
        if item.quantity > product.stock:
            messages.error(request, f"❌ สินค้า {product.name} คงเหลือเพียง {product.stock} ชิ้น ไม่สามารถสั่งซื้อได้")
            return redirect("cart_view")

        # ✅ ลดสต็อกสินค้าในฐานข้อมูล
        product.stock -= item.quantity
        product.save()

        # ✅ บันทึกรายการสินค้าในคำสั่งซื้อ
        OrderItem.objects.create(order=order, product=product, quantity=item.quantity, price=item.product.price)

    # ✅ ล้างตะกร้าหลังสั่งซื้อ
    cart_items.delete()

    messages.success(request, "✅ คำสั่งซื้อถูกสร้างเรียบร้อยแล้ว และสต็อกสินค้าถูกอัปเดต!")
    
    return redirect("order_list")


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if request.method == "POST":
        payment_method = request.POST["payment_method"]
        transaction_id = request.POST.get("transaction_id", "")

        # ✅ บันทึกข้อมูลการชำระเงิน
        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            transaction_id=transaction_id,
            paid=True
        )

        order.status = "shipped"  # ✅ อัปเดตสถานะออเดอร์
        order.save()

        messages.success(request, "✅ การชำระเงินสำเร็จ!")
        return redirect("order_list")  # ✅ ไปยังหน้ารายการคำสั่งซื้อ

    return render(request, "payments/payment.html", {"order": order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order_items = order.order_items.all()  # ✅ เรียกจาก related_name ที่ถูกต้อง

    
    return render(request, "orders/order_detail.html", {
        "order": order,
        "order_items": order_items
    })


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from.forms import AdminRegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AdminRegisterForm
from .models import CustomUser

# ตรวจสอบว่าเป็นแอดมินหรือไม่
def is_admin(user):
    return user.is_authenticated and user.is_staff

# ✅ ฟังก์ชันสมัคร Admin
def admin_register_view(request):
    if request.method == "POST":
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "❌ กรุณาตรวจสอบข้อมูลที่กรอก!")
    else:
        form = AdminRegisterForm()

    return render(request, "admin/register.html", {"form": form})

# ✅ ฟังก์ชันเข้าสู่ระบบ Admin
def admin_login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user and user.is_admin():  # ✅ ตรวจสอบว่าเป็น Admin
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "❌ ไม่สามารถเข้าสู่ระบบได้")

    return render(request, "admin/login.html")

# ✅ ออกจากระบบ
def admin_logout(request):
    logout(request)
    return redirect("admin_login")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Product, Order
# ✅ ฟังก์ชันแสดงรายการสินค้า Admin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, Product, CustomUser
import json

# ✅ ฟังก์ชันช่วยแปลง Decimal เป็น float
def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # ✅ แปลง Decimal เป็น float
    raise TypeError

# ป้องกัน customer ไม่ให้เข้าถึง dashboard
@login_required
@user_passes_test(is_not_customer, login_url='home')
def dashboard_view(request):
    # ✅ คำนวณสถิติ
    total_sales = Order.objects.filter(status="delivered").aggregate(total=models.Sum("total_amount"))["total"] or 0
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = CustomUser.objects.filter(role="customer").count()

    # ✅ เตรียมข้อมูลสำหรับกราฟ
    sales_data = Order.objects.values("created_at").annotate(total=models.Sum("total_amount")).order_by("created_at")
    labels = [str(order["created_at"].date()) for order in sales_data]
    data = [order["total"] for order in sales_data]

    return render(request, "products/dashboard.html", {
        "total_sales": total_sales,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "labels": json.dumps(labels),
        "data": json.dumps(data, default=decimal_to_float),
    })

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import StorePayment
from django.utils.timezone import now

def upload_slip(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.payment_slip:
        messages.error(request, "❌ คุณได้อัปโหลดสลิปไปแล้ว ไม่สามารถอัปโหลดซ้ำได้")
        return redirect('order_detail', order_id=order.id)

    if request.method == "POST":
        form = PaymentSlipForm(request.POST, request.FILES)
        if form.is_valid():
            order.payment_slip = form.cleaned_data['payment_slip']
            order.save()  # ✅ ไม่เปลี่ยนสถานะเป็น completed
            messages.success(request, "✅ อัปโหลดสลิปสำเร็จ! รอการอนุมัติจาก Admin")
            return redirect('order_detail', order_id=order.id)
    else:
        form = PaymentSlipForm()

    return render(request, 'payments/upload_slip.html', {'form': form, 'order': order})

from django.contrib.auth.decorators import login_required, user_passes_test



from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from .models import Product, Order, OrderItem, StorePayment
from django.db.models import Sum, Count
from django.utils.timezone import now
from django.db.models.functions import TruncDate

# ✅ Function to convert Matplotlib figures to Base64 for embedding in HTML
def create_chart(figure):
    buffer = io.BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(figure)
    return base64.b64encode(image_png).decode('utf-8')

# ✅ Function to generate the dashboard
def dashboard_view(request):
    try:
        # ✅ 1. Pie Chart - Product Category Distribution
        category_counts = Product.objects.values("category").annotate(total=Count("id"))
        pie_chart = None
        bar_chart = None
        price_histogram = None
        sales_trend_chart = None
        top_products_chart = None
        payment_chart = None
        
        if category_counts:
            df_category = pd.DataFrame(category_counts)
            fig1, ax1 = plt.subplots(figsize=(6, 6))
            ax1.pie(df_category["total"], labels=df_category["category"], autopct="%1.1f%%", startangle=140)
            plt.title("📊 Product Category Distribution")
            pie_chart = create_chart(fig1)
        else:
            pie_chart = None

        # ✅ 2. Bar Chart - Number of Products by Category
        if category_counts:
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.bar(df_category["category"], df_category["total"], color="skyblue")
            plt.title("📦 Product Count by Category")
            plt.xticks(rotation=45)
            bar_chart = create_chart(fig2)
        else:
            bar_chart = None

        # ✅ 3. Histogram - Product Price Distribution
        product_prices = list(Product.objects.values_list("price", flat=True))
        if product_prices:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.histplot(product_prices, bins=10, kde=True, color="green", ax=ax3)
            ax3.set_xlabel("Price (THB)")
            ax3.set_ylabel("Number of Products")
            ax3.set_title("💰 Product Price Distribution")
            price_histogram = create_chart(fig3)
        else:
            price_histogram = None

        # ✅ 4. Line Chart - Sales Trend Over Time
        sales_data = (
            Order.objects.filter(status="delivered")
            .annotate(sale_date=TruncDate("created_at"))  # ✅ Use TruncDate to extract the date
            .values("sale_date")
            .annotate(total_sales=Sum("total_amount"))
            .order_by("sale_date")
        )

        if sales_data:
            df_sales = pd.DataFrame(sales_data)
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            ax4.plot(df_sales["sale_date"], df_sales["total_sales"], marker="o", linestyle="-", color="red")
            ax4.set_xlabel("Date")
            ax4.set_ylabel("Total Sales (THB)")
            ax4.set_title("📈 Daily Sales Trend")
            ax4.grid(True)
            sales_trend_chart = create_chart(fig4)
        else:
            sales_trend_chart = None

        # ✅ 5. Bar Chart - Top 5 Best-Selling Products
        top_products = (
            OrderItem.objects.values("product__name")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")[:5]
        )

        if top_products:
            df_top_products = pd.DataFrame(top_products)
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            ax5.bar(df_top_products["product__name"], df_top_products["total_sold"], color="orange")
            ax5.set_xlabel("Product")
            ax5.set_ylabel("Units Sold")
            ax5.set_title("🏆 Top 5 Best-Selling Products")
            plt.xticks(rotation=45)
            top_products_chart = create_chart(fig5)
        else:
            top_products_chart = None

        # ✅ 6. Pie Chart - Payment Method Distribution
        payment_data = StorePayment.objects.values("payment_method").annotate(total=Count("id"))
        if payment_data:
            df_payment = pd.DataFrame(payment_data)
            fig6, ax6 = plt.subplots(figsize=(6, 6))
            ax6.pie(df_payment["total"], labels=df_payment["payment_method"], autopct="%1.1f%%", startangle=140)
            plt.title("💳 Payment Method Distribution")
            payment_chart = create_chart(fig6)
        else:
            payment_chart = None

        # ✅ Send Charts to Template
        return render(request, "dashboard.html", {
            "pie_chart": pie_chart,
            "bar_chart": bar_chart,
            "price_histogram": price_histogram,
            "sales_trend_chart": sales_trend_chart,
            "top_products_chart": top_products_chart,
            "payment_chart": payment_chart
        })

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@login_required
@user_passes_test(is_admin)
def approve_order(request, order_id):
    """ อนุมัติคำสั่งซื้อ (เปลี่ยนสถานะเป็น 'completed') """
    order = get_object_or_404(Order, id=order_id)  # ✅ ตรวจสอบว่าออเดอร์มีอยู่จริง

    if order.status == "pending":  
        order.approve_order()  # ✅ ใช้ฟังก์ชัน approve_order() ใน models.py
        messages.success(request, f"✅ คำสั่งซื้อ #{order.id} อนุมัติเรียบร้อยแล้ว!")

    return redirect('admin_payment_list')  # ✅ เปลี่ยนให้ Redirect ไปที่หน้า Admin


@login_required
@user_passes_test(is_admin)
def admin_payment_list(request):
    """ แสดงรายการออเดอร์ทั้งหมด และให้กรองตามสถานะ """
    status_filter = request.GET.get('status', '')  # ✅ ดึงค่าจาก dropdown (ค่าเริ่มต้นเป็นค่าว่าง)

    if status_filter and status_filter in ["pending", "completed", "rejected"]:
        orders = Order.objects.filter(status=status_filter)  # ✅ กรองตามสถานะที่เลือก
    else:
        orders = Order.objects.all()  # ✅ ถ้าไม่เลือก ให้แสดงทั้งหมด

    return render(request, 'admin/admin_payment_list.html', {
        'orders': orders,
        'status_filter': status_filter  # ✅ ส่งค่าไปยัง template
    })


import os

@login_required
@user_passes_test(is_admin)
def reject_order(request, order_id):
    """ ❌ ฟังก์ชันให้ Admin กด 'ไม่อนุมัติ' ออเดอร์ """
    order = get_object_or_404(Order, id=order_id)

    if order.payment_slip:
        slip_path = os.path.join(settings.MEDIA_ROOT, str(order.payment_slip))
        if os.path.exists(slip_path):
            os.remove(slip_path)  # ✅ ลบไฟล์จริงจากเซิร์ฟเวอร์
        order.payment_slip.delete()  # ✅ ลบจากฐานข้อมูล

    order.status = "rejected"  # ✅ เปลี่ยนสถานะเป็น 'ไม่อนุมัติ'
    order.save()
    messages.error(request, f"❌ คำสั่งซื้อ #{order.id} ถูกปฏิเสธแล้ว!")

    return redirect('admin_payment_list')  # ✅ กลับไปที่หน้าตรวจสอบการชำระเงิน
