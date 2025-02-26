from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns  # Import seaborn สำหรับสร้าง Histogram
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def home_view(request):
    return render(request, "login/home.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")

# def dashboard_view(request):
#     try:
#         # โหลดข้อมูล
#         df = pd.read_csv('data/Electric_Vehicle_Population_Data.csv')

#         # ตรวจสอบว่ามีคอลัมน์ที่จำเป็นหรือไม่
#         required_columns = ['Electric Vehicle Type', 'County', 'Electric Range', 'Model Year']
#         for column in required_columns:
#             if column not in df.columns:
#                 return HttpResponse(f"The required column '{column}' is missing.")

#         # Function สำหรับสร้างกราฟและแปลงเป็น Base64
#         def create_chart(figure):
#             buffer = io.BytesIO()
#             plt.savefig(buffer, format='png')
#             buffer.seek(0)
#             image_png = buffer.getvalue()
#             buffer.close()
#             plt.close(figure)
#             return base64.b64encode(image_png).decode('utf-8')

#         # 1. Pie Chart - Electric Vehicle Type Distribution
#         fig1, ax1 = plt.subplots(figsize=(6, 6))
#         df['Electric Vehicle Type'].value_counts().plot(
#             kind='pie', 
#             autopct='%1.1f%%', 
#             ax=ax1,
#             fontsize=12
#         )
#         plt.title("Electric Vehicle Type Distribution")
#         plt.ylabel('')
#         pie_chart = create_chart(fig1)

#         # 2. Bar Chart - Count of Electric Vehicle Types
#         fig2, ax2 = plt.subplots(figsize=(8, 5))
#         df['Electric Vehicle Type'].value_counts().plot(kind='bar', ax=ax2, color='skyblue')
#         plt.title('Count of Electric Vehicle Types')
#         plt.xticks(rotation=45)
#         bar_chart = create_chart(fig2)

#         # 3. County Distribution Chart
#         county_counts = df.groupby('County').size().reset_index(name='Electric Vehicle Count')
#         county_counts = county_counts.sort_values(by='Electric Vehicle Count', ascending=False).head(10)
#         fig3, ax3 = plt.subplots(figsize=(10, 6))
#         ax3.bar(county_counts['County'], county_counts['Electric Vehicle Count'], color='skyblue')
#         ax3.set_xlabel('County')
#         ax3.set_ylabel('Electric Vehicle Count')
#         ax3.set_title('Distribution of Electric Vehicles by County')
#         plt.xticks(rotation=90)
#         county_chart = create_chart(fig3)

#         # 4. Histogram - Electric Range
#         fig4, ax4 = plt.subplots(figsize=(10, 6))
#         sns.histplot(df['Electric Range'], bins=20, kde=True, color='red', ax=ax4)
#         ax4.set_xlabel('Electric Range (miles)')
#         ax4.set_ylabel('Frequency')
#         ax4.set_title('Distribution of Electric Range for Electric Vehicles')
#         electric_range_chart = create_chart(fig4)

#         # 5. Line Chart - Trend in Electric Vehicle Manufacturing
#         yearly_counts = df.groupby('Model Year').size().reset_index(name='Electric Vehicle Count')
#         fig5, ax5 = plt.subplots(figsize=(10, 6))
#         ax5.plot(yearly_counts['Model Year'], yearly_counts['Electric Vehicle Count'], marker='o', color='red')
#         ax5.set_xlabel('Model Year')
#         ax5.set_ylabel('Electric Vehicle Count')
#         ax5.set_title('Trend in Electric Vehicle Manufacturing Over Time')
#         ax5.grid(True)
#         trend_chart = create_chart(fig5)

#         # ส่งกราฟไปยัง Template
#         return render(request, 'dash1.html', {
#             'pie_chart': pie_chart,
#             'bar_chart': bar_chart,
#             'county_chart': county_chart,
#             'electric_range_chart': electric_range_chart,
#             'trend_chart': trend_chart
#         })

#     except FileNotFoundError:
#         return HttpResponse("Data file not found.")
#     except pd.errors.EmptyDataError:
#         return HttpResponse("Data file is empty.")
#     except Exception as e:
#         return HttpResponse(f"An unexpected error occurred: {str(e)}")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # ✅ ยังไม่บันทึกลงฐานข้อมูล
            user.role = "member"  # ✅ กำหนดค่า role เป็น "member" อัตโนมัติ
            user.set_password(form.cleaned_data["password1"])  # ✅ เข้ารหัสรหัสผ่าน
            user.save()  # ✅ บันทึกข้อมูลลงฐานข้อมูล
            login(request, user)  # ✅ ล็อกอินอัตโนมัติหลังสมัคร
            return redirect("product_list")  # ✅ ไปยังหน้า Dashboard
        else:
            messages.error(request, "❌ กรุณาตรวจสอบข้อมูลที่กรอก!")
    else:
        form = RegisterForm()
    
    return render(request, "login/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]  # ✅ ต้องใช้ username เท่านั้น
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)  # ✅ ตรวจสอบข้อมูล

        if user:
            login(request, user)  # ✅ ล็อกอิน
            return redirect("product_list")  # ✅ ไปยังหน้า Dashboard
        else:
            messages.error(request, "❌ Username หรือ Password ไม่ถูกต้อง!")

    return render(request, "login/login.html")


def logout_view(request):
    logout(request)
    return redirect("login/login.html")



# ✅ แสดงรายการสินค้า
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})

# ✅ เพิ่มสินค้าใหม่
@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        stock = request.POST["stock"]

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            seller=request.user  # ✅ กำหนด seller เป็น User ที่ล็อกอินอยู่
        )
        return redirect("product_list")

    return render(request, "products/add_product.html")


# ✅ แก้ไขสินค้า
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.name = request.POST["name"]
        product.description = request.POST["description"]
        product.price = request.POST["price"]
        product.stock = request.POST["stock"]
        product.save()
        return redirect("product_list")

    return render(request, "products/edit_product.html", {"product": product})

# ✅ ลบสินค้า
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # ✅ ถ้าไม่มีสินค้าจะขึ้น 404 ทันที

    if request.method == "POST":
        product.delete()
        return redirect("product_list")  # ✅ กลับไปยังหน้ารายการสินค้า

    return render(request, "products/delete_product.html", {"product": product})