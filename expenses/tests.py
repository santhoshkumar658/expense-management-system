from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch
from rest_framework.test import APIClient

from .forms import BudgetForm, ExpenseForm
from .models import Budget, Category, Expense, Income, SavingsGoal


class FinanceViewsTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='sam', password='test-password-123')
		self.other_user = User.objects.create_user(username='alex', password='test-password-123')
		self.category = Category.objects.create(user=self.user, name='Food')
		self.other_category = Category.objects.create(user=self.other_user, name='Private')
		self.client.login(username='sam', password='test-password-123')

	def test_dashboard_uses_current_month_totals_and_user_records(self):
		today = timezone.localdate()
		Income.objects.create(user=self.user, source='Pay', amount='1000.00', date=today)
		Expense.objects.create(user=self.user, category=self.category, amount='200.00', date=today)
		Income.objects.create(user=self.other_user, source='Other pay', amount='9000.00', date=today)

		response = self.client.get(reverse('dashboard'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['month_income'], Decimal('1000.00'))
		self.assertEqual(response.context['month_expense'], Decimal('200.00'))
		self.assertEqual(response.context['month_net'], Decimal('800.00'))
		self.assertEqual(response.context['category_labels'], ['Food'])

	def test_budget_coach_forecasts_spending_and_warns_over_budget(self):
		forecast_date = date(2026, 10, 10)
		Budget.objects.create(
			user=self.user, amount='200.00', month=date(2026, 10, 1)
		)
		Expense.objects.create(
			user=self.user, category=self.category, amount='120.00', date=forecast_date
		)
		other_category = Category.objects.create(user=self.user, name='Travel')
		Expense.objects.create(
			user=self.user, category=other_category, amount='30.00', date=forecast_date
		)

		with patch('expenses.views.timezone.localdate', return_value=forecast_date):
			response = self.client.get(reverse('dashboard'))

		coach_item = response.context['budget_status'][0]
		self.assertEqual(coach_item['spent'], Decimal('150.00'))
		self.assertEqual(coach_item['projected_spend'], Decimal('465.00'))
		self.assertEqual(coach_item['forecast_overage'], Decimal('265.00'))
		self.assertTrue(coach_item['will_exceed'])
		self.assertContains(response, 'Likely to exceed')

	def test_budget_pages_show_only_selected_month_and_allow_history(self):
		Budget.objects.create(
			user=self.user, amount='200.00', month=date(2026, 10, 14)
		)
		Budget.objects.create(
			user=self.user, amount='150.00', month=date(2026, 9, 1)
		)
		Expense.objects.create(
			user=self.user, category=self.category, amount='75.00', date=date(2026, 9, 20)
		)

		with patch('expenses.views.timezone.localdate', return_value=date(2026, 10, 4)):
			current_response = self.client.get(reverse('budget_list'))
			previous_response = self.client.get(reverse('budget_list'), {'month': '2026-09'})
			status_response = self.client.get(reverse('budget_status'), {'month': '2026-09'})

		self.assertEqual(len(current_response.context['budgets']), 1)
		self.assertEqual(current_response.context['budgets'][0].month, date(2026, 10, 1))
		self.assertEqual(len(previous_response.context['budgets']), 1)
		self.assertEqual(previous_response.context['budgets'][0].amount, Decimal('150.00'))
		self.assertEqual(status_response.context['budget_data'][0]['spent'], Decimal('75.00'))

	def test_budget_form_rejects_second_overall_budget_for_month(self):
		Budget.objects.create(
			user=self.user, amount='200.00', month=date(2026, 10, 1)
		)
		form = BudgetForm(
			data={'amount': '250.00', 'month': '2026-10'},
			user=self.user,
		)

		self.assertFalse(form.is_valid())
		self.assertIn('already have an overall budget', str(form.errors))

	def test_budget_api_rejects_second_overall_budget_for_month(self):
		Budget.objects.create(
			user=self.user, amount='200.00', month=date(2026, 10, 1)
		)
		client = APIClient()
		client.force_authenticate(user=self.user)

		response = client.post(reverse('api_budget_list'), {
			'amount': '250.00',
			'month': '2026-10-20',
		}, format='json')

		self.assertEqual(response.status_code, 400)
		self.assertIn('already have an overall budget', str(response.data))

	def test_transaction_edit_and_delete_are_limited_to_owner(self):
		expense = Expense.objects.create(
			user=self.user, category=self.category, amount='25.00', date=date(2026, 1, 1)
		)
		foreign_expense = Expense.objects.create(
			user=self.other_user, category=self.other_category, amount='50.00', date=date(2026, 1, 1)
		)

		response = self.client.post(reverse('expense_edit', args=[expense.pk]), {
			'category': self.category.pk,
			'amount': '30.00',
			'description': 'Updated',
			'date': '2026-01-02',
		})
		self.assertRedirects(response, reverse('expense_list'))
		expense.refresh_from_db()
		self.assertEqual(expense.amount, Decimal('30.00'))
		self.assertEqual(self.client.get(reverse('expense_edit', args=[foreign_expense.pk])).status_code, 404)

		self.assertRedirects(
			self.client.post(reverse('expense_delete', args=[expense.pk])),
			reverse('expense_list'),
		)
		self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

	def test_expense_form_only_offers_the_users_categories(self):
		form = ExpenseForm(user=self.user)

		self.assertEqual(list(form.fields['category'].queryset), [self.category])

	def test_savings_goal_shows_saved_amount_remaining_and_progress(self):
		goal = SavingsGoal.objects.create(
			user=self.user,
			name='Emergency fund',
			target_amount='1000.00',
			saved_amount='250.00',
		)
		goal.refresh_from_db()

		response = self.client.get(reverse('savings_goal_list'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(goal.remaining_amount, Decimal('750.00'))
		self.assertEqual(goal.progress_percentage, 25)
		self.assertFalse(goal.is_complete)
		self.assertContains(response, 'Emergency fund')
		self.assertContains(response, '₹750.00 remaining')

	def test_savings_goal_create_and_edit_are_limited_to_owner(self):
		self.assertContains(
			self.client.get(reverse('savings_goal_create')),
			'What are you saving for?',
		)
		response = self.client.post(reverse('savings_goal_create'), {
			'name': 'New laptop',
			'target_amount': '800.00',
			'saved_amount': '100.00',
			'target_date': '',
		})
		self.assertRedirects(response, reverse('savings_goal_list'))
		goal = SavingsGoal.objects.get(user=self.user, name='New laptop')
		self.assertEqual(goal.saved_amount, Decimal('100.00'))

		self.assertEqual(
			self.client.get(reverse('savings_goal_edit', args=[goal.pk])).status_code,
			200,
		)
		other_client = Client()
		other_client.login(username='alex', password='test-password-123')
		self.assertEqual(
			other_client.get(reverse('savings_goal_edit', args=[goal.pk])).status_code,
			404,
		)
