from django.urls import path

from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [



    # path('add-day_care/', add_day_care, name='add_day_care'),
    # path('update-day_care/<int:day_care_id>/', update_day_care, name='update_day_care'),
    # path('list-day_care/', list_day_care, name='list_day_care'),
    # path('delete-day_care/<int:day_care_id>/', delete_day_care, name='delete_day_care'),
    path('get-day_care/', get_day_care.as_view(), name='get_day_care'),

    path('login-day-care/', day_care_login.as_view(), name='login_day_care'),
    path('signup-day-care/', day_care_signup.as_view(), name='signup_day_care'),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)