import datetime
from decimal import Decimal
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from budget.models import Budget, BudgetEstimate
from budget.categories.models import Category
from budget.transactions.models import Transaction
from budget.forms import BudgetEstimateForm, BudgetForm

def dashboard(request):
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
    budget = Budget.active.most_current_for_date(datetime.datetime.today())
    
    latest_debits = Transaction.debits.get_latest()
    latest_credits = Transaction.credits.get_latest()
    
    estimated_amount = budget.monthly_estimated_total()
    amount_used = budget.actual_total(start_date, end_date)
    progress_bar_percent = int(amount_used / estimated_amount * 100)
    
    if progress_bar_percent >= 100:
        progress_bar_level = 'red'
        progress_bar_percent = 100
    elif progress_bar_percent >= 75:
        progress_bar_level = 'yellow'
    else:
        progress_bar_level = 'green'
    
    return render_to_response('budget/dashboard.html', {
        'budget': budget,
        'latest_debits': latest_debits,
        'latest_credits': latest_credits,
        'estimated_amount': estimated_amount,
        'amount_used': amount_used,
        'progress_bar_percent': progress_bar_percent,
        'progress_bar_level': progress_bar_level,
    }, context_instance=RequestContext(request))

def setup(request):
    return render_to_response('budget/setup.html', {}, context_instance=RequestContext(request))

def summary_list(request):
    dates = []
    
    try:
        # import pdb; pdb.set_trace()
        oldest_date = Transaction.active.order_by('date')[0].date
        newest_date = Transaction.active.order_by('-date')[0].date
        current_date = datetime.date(oldest_date.year, oldest_date.month, 1)
        
        while current_date <= newest_date:
            dates.append(datetime.date(current_date.year, current_date.month, 1))
            current_year, current_month = current_date.year, current_date.month
            
            if current_month >= 12:
                current_month = 1
                current_year += 1
            
            current_date = datetime.date(current_year, current_month + 1, 1)
    except IndexError:
        # Just don't populate the dates.
        pass
    
    return render_to_response('budget/summaries/summary_list.html', {
        'dates': dates,
    }, context_instance=RequestContext(request))

def summary_year(request, year):
    start_date = datetime.date(int(year), 1, 1)
    end_date = datetime.date(int(year), 12, 31)
    budget = Budget.active.most_current_for_date(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    return render_to_response('budget/summaries/summary_year.html', {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }, context_instance=RequestContext(request))

def summary_month(request, year, month):
    start_date = datetime.date(int(year), int(month), 1)
    end_date = datetime.date(int(year), int(month) + 1, 1) - datetime.timedelta(days=1)
    budget = Budget.active.most_current_for_date(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    return render_to_response('budget/summaries/summary_month.html', {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }, context_instance=RequestContext(request))

def budget_list(request):
    budgets = Budget.active.all()
    return render_to_response('budget/budgets/list.html', {
        'budgets': budgets,
    }, context_instance=RequestContext(request))

def budget_add(request):
    if request.POST:
        form = BudgetForm(request.POST)
        
        if form.is_valid():
            budget = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = BudgetForm()
    return render_to_response('budget/budgets/add.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def budget_edit(request, slug):
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    if request.POST:
        form = BudgetForm(request.POST, instance=budget)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = BudgetForm(instance=budget)
    return render_to_response('budget/budgets/edit.html', {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))

def budget_delete(request, slug):
    budget = get_object_or_404(Budget.active.all(), slug=slug)
    if request.POST:
        if request.POST.get('confirmed'):
            budget.delete()
        return HttpResponseRedirect(reverse('budget_budget_list'))
    return render_to_response('budget/budgets/delete.html', {
        'budget': budget,
    }, context_instance=RequestContext(request))

def estimate_list(request, budget_slug):
    budget = get_object_or_404(Budget.active.all(), slug=budget_slug)
    estimates = BudgetEstimate.active.all()
    return render_to_response('budget/estimates/list.html', {
        'budget': budget,
        'estimates': estimates,
    }, context_instance=RequestContext(request))

def estimate_add(request, budget_slug):
    budget = get_object_or_404(Budget.active.all(), slug=budget_slug)
    if request.POST:
        form = BudgetEstimateForm(request.POST)
        
        if form.is_valid():
            estimate = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = BudgetEstimateForm()
    return render_to_response('budget/estimates/add.html', {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))

def estimate_edit(request, budget_slug, estimate_id):
    budget = get_object_or_404(Budget.active.all(), slug=budget_slug)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        form = BudgetEstimateForm(request.POST, instance=estimate)
        
        if form.is_valid():
            category = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = BudgetEstimateForm(instance=estimate)
    return render_to_response('budget/estimates/edit.html', {
        'budget': budget,
        'estimate': estimate,
        'form': form,
    }, context_instance=RequestContext(request))

def estimate_delete(request, budget_slug, estimate_id):
    budget = get_object_or_404(Budget.active.all(), slug=budget_slug)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        if request.POST.get('confirmed'):
            estimate.delete()
        return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    return render_to_response('budget/estimates/delete.html', {
        'budget': budget,
        'estimate': estimate,
    }, context_instance=RequestContext(request))
