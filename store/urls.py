from django.urls import path
from .views import *


urlpatterns = [
    path("", index_view, name="index"),  # ✅ หน้าแรกคือ index.html
    path("home/", home_view, name="home"),  # ✅ หน้า home หลัง login
    path("logout/", logout_view, name="logout"),  # ✅ Logout แล้วกลับไป indeX

    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),


   # ✅ ระบบจัดการสินค้า
    path("products/", product_list, name="product_list"),
    path("products/add/", add_product, name="add_product"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
    path("products/update/", update_product_info, name="update_product_info"),

    path("pos/", pos_view, name="pos"),  # ✅ เพิ่มเส้นทาง POS
    path("settings/", settings_view, name="settings"),


    path('cart/', cart_view, name='cart_view'),  # ✅ ต้องมี path นี้
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_id>/', update_cart_quantity, name='update_cart_quantity'),
    path("cart/checkout/", checkout, name="checkout"),

]