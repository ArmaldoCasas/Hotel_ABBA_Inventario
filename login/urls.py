from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('registrar',views.create_user_view, name='registrar'),
    path('inicio', views.inicio_view, name='inicio'),]