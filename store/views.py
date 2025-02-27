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
from django.http import HttpResponseForbidden


def admin_or_seller_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_admin() or request.user.is_seller()):
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้!")
        return view_func(request, *args, **kwargs)
    return wrapper

def home_view(request):
    return render(request, "login/home.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")

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