"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import  path

from app import views

urlpatterns = [
    path('',views.home,name='home'),
    
    path('register/',views.Sign_up,name='signUp'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('verify_otp_login/',views.verify_otp_login,name='verify_otp_login'),
    path('task_list/', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:id>/', views.task_update, name='task_update'),
    path('delete/<int:id>/', views.task_delete, name='task_delete'),
    path('task/<int:id>/', views.task_detail, name='task_detail'),
]
