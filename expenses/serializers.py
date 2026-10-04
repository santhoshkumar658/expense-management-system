from rest_framework import serializers
from .models import Category, Expense, Income , Budget


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = [
            'id',
            'category',
            'amount',
            'description',
            'date',
        ]

    def validate_category(self, category):

        request = self.context.get('request')

        if request and category.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own categories."
            )

        return category

    def validate_amount(self, amount):

        if amount <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return amount

class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = [
            'id',
            'amount',
            'source',
            'description',
            'date',
        ]

    def validate_amount(self, amount):

        if amount <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return amount

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]

class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = [
            'id',
            'amount',
            'month',
        ]

    def validate_amount(self, amount):

        if amount <= 0:
            raise serializers.ValidationError(
                "Budget amount must be greater than zero."
            )

        return amount

    def validate(self, attrs):
        request = self.context.get('request')
        month = attrs.get('month', getattr(self.instance, 'month', None))

        if request and month:
            existing = Budget.objects.filter(
                user=request.user,
                month__year=month.year,
                month__month=month.month,
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError({
                    'month': 'You already have an overall budget for that month.'
                })

        return attrs