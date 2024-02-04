from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('',views.home,name="home"),
    path('settings/',views.setting,name="settings"),
    path('logout/',views.logoutPage,name="logout"),
    path('manuscriptform/',views.manuscriptFormPage, name='manuscriptform'),
    path('languageform/',views.LanguageFormPage,name="languageform"),
    path('generform/',views.GenerFormPage,name='generform'),
    path('reporitoryform/',views.RepositoryFormPage,name="repositoryform"),
    path('repositoryLocationform/',views.RepositoryLocationFormPage,name="repositoryLocationform"),
    path('repositoryOwnerform/',views.RepositoryOwnerFormpage,name="repositoryownerform"),
    path('detail/<int:pk>',views.detail,name="detail")
]
