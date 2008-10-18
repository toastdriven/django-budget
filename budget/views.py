import datetime
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from budget.models import Budget, BudgetEstimate
from budget.categories.models import Category
from budget.transactions.models import Transaction
from budget.forms import BudgetEstimateForm, BudgetForm


def dashboard(request, budget_model_class=Budget, transaction_model_class=Transaction, template_name='budget/dashboard.html'):
    today = datetime.date.today()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
    budget = budget_model_class.active.most_current_for_date(datetime.datetime.today())
    
    latest_debits = transaction_model_class.debits.get_latest()
    latest_credits = transaction_model_class.credits.get_latest()
    
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
    
    return render_to_response(template_name, {
        'budget': budget,
        'latest_debits': latest_debits,
        'latest_credits': latest_credits,
        'estimated_amount': estimated_amount,
        'amount_used': amount_used,
        'progress_bar_percent': progress_bar_percent,
        'progress_bar_level': progress_bar_level,
    }, context_instance=RequestContext(request))


def setup(request, template_name='budget/setup.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))


def summary_list(request, transaction_model_class=Transaction, template_name='budget/summaries/summary_list.html'):
    dates = []
    
    try:
        oldest_date = transaction_model_class.active.order_by('date')[0].date
        newest_date = transaction_model_class.active.order_by('-date')[0].date
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
    
    return render_to_response(template_name, {
        'dates': dates,
    }, context_instance=RequestContext(request))


def summary_year(request, year, budget_model_class=Budget, template_name='budget/summaries/summary_year.html'):
    start_date = datetime.date(int(year), 1, 1)
    end_date = datetime.date(int(year), 12, 31)
    budget = budget_model_class.active.most_current_for_date(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    return render_to_response(template_name, {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }, context_instance=RequestContext(request))


def summary_month(request, year, month, budget_model_class=Budget, template_name='budget/summaries/summary_month.html'):
    start_date = datetime.date(int(year), int(month), 1)
    end_date = datetime.date(int(year), int(month) + 1, 1) - datetime.timedelta(days=1)
    budget = budget_model_class.active.most_current_for_date(end_date)
    estimates_and_transactions, actual_total = budget.estimates_and_transactions(start_date, end_date)
    return render_to_response(template_name, {
        'budget': budget,
        'estimates_and_transactions': estimates_and_transactions,
        'actual_total': actual_total,
        'start_date': start_date,
        'end_date': end_date,
    }, context_instance=RequestContext(request))


def budget_list(request, model_class=Budget, template_name='budget/budgets/list.html'):
    budgets_list = model_class.active.all()
    try:
        paginator = Paginator(budgets_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        budgets = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    return render_to_response(template_name, {
        'budgets': budgets,
        'paginator': paginator,
        'page': page,
    }, context_instance=RequestContext(request))


def budget_add(request, form_class=BudgetForm, template_name='budget/budgets/add.html'):
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            budget = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = form_class()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


def budget_edit(request, slug, model_class=Budget, form_class=BudgetForm, template_name='budget/budgets/edit.html'):
    budget = get_object_or_404(model_class.active.all(), slug=slug)
    if request.POST:
        form = form_class(request.POST, instance=budget)
        
        if form.is_valid():
            category = form.save()
            return HttpResponseRedirect(reverse('budget_budget_list'))
    else:
        form = form_class(instance=budget)
    return render_to_response(template_name, {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))


def budget_delete(request, slug, model_class=Budget, template_name='budget/budgets/delete.html'):
    budget = get_object_or_404(model_class.active.all(), slug=slug)
    if request.POST:
        if request.POST.get('confirmed'):
            budget.delete()
        return HttpResponseRedirect(reverse('budget_budget_list'))
    return render_to_response(template_name, {
        'budget': budget,
    }, context_instance=RequestContext(request))


def estimate_list(request, budget_slug, budget_model_class=Budget, model_class=BudgetEstimate, template_name='budget/estimates/list.html'):
    budget = get_object_or_404(budget_model_class.active.all(), slug=budget_slug)
    estimates_list = model_class.active.all()
    try:
        paginator = Paginator(estimates_list, getattr(settings, 'BUDGET_LIST_PER_PAGE', 50))
        page = paginator.page(request.GET.get('page', 1))
        estimates = page.object_list
    except InvalidPage:
        raise Http404('Invalid page requested.')
    return render_to_response(template_name, {
        'budget': budget,
        'estimates': estimates,
        'paginator': paginator,
        'page': page,
    }, context_instance=RequestContext(request))


def estimate_add(request, budget_slug, budget_model_class=Budget, form_class=BudgetEstimateForm, template_name='budget/estimates/add.html'):
    budget = get_object_or_404(budget_model_class.active.all(), slug=budget_slug)
    if request.POST:
        form = form_class(request.POST)
        
        if form.is_valid():
            estimate = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = form_class()
    return render_to_response(template_name, {
        'budget': budget,
        'form': form,
    }, context_instance=RequestContext(request))


def estimate_edit(request, budget_slug, estimate_id, budget_model_class=Budget, form_class=BudgetEstimateForm, template_name='budget/estimates/edit.html'):
    budget = get_object_or_404(budget_model_class.active.all(), slug=budget_slug)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        form = form_class(request.POST, instance=estimate)
        
        if form.is_valid():
            category = form.save(budget=budget)
            return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    else:
        form = form_class(instance=estimate)
    return render_to_response(template_name, {
        'budget': budget,
        'estimate': estimate,
        'form': form,
    }, context_instance=RequestContext(request))


def estimate_delete(request, budget_slug, estimate_id, budget_model_class=Budget, template_name='budget/estimates/delete.html'):
    budget = get_object_or_404(budget_model_class.active.all(), slug=budget_slug)
    try:
        estimate = budget.estimates.get(pk=estimate_id, is_deleted=False)
    except ObjectDoesNotExist:
        raise Http404("The requested estimate could not be found.")
    if request.POST:
        if request.POST.get('confirmed'):
            estimate.delete()
        return HttpResponseRedirect(reverse('budget_estimate_list', kwargs={'budget_slug': budget.slug}))
    return render_to_response(template_name, {
        'budget': budget,
        'estimate': estimate,
    }, context_instance=RequestContext(request))
