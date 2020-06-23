from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views

urlpatterns = [
    path('', include('chat.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout')
]
