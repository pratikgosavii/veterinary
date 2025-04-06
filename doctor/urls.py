from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [



    # path('add-doctor/', add_doctor, name='add_doctor'),
    # path('update-doctor/<int:doctor_id>/', update_doctor, name='update_doctor'),
    # path('list-doctor/', list_doctor, name='list_doctor'),
    # path('delete-doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),
    path('get-doctor/', get_doctor.as_view(), name='get_doctor'),

    path('login-doctor/', doctor_login.as_view(), name='login_doctor'),
    path('signup-doctor/', doctor_signup.as_view(), name='signup_doctor'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)