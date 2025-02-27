from django.urls import path
#from .views import ProductViewSet
from .views import (home_view, dashboard_view, register_view, login_view, logout_view,
                    product_list, add_product, edit_product, delete_product,view_cart

)

urlpatterns = [
    path("", home_view, name="home"),  # ✅ หน้าแรกต้องมีเส้นทางนี้
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

   # ✅ ระบบจัดการสินค้า
    path("products/", product_list, name="product_list"),
    path("products/add/", add_product, name="add_product"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),

    path("products/", view_cart, name="view_cart"),
]