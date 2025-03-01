from django.urls import path
from .views import *

from django.urls import path
from .views import *

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
]