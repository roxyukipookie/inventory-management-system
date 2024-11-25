from django.urls import path
from .views import login_view, signup
from . import views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('', views.redirect_to_login, name='home'),
]
