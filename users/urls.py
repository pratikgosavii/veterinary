from django.urls import path

from .views import *

urlpatterns = [
    path('login-customer/', LoginView.as_view(), name='login'),
    path('login-admin/', login_admin, name='login_admin'),
    path('signup-customer/', SignupView.as_view(), name='signup'),
    path('logout/', logout_page, name='logout'),
    
    path('user_list/', user_list, name='user_list'),
]
