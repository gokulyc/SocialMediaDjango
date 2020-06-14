"""SocialMedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import Connect.views as cview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cview.Login, name = "login"),
    path('Register/', cview.Register, name = "register"),
    path('in/<str:Username>/', cview.UserProfile, name = "UserProfile"),
    path('in/edit/<str:Username>/', cview.Update_User_Details, name = "EditUserProfile"),
    path('logout/', cview.logout_page, name="logoutpage"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
