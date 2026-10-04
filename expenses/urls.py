from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'income/add/',
        views.income_create,
        name='income_create'
    ),

    path(
        'income/',
        views.income_list,
        name='income_list'
    ),
    path('income/<int:pk>/edit/', views.income_edit, name='income_edit'),
    path('income/<int:pk>/delete/', views.income_delete, name='income_delete'),

    path(
        'expense/add/',
        views.expense_create,
        name='expense_create'
    ),

    path(
        'expense/',
        views.expense_list,
        name='expense_list'
    ),
    path('expense/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path(
        'categories/add/',
        views.category_create,
        name='category_create'
    ),

    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('savings-goals/', views.savings_goal_list, name='savings_goal_list'),
    path('savings-goals/add/', views.savings_goal_create, name='savings_goal_create'),
    path('savings-goals/<int:pk>/edit/', views.savings_goal_edit, name='savings_goal_edit'),
    path('savings-goals/<int:pk>/delete/', views.savings_goal_delete, name='savings_goal_delete'),
    path(
       'budgets/add/',
       views.budget_create,
       name='budget_create'
    ),

    path(
       'budgets/',
       views.budget_list,
       name='budget_list'
     ),
        path('budgets/<int:pk>/edit/', views.budget_edit, name='budget_edit'),
        path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path(
    'budget-status/',
    views.budget_status,
    name='budget_status'
     ),
]