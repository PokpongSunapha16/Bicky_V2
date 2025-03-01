from django.urls import path
#from .views import ProductViewSet
from .views import *

urlpatterns = [
    path("", home_view, name="index"),  # ✅ หน้าแรกต้องมีเส้นทางนี้
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

   # ✅ ระบบจัดการสินค้า
    path("products/", product_list, name="product_list"),
    path("products/add/", add_product, name="add_product"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
    path("products/update/", update_product_info, name="update_product_info"),

    path("pos/", pos_view, name="pos"),  # ✅ เพิ่มเส้นทาง POS
    path("settings/", settings_view, name="settings"),
]