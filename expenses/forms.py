from django import forms
from django.utils import timezone
from .models import Income, Expense,Category,Budget,SavingsGoal


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'


class IncomeForm(StyledModelForm):

    class Meta:
        model = Income
        fields = ['amount', 'source', 'description', 'date']

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['source'].widget.attrs.update({'placeholder': 'e.g. Salary'})
            self.fields['description'].widget.attrs.update({'rows': 3, 'placeholder': 'Add a note (optional)'})

class ExpenseForm(StyledModelForm):

    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
            self.fields['description'].widget.attrs.update({'rows': 3, 'placeholder': 'Add a note (optional)'})

class CategoryForm(StyledModelForm):

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['name'].widget.attrs.update({'placeholder': 'e.g. Groceries'})


class BudgetForm(StyledModelForm):
    month = forms.DateField(
        input_formats=('%Y-%m',),
        widget=forms.DateInput(
            format='%Y-%m',
            attrs={'type': 'month'},
        ),
    )

    class Meta:
        model = Budget
        fields = ['amount', 'month']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            if not self.instance.pk:
                self.initial.setdefault('month', timezone.localdate().replace(day=1))

    def clean_month(self):
        return self.cleaned_data['month'].replace(day=1)

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        month = cleaned_data.get('month')
        if self.user is not None and month is not None:
            existing = Budget.objects.filter(
                user=self.user,
                month__year=month.year,
                month__month=month.month,
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                self.add_error('month', 'You already have an overall budget for that month.')
        return cleaned_data


class SavingsGoalForm(StyledModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'saved_amount', 'target_date']
        labels = {
            'name': 'What are you saving for?',
            'target_amount': 'Savings target',
            'saved_amount': 'Amount saved so far',
            'target_date': 'Target date (optional)',
        }
        help_texts = {
            'saved_amount': 'You can update this amount as you save.',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Emergency fund, laptop, or vacation',
            }),
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }
