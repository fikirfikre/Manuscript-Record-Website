from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('',views.home,name="home"),
    path('settings/',views.setting,name="settings"),
    path('logout/',views.logoutPage,name="logout")
]
