from django.urls import path
from users import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static 


urlpatterns = [

    # Registro y Login/out
    path('register', views.register, name='register'),
    path('',views.loginPage, name= 'login'),
    path('login/',views.loginPage, name= 'login'),
    path('logout/',views.logoutUser, name= 'logout'),
    path('home',views.home, name="home"),
    path('count',views.count, name="count"),
    path('break',views.toggleBreak, name="break"),
    path('reset_counters',views.resetCounters, name="reset_counters"),
]