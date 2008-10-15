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
    budget = Budget.active.most_current_for_date(datetime.datetime.today())
    return render_to_response('budget/dashboard.html', {
        'budget': budget,
    }, context_instance=RequestContext(request))

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
    estimates_and_transactions = []
    actual_total = Decimal('0.0')
    
    for estimate in budget.estimates.all():
        actual_amount = estimate.actual_amount(start_date, end_date)
        actual_total += actual_amount
        estimates_and_transactions.append({
            'estimate': estimate,
            'transactions': estimate.actual_transactions(start_date, end_date),
            'actual_amount': actual_amount,
        })
    
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
    estimates_and_transactions = []
    actual_total = Decimal('0.0')
    
    for estimate in budget.estimates.all():
        actual_amount = estimate.actual_amount(start_date, end_date)
        actual_total += actual_amount
        estimates_and_transactions.append({
            'estimate': estimate,
            'transactions': estimate.actual_transactions(start_date, end_date),
            'actual_amount': actual_amount,
        })
    
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
