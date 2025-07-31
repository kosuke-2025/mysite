from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "myapp"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('user/', views.UserHomeView.as_view(), name="user_home"),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
]
