from xml.etree.ElementInclude import include

from django.urls import path

from . import views

urlpatterns = [
    path(
        'expenses/',
        views.ExpenseListAPIView.as_view(),
        name='api_expense_list'
    ),
    path(
        'expenses/<int:pk>/',
        views.ExpenseDetailAPIView.as_view(),
        name='api_expense_detail'
    ),
    path(
        'income/',
        views.IncomeListAPIView.as_view(),
        name='api_income_list'

    ),
    path(
        'income/<int:pk>/',
        views.IncomeDetailAPIView.as_view(),
        name='api_income_detail'
    ),

    path(
        'categories/',
        views.CategoryListAPIView.as_view(),
        name='api_category_list'
    ),
    path(
    'categories/<int:pk>/',
    views.CategoryDetailAPIView.as_view(),
    name='api_category_detail'
    ),

    path(
    'budgets/',
    views.BudgetListAPIView.as_view(),
    name='api_budget_list'
    ),

    path(
    'budgets/<int:pk>/',
    views.BudgetDetailAPIView.as_view(),
    name='api_budget_detail'
    ),
]