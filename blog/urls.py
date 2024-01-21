from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing, name='landing'),
    path('landing/', views.landingLogin, name='landingLogin'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),   
    path('edit-account/', views.editAccount, 
        name='edit-account'),
]