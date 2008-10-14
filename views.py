from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from budget.models import Budget, BudgetEstimate
from budget.categories.models import Category
from budget.transactions.models import Transaction

def dashboard(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def year_summary(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def month_summary(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def budget_list(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def budget_add(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def budget_edit(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def budget_delete(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def estimate_list(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def estimate_add(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def estimate_edit(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))

def estimate_delete(request):
    return render_to_response('.html', {}, context_instance=RequestContext(request))
