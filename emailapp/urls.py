from django.urls import path
from .views import *

urlpatterns = [
    path('regis/',regis),
    path('email_send/',email_send),
    path('regist/',regist),
    path('verify/<auth_token>',verify),
    path('login/',login)


]