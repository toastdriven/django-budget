from django.shortcuts import render_to_response, get_object_or_404
from budget.models import Budget, BudgetCategoryEstimate
from budget.categories.models import Category
from budget.transactions.models import Transaction

def dashboard(request):
    return render_to_response('.html', {})

def year_summary(request):
    return render_to_response('.html', {})

def month_summary(request):
    return render_to_response('.html', {})

def budget_list(request):
    return render_to_response('.html', {})

def budget_add(request):
    return render_to_response('.html', {})

def budget_edit(request):
    return render_to_response('.html', {})

def budget_delete(request):
    return render_to_response('.html', {})

def estimate_list(request):
    return render_to_response('.html', {})

def estimate_add(request):
    return render_to_response('.html', {})

def estimate_edit(request):
    return render_to_response('.html', {})

def estimate_delete(request):
    return render_to_response('.html', {})
