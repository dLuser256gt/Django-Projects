from django.urls import path
from .views import CustomLoginView, dashboard, register_request
from .views import IncomeListView, IncomeCreateView, IncomeUpdateView, IncomeDeleteView

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("register", register_request, name="register"),
    path('income/', IncomeListView.as_view(), name='income_list'),
    path('income/new/', IncomeCreateView.as_view(), name='income_create'),
    path('income/<int:pk>/edit/', IncomeUpdateView.as_view(), name='income_update'),
    path('income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income_delete'),
]