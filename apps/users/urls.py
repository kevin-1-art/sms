from django.urls import path
from apps.users.views import login_view, logout_view, password_reset_view, set_password_view

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('set-password/', set_password_view, name='set_password'),
]
