from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", index_view, name="index"),  # ✅ หน้าแรกคือ index.html
    path("home/", home_view, name="home"),  # ✅ หน้า home หลัง login
    path("logout/", logout_view, name="logout"),  # ✅ Logout แล้วกลับไป indeX
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

    # ✅ ระบบจัดการผู้ใช้
    path("admin/register/", admin_register_view, name="admin_register"),
    path("admin/login/", admin_login_view, name="admin_login"),
    #path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/logout/", admin_logout, name="admin_logout"),


    path("dashboard/", dashboard_view, name="dashboard"),  # ✅ เปลี่ยนเป็น dashboard/


    path('cart/', cart_view, name='cart_view'),  # ✅ ต้องมี path นี้
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_id>/', update_cart_quantity, name='update_cart_quantity'),
    path("cart/checkout/", checkout, name="checkout"),

    path("cart/confirm_order/", confirm_order, name="confirm_order"),
    path("cart/place_order/", place_order, name="place_order"),

    #กบเพิ่มตรงนี้
    path("payment/<int:order_id>/", payment_view, name="payment"),

    path("orders/", order_list, name="order_list"),  # ✅ ต้องมี path นี้
    path("orders/<int:order_id>/", order_detail, name="order_detail"),  # ✅ ต้องมีเส้นทางนี้
    path('upload-slip/', views.upload_slip, name='upload_slip'),



]