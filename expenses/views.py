import calendar
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP

from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import IncomeForm, ExpenseForm,CategoryForm,BudgetForm,SavingsGoalForm
from .models import Income, Expense,Category,Budget,SavingsGoal
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, ExpenseSerializer, IncomeSerializer ,BudgetSerializer
from rest_framework.permissions import IsAuthenticated


@login_required
def income_create(request):

    if request.method == 'POST':

        form = IncomeForm(request.POST, user=request.user)

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()

            return redirect('income_list')

    else:

        form = IncomeForm(user=request.user)

    return render(
        request,
        'expenses/income_form.html',
        {'form': form}
    )


@login_required
def income_list(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'expenses/income_list.html',
        {'incomes': incomes}
    )


@login_required
def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    form = IncomeForm(request.POST or None, instance=income, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('income_list')
    return render(request, 'expenses/income_form.html', {'form': form, 'is_edit': True})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'expenses/delete_confirm.html', {
        'object_name': income.source,
        'cancel_url': 'income_list',
        'page_title': 'Delete income',
    })

@login_required
def expense_create(request):

    if request.method == 'POST':

        form = ExpenseForm(request.POST, user=request.user)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            return redirect('expense_list')

    else:

        form = ExpenseForm(user=request.user)

    return render(
        request,
        'expenses/expense_form.html',
        {'form': form}
    )

@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date')

    return render(
        request,
        'expenses/expense_list.html',
        {'expenses': expenses}
    )


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'expenses/expense_form.html', {'form': form, 'is_edit': True})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/delete_confirm.html', {
        'object_name': expense.category.name,
        'cancel_url': 'expense_list',
        'page_title': 'Delete expense',
    })

@login_required
def category_create(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST, user=request.user)

        if form.is_valid():

            category = form.save(commit=False)

            category.user = request.user

            category.save()

            return redirect('category_list')

    else:

        form = CategoryForm(user=request.user)

    return render(
        request,
        'expenses/category_form.html',
        {'form': form}
    )


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    form = CategoryForm(request.POST or None, instance=category, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'expenses/category_form.html', {'form': form, 'is_edit': True})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'expenses/delete_confirm.html', {
        'object_name': category.name,
        'cancel_url': 'category_list',
        'page_title': 'Delete category',
        'related_warning': 'Deleting a category also permanently removes its linked expenses and budgets.',
    })

@login_required
def category_list(request):

    categories = Category.objects.filter(
        user=request.user
    ).order_by('name')

    return render(
        request,
        'expenses/category_list.html',
        {'categories': categories}
    )


@login_required
def savings_goal_list(request):
    goals = SavingsGoal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'expenses/savings_goal_list.html', {'goals': goals})


@login_required
def savings_goal_create(request):
    form = SavingsGoalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        goal = form.save(commit=False)
        goal.user = request.user
        goal.save()
        return redirect('savings_goal_list')
    return render(request, 'expenses/savings_goal_form.html', {'form': form})


