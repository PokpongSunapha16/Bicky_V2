from django.urls import path
from .views import home_view, dashboard_view, register_view, login_view, logout_view

urlpatterns = [
    path("", home_view, name="home"),  # ✅ หน้าแรกต้องมีเส้นทางนี้
    path("dashboard/", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
