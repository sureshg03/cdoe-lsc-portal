from django.urls import path
from .views import LSCLoginView, LSCLogoutView, ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'lsc_auth'

urlpatterns = [
    path('login/', LSCLoginView.as_view(), name='login'),
    path('logout/', LSCLogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]