@login_required
def savings_goal_edit(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    form = SavingsGoalForm(request.POST or None, instance=goal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('savings_goal_list')
    return render(request, 'expenses/savings_goal_form.html', {
        'form': form,
        'is_edit': True,
        'goal': goal,
    })


@login_required
def savings_goal_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        return redirect('savings_goal_list')
    return render(request, 'expenses/delete_confirm.html', {
        'object_name': goal.name,
        'cancel_url': 'savings_goal_list',
        'page_title': 'Delete savings goal',
    })

@login_required
def budget_create(request):

    if request.method == 'POST':

        form = BudgetForm(request.POST, user=request.user)

        if form.is_valid():

            budget = form.save(commit=False)

            budget.user = request.user

            budget.save()

            return redirect('budget_list')

    else:

        form = BudgetForm(user=request.user)

    return render(
        request,
        'expenses/budget_form.html',
        {'form': form}
    )


@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    form = BudgetForm(request.POST or None, instance=budget, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('budget_list')
    return render(request, 'expenses/budget_form.html', {'form': form, 'is_edit': True})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'expenses/delete_confirm.html', {
        'object_name': f'{budget.month:%B %Y} overall budget',
        'cancel_url': 'budget_list',
        'page_title': 'Delete budget',
    })

@login_required
def budget_list(request):
    selected_month = _selected_budget_month(request)

    budgets = Budget.objects.filter(
        user=request.user,
        month__year=selected_month.year,
        month__month=selected_month.month,
    )

    return render(
        request,
        'expenses/budget_list.html',
        {
            'budgets': budgets,
            'selected_month': selected_month,
            'available_months': _available_budget_months(request.user, selected_month),
        }
    )

@login_required
def budget_status(request):
    selected_month = _selected_budget_month(request)
    today = timezone.localdate()

    budget = Budget.objects.filter(
        user=request.user,
        month__year=selected_month.year,
        month__month=selected_month.month,
    ).first()
    budget_data = []
    if budget:
        total_spent = Expense.objects.filter(
            user=request.user,
            date__year=budget.month.year,
            date__month=budget.month.month,
            date__lte=today,
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        remaining = budget.amount - total_spent

        if budget.amount > 0:
            percentage_used = (
                total_spent / budget.amount
            ) * 100
        else:
            percentage_used = 0

        if total_spent > budget.amount:
            status = 'Budget Exceeded'
        else:
            status = 'Within Budget'

        budget_data.append({
            'category': 'Overall monthly budget',
            'budget': budget.amount,
            'spent': total_spent,
            'remaining': remaining,
            'percentage_used': percentage_used,
            'progress': min(max(float(percentage_used), 0), 100),
            'month': budget.month,
            'status': status,
        })

    return render(
        request,
        'expenses/budget_status.html',
        {
            'budget_data': budget_data,
            'selected_month': selected_month,
            'available_months': _available_budget_months(request.user, selected_month),
        }
    )


def _selected_budget_month(request):
    try:
        return datetime.strptime(request.GET.get('month', ''), '%Y-%m').date().replace(day=1)
    except ValueError:
        return timezone.localdate().replace(day=1)


def _available_budget_months(user, selected_month):
    months = set(Budget.objects.filter(user=user).dates('month', 'month', order='DESC'))
    months.update((timezone.localdate().replace(day=1), selected_month))
    return sorted(months, reverse=True)

@login_required
def dashboard(request):
    today = timezone.localdate()
    current_income = Income.objects.filter(
        user=request.user, date__year=today.year, date__month=today.month, date__lte=today
    )
    current_expenses = Expense.objects.filter(
        user=request.user, date__year=today.year, date__month=today.month, date__lte=today
    )
    month_income = current_income.aggregate(total=Sum('amount'))['total'] or 0
    month_expense = current_expenses.aggregate(total=Sum('amount'))['total'] or 0

    total_income = Income.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expense = Expense.objects.filter(
        user=request.user
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expense

    category_expenses = current_expenses.values(
        'category_id', 'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')
    spending_by_category = {
        item['category_id']: item['total'] for item in category_expenses
    }

    max_spend = max((item['total'] or 0) for item in category_expenses) if category_expenses else 0

    monthly_labels = []
    monthly_income = []
    monthly_expenses = []
    for offset in range(5, -1, -1):
        month_index = today.month - offset
        year = today.year + (month_index - 1) // 12
        month = (month_index - 1) % 12 + 1
        monthly_labels.append(date(year, month, 1).strftime('%b'))
        monthly_income.append(float(Income.objects.filter(
            user=request.user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0))
        monthly_expenses.append(float(Expense.objects.filter(
            user=request.user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0))

    recent_transactions = [
        {
            'kind': 'Income', 'title': income.source, 'detail': 'Income',
            'amount': income.amount, 'date': income.date,
        }
        for income in Income.objects.filter(user=request.user).order_by('-date')[:8]
    ] + [
        {
            'kind': 'Expense', 'title': expense.category.name, 'detail': expense.description,
            'amount': expense.amount, 'date': expense.date,
        }
        for expense in Expense.objects.filter(user=request.user).select_related('category').order_by('-date')[:8]
    ]
    recent_transactions.sort(key=lambda item: item['date'], reverse=True)

    budget_status = []
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    monthly_budget = Budget.objects.filter(
        user=request.user, month__year=today.year, month__month=today.month
    ).first()
    if monthly_budget:
        spent = month_expense
        used = float(spent / monthly_budget.amount * 100) if monthly_budget.amount else 0
        projected_spend = (spent * days_in_month / today.day).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        budget_status.append({
            'category': 'Overall monthly budget',
            'amount': monthly_budget.amount,
            'spent': spent,
            'progress': min(max(used, 0), 100),
            'percentage_used': used,
            'projected_spend': projected_spend,
            'will_exceed': projected_spend > monthly_budget.amount,
            'forecast_overage': max(projected_spend - monthly_budget.amount, Decimal('0.00')),
        })

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'month_income': month_income,
        'month_expense': month_expense,
        'month_net': month_income - month_expense,
        'category_expenses': category_expenses,
        'category_labels': [item['category__name'] for item in category_expenses],
        'category_values': [float(item['total'] or 0) for item in category_expenses],
        'max_spend': max_spend,
        'monthly_labels': monthly_labels,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'recent_transactions': recent_transactions[:8],
        'budget_status': budget_status,
        'current_month': today.strftime('%B %Y'),
    }

    return render(request, 'expenses/dashboard.html', context)


#API view

class ExpenseListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

       expenses = Expense.objects.filter(
          user=request.user
       ).order_by('-date')

       category = request.GET.get('category')
       date = request.GET.get('date')
       min_amount = request.GET.get('min_amount')
       max_amount = request.GET.get('max_amount')
       search = request.GET.get('search')

       if category:
        expenses = expenses.filter(
            category_id=category
        )

       if date:
        expenses = expenses.filter(
            date=date
        )

       if min_amount:
        expenses = expenses.filter(
            amount__gte=min_amount
        )

       if max_amount:
        expenses = expenses.filter(
            amount__lte=max_amount
        )
        if search:
          expenses = expenses.filter(
          description__icontains=search
        )

       serializer = ExpenseSerializer(
        expenses,
        many=True
       )

    return Response(serializer.data)

    def post(self, request):

        serializer = ExpenseSerializer(
        data=request.data,
        context={'request': request}
        )

        if serializer.is_valid():

            expense = serializer.save(
                user=request.user
            )

            return Response(
                ExpenseSerializer(expense).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )

class ExpenseDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        expense = get_object_or_404(
            Expense,
            id=pk,
            user=request.user
        )

        serializer = ExpenseSerializer(expense)

        return Response(serializer.data)

    def put(self, request, pk):

        expense = get_object_or_404(
            Expense,
            id=pk,
            user=request.user
        )

        serializer = ExpenseSerializer(
        expense,
        data=request.data,
        context={'request': request}
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def patch(self, request, pk):

        expense = get_object_or_404(
            Expense,
            id=pk,
            user=request.user
        )

        serializer = ExpenseSerializer(
            expense,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        expense = get_object_or_404(
            Expense,
            id=pk,
            user=request.user
        )

        expense.delete()

        return Response(status=204)

class IncomeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        incomes = Income.objects.filter(
            user=request.user
        ).order_by('-date')

        serializer = IncomeSerializer(
            incomes,
            many=True
        )
        return Response(serializer.data)
    def post(self,request):

        serializer = IncomeSerializer(
            data=request.data
        )

        if serializer.is_valid():
            income = serializer.save(
                user = request.user

            )
            return Response(
                IncomeSerializer(income).data,
                status=201

            )
        return Response(
            serializer.errors,
            status=400

        )

class IncomeDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        income = get_object_or_404(
            Income,
            id=pk,
            user=request.user
        )

        serializer = IncomeSerializer(income)

        return Response(serializer.data)

    def put(self, request, pk):

        income = get_object_or_404(
            Income,
            id=pk,
            user=request.user
        )

        serializer = IncomeSerializer(
            income,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def patch(self, request, pk):

        income = get_object_or_404(
            Income,
            id=pk,
            user=request.user
        )

        serializer = IncomeSerializer(
            income,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        income = get_object_or_404(
            Income,
            id=pk,
            user=request.user
        )

        income.delete()

        return Response(status=204)

class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        categories =Category.objects.filter(
            user=request.user
        ).order_by('name')

        serializer = CategorySerializer(
            categories,
            many=True
        )
        return Response(serializer.data)

    def post(self,request):
        serializer = CategorySerializer(
            data=request.data
        )
        if serializer.is_valid():
            category = serializer.save(
                user=request.user
            )
            return Response(
                CategorySerializer(category).data,
                status=201
            )
        return Response(
            serializer.errors,
            status=400
        )

class CategoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        category = get_object_or_404(
            Category,
            id=pk,
            user=request.user
        )

        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def put(self, request, pk):

        category = get_object_or_404(
            Category,
            id=pk,
            user=request.user
        )

        serializer = CategorySerializer(
            category,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def patch(self, request, pk):

        category = get_object_or_404(
            Category,
            id=pk,
            user=request.user
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        category = get_object_or_404(
            Category,
            id=pk,
            user=request.user
        )

        category.delete()

        return Response(status=204)

class BudgetListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(
            user=request.user
        ).order_by('-month')

        serializer = BudgetSerializer(
            budgets,
            many=True
        )
        return Response(serializer.data)
    def post(self, request):

        serializer = BudgetSerializer(
        data=request.data,
        context={'request': request}
        )

        if serializer.is_valid():

            budget = serializer.save(
                user=request.user
            )

            return Response(
                BudgetSerializer(budget).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )
class BudgetDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        budget = get_object_or_404(
            Budget,
            id=pk,
            user=request.user
        )

        serializer = BudgetSerializer(budget)

        return Response(serializer.data)

    def put(self, request, pk):

        budget = get_object_or_404(
            Budget,
            id=pk,
            user=request.user
        )

        serializer = BudgetSerializer(
            budget,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def patch(self, request, pk):

        budget = get_object_or_404(
            Budget,
            id=pk,
            user=request.user
        )

        serializer = BudgetSerializer(
            budget,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):

        budget = get_object_or_404(
            Budget,
            id=pk,
            user=request.user
        )

        budget.delete()

        return Response(status=204)