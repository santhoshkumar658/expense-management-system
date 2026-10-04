from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Income, Expense, Budget, SavingsGoal
from django.contrib import admin
from .models import Category, Income, Expense, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name',)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount', 'date')
    search_fields = ('source',)
    list_filter = ('date',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')
    search_fields = ('description',)
    list_filter = ('category', 'date')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'month')
    list_filter = ('month',)


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'saved_amount', 'target_amount', 'target_date')
    search_fields = ('name', 'user__username')