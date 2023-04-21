from django.urls import path
from .views import CustomLoginView, dashboard, register_request

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("register", register_request, name="register"),
]