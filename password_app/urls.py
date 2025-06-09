from django.urls import path
from .views import GeneratePasswordView

app_name = 'password_app'

urlpatterns = [
    path('generate/', GeneratePasswordView.as_view(), name='generate_password'),
]