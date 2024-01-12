from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('home/',views.home,name="home"),
    path('settings/',views.setting,name="settings")
]